import os
import tkinter as tk
from tkinter import filedialog
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders
import importlib.util


class EmailSender:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Email Sender")
        self.file_path = None
        self.email_to = tk.StringVar()

        # read email and password from config file
        config_path = os.path.join(os.path.dirname(__file__), "config.py")
        if os.path.exists(config_path):
            config_spec = importlib.util.spec_from_file_location("config", config_path)
            config_module = importlib.util.module_from_spec(config_spec)
            config_spec.loader.exec_module(config_module)
            self.email_from = config_module.email
            self.email_password = config_module.password
        else:
            self.email_from = None
            self.email_password = None
            tk.messagebox.showerror("Error", "Config file not found")

        # create the GUI components
        self.file_label = tk.Label(self.window, text="No file selected")
        self.select_file_button = tk.Button(self.window, text="Select file", command=self.select_file)
        self.email_label = tk.Label(self.window, text="Email to:")
        self.email_entry = tk.Entry(self.window, textvariable=self.email_to)
        self.send_button = tk.Button(self.window, text="Send", command=self.send_email)

        # layout the GUI components
        self.file_label.pack()
        self.select_file_button.pack()
        self.email_label.pack()
        self.email_entry.pack()
        self.send_button.pack()

        self.window.mainloop()

    def select_file(self):
        self.file_path = filedialog.askopenfilename()
        self.file_label.config(text=self.file_path)

    def send_email(self):
        if not self.file_path:
            tk.messagebox.showerror("Error", "No file selected")
            return

        if not self.email_from or not self.email_password:
            tk.messagebox.showerror("Error", "Email or password not found in config file")
            return

        email_to = self.email_to.get()

        msg = MIMEMultipart()
        msg['From'] = self.email_from
        msg['To'] = COMMASPACE.join([email_to])
        msg['Subject'] = "File Attached"
        msg.attach(MIMEText("Please find attached the file you requested."))

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(self.file_path, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=self.file_path.split("/")[-1])
        msg.attach(part)

        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login(self.email_from, self.email_password)
        smtp_server.sendmail(self.email_from, email_to, msg.as_string())
        smtp_server.quit()

        tk.messagebox.showinfo("Email Sent", "The email was sent successfully.")


EmailSender()
