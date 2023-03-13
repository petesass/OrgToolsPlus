from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image

def convert_image(image_path, width):
    ascii_chars = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@', 'W', 'B', '$', 'O', '8']
    image = Image.open(image_path)
    hsize = int((float(image.size[1]) * float(width / image.size[0])) / 2)
    image = image.resize((width, hsize), Image.LANCZOS)
    pixels = image.load()
    ascii_text = ""
    for y in range(hsize):
        for x in range(width):
            pixel = pixels[x, y]
            pixel_brightness = sum(pixel) / 3
            ascii_text += ascii_chars[int((pixel_brightness/21.25))]
        ascii_text += "\n"
    return ascii_text

def select_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        ascii_text = convert_image(file_path, width=200)
        root.clipboard_clear()
        root.clipboard_append(ascii_text)
        messagebox.showinfo("Success", "The ASCII art has been copied to your clipboard!")

root = Tk()
root.title("ASCII Art Converter")
root.geometry("300x100")

select_button = Button(root, text="Select Image", command=select_image)
select_button.pack(pady=20)

root.mainloop()
