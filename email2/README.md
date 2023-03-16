*```email2.py```*

This is a simple GUI that allows the user to choose a file and fill out an email field to quickly send files. 
Requires a little bit of first-time-use configuration.

You have to edit *```config.py```* to fill out your own email address and app password.

  *WHATS AN APP PASSWORD? (& WHY?)*
  
  An app password is a unique identifier provided to you by your email provider to represent your password for use in apps, like in *```email2.py```*.
  You can find your app password somewhere in your email settings; every provider is different. In my example I use Gmail.
   
   1. Go to google.com and sign in
   
   2. Click on your icon and click on Manage your Google Account
   
   3. Click on Security tab
   
   4. Turn on 2-Step Verification
   
   5. Reload
   
   6. Click on the Search Google Account search bar
   
   7. Search for App passwords
   
   8. Select the app and device you want to generate the app password for. I used Mail/Windows but I think anything probably works.
   
   9. Copy your newly generated app password and paste it into *```config.py```*.
   
   10. That's it! If you encounter any issues open a request and I'll look into it.
   
   *Why do I have to do all this setup?*
   
   For security and customization purposes, this is the only way I could figure out how to link an email account to the app. Once you set it up, it will always work!
