# PyChromium: A Simple Extensible Browser

PyChromium is a minimalistic web browser developed in Python, designed with extensibility and simplicity in mind. It supports loading extensions, managing downloads, and basic browsing functionalities. The codebase is structured to be easily understandable and modifiable, making it a perfect starting point for those looking to build or customize their own browsers.

![Browser Icon](chromium.ico)

## 📦 Installation

Before running PyChromium, ensure you have [Python](https://www.python.org/downloads/) installed on your system. You can install the necessary libraries individually using pip, or all at once using a `requirements.txt` file.

### Individual Installation:

```bash
pip install PyQt5
pip install PyQtWebEngine
pip install requests
pip install wget
```
### Using `requirements.txt`:

First, create a `requirements.txt` file with the following content:

```plaintext
PyQt5
PyQtWebEngine
requests
wget
```
Then, run the following command:

```bash
pip install -r requirements.txt
```

### 🚀 Usage

Once the required libraries are installed, execute the browser script to launch PyChromium. The browser encompasses basic functionalities such as navigation, search, browsing history, downloads management, and settings configuration as well as more advanced settings such as themes, custom update server and more.

### 🛠️ Extensions

PyChromium supports loading extensions to enhance its functionality. You can add your own extensions or modify existing ones to tailor the browser to your needs.

### 🤝 Contributing

Feel free to fork, modify, and customize PyChromium to suit your preferences. This project serves as a foundation for building a personalized web browser.

### 📄 License

PyChromium is licensed under the MIT License.

### 🖥️ Standalone Application

If you prefer running PyChromium as a standalone application without a Python runtime, you can compile it using PyInstaller.

First, install PyInstaller:
```bash
pip install pyinstaller
```

Then, compile PyChromium. The compilation process will take approximately 4 minutes:
```bash
# MacOS & Linux
pyinstaller --onefile --noconsole --add-data "chromium-mac.icns:." --add-data "chromium-no-bg.icns:." --add-data "chromium-old.ico:." --add-data "chromium.ico:." --icon=chromium-mac.icns chromium.py

# Windows
pyinstaller --onefile --noconsole --add-data "chromium-mac.icns;." --add-data "chromium-no-bg.icns;." --add-data "chromium-old.ico;." --add-data "chromium.ico;." --icon=chromium.ico chromium.py
```

⚠️ Note: PyInstaller compiles the application for the operating system it's run on. For example, if you compile on Windows, the executable will only work on other Windows machines. And, if compiled on Mac, it will only run on other Mac machines. (Not tested on linux my gut is that it will only work on the same linux distro with the same system Arch).
