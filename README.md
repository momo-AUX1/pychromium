# Simple Python Browser
This is a basic web browser built in Python with support for loading extensions and downloading files. The code is designed to be easily readable, allowing anyone to modify and customize it according to their needs.

 #Installation
To run this browser, you'll need to install the necessary libraries. You can do this using pip with the following commands:

```bash
Copy code
pip install pyqt5
pip install wget
Make sure you have Python installed on your system before running the application.
```
# Usage
Once you have installed the required libraries, you can run the browser script. The browser provides basic functionality like navigation, search, history, downloads, and settings.

# Extensions
The browser also supports loading extensions. You can add your own extensions to enhance the functionality of the browser.

# Contributing
Feel free to modify and customize the code to suit your preferences. This project is designed to be a starting point for building your own custom browser.

# License
This project is licensed under the MIT License.

# Don't want to run it on Python?
you can compile the browser to run natively without any python runtime!
to do so you need to install pyinstaller 
```bash
pip install pyinstaller
```
then you can compile it directly (roughly 4 minutes)
```bash
pyinstaller --onefile --name=my_browser --add-data="chromium.ico;." simple_browser.py
```
