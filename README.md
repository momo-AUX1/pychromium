# PyChromium: A Simple Extensible Browser

PyChromium is a minimalistic web browser developed in Python, designed with extensibility and simplicity in mind. It supports loading extensions, managing downloads, and basic browsing functionalities. The codebase is structured to be easily understandable and modifiable, making it a perfect starting point for those looking to build or customize their own browsers.

![Browser Icon](chromium.ico)

## 📦 Installation

Before running PyChromium, ensure you have [Python](https://www.python.org/downloads/) installed on your system. You can install the necessary libraries individually using pip, or all at once using a `requirements.txt` file.

### Individual Installation:

```bash
pip install PyQt5
pip install PyQt6
pip install PyQtWebEngine
pip install PyQt6-WebEngine
pip install requests
pip install wget
```
### Using `requirements.txt`:

First, create a `requirements.txt` file with the following content:

```plaintext
PyQt5
PyQt6
PyQtWebEngine
PyQt6-WebEngine
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
# For Mac/Linux
pyinstaller --onefile --noconsole --add-data "chromium-mac.icns:." --add-data "chromium-no-bg.icns:." --add-data "chromium-old.ico:." --add-data "chromium.ico:." --add-data "Icons/back.png:Icons" --add-data "Icons/download.png:Icons" --add-data "Icons/extensions.png:Icons" --add-data "Icons/forward.png:Icons" --add-data "Icons/history.png:Icons" --add-data "Icons/home.png:Icons" --add-data "Icons/more.png:Icons" --add-data "Icons/new-tab.png:Icons" --add-data "Icons/refresh.png:Icons" --add-data "Icons/remove-tab.png:Icons" --add-data "Icons/settings.png:Icons" --add-data "Icons/settings-old.png:Icons" --add-data "pdfjs/pdfjs.html:pdfjs" --add-data "pdfjs/pdf.worker.js:pdfjs" --add-data "pdfjs/images:pdfjs/images" --add-data "pdfjs/cmaps:pdfjs/cmaps" --icon=chromium-mac.icns chromium.py

# For Windows
pyinstaller --onefile --noconsole --add-data "chromium-mac.icns;." --add-data "chromium-no-bg.icns;." --add-data "chromium-old.ico;." --add-data "chromium.ico;." --add-data "Icons/back.png;Icons" --add-data "Icons/download.png;Icons" --add-data "Icons/extensions.png;Icons" --add-data "Icons/forward.png;Icons" --add-data "Icons/history.png;Icons" --add-data "Icons/home.png;Icons" --add-data "Icons/more.png;Icons" --add-data "Icons/new-tab.png;Icons" --add-data "Icons/refresh.png;Icons" --add-data "Icons/remove-tab.png;Icons" --add-data "Icons/settings.png;Icons" --add-data "Icons/settings-old.png;Icons" --add-data "pdfjs/pdfjs.html;pdfjs" --add-data "pdfjs/pdf.worker.js;pdfjs" --add-data "pdfjs/images;pdfjs\images" --add-data "pdfjs/cmaps;pdfjs\cmaps"  --icon=chromium.ico chromium.py
```

⚠️ Note: PyInstaller compiles the application for the operating system it's run on. For example, if you compile on Windows, the executable will only work on other Windows machines. And, if compiled on Mac, it will only run on other Mac machines. (Not tested on linux my gut is that it will only work on the same linux distro with the same system Arch).

# 🌐 Extending PyChromium: Extensions Deep Dive

Extensions in PyChromium eallows you to supercharge the browser's functionality, allowing for a lot customization options.

### 🛠️ Capabilities of Extensions:

1. 🌍 Direct Browser Manipulation: You can directly interface with the browser's core. Like change the current URL without the need for JavaScript:
   ```python
   browser.load(QUrl("https://example.com"))
   ````

2. 🎨 Local Configuration Modifications: Extensions can directly modify local files:
   ```python
   with open("theme.stg", "w") as f:
    f.write("""
    QWidget {
        background-color: #000000;  
        color: #FFA500;  
    }
    QTabBar::tab {
        background-color: #FFA500;  
        color: #000000;  
    }
    QPushButton {
        background-color: #FFA500;  
        border: none;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #FF8C00;  
    }
   """)  
   ```
3. 💻 Javascript Injection: Run JavaScript seamlessly on your current page:
   ```python
   js_code = """..."""
   browser.page().runJavaScript(js_code)
   ```

4. 🐍 Python Program Interactions: Extensions can tap into other Python scripts or libraries, broadening the browser's capabilities.

### 🚧 Considerations:

🔒 Security: Always prioritize security. The depth of access means a minor oversight can introduce vulnerabilities.

📝 Note: When writing extensions, your IDE might indicate that certain variables (like browser) are not declared. This is expected. Extensions are executed within the PyChromium environment where these variables are defined.

### 📖 Example Extensions:

1. 🔴 Red Hello Div: Add a static red div to any webpage that greets the user:
   
   ```python
   def add_hello_div(browser):
    js_code = """
    (function() {
        let helloDiv = document.createElement("div");
        helloDiv.style.position = "fixed";
        helloDiv.style.top = "10px";
        helloDiv.style.right = "10px";
        helloDiv.style.backgroundColor = "red";
        helloDiv.style.color = "white";
        helloDiv.style.padding = "10px";
        helloDiv.style.borderRadius = "5px";
        helloDiv.style.zIndex = "9999";  
        helloDiv.innerText = "Hello";
        
        document.body.appendChild(helloDiv);
    })();"""

    browser.page().runJavaScript(js_code)

   add_hello_div(browser)
   ```

2. 🚫 Adblocker: A simple ad-blocking extension:
   ```python
   def block_ads(browser):
    ad_selectors = [
        'iframe[src*="ads-iframe"]',
        'div[id*="ad-container"]',
        'div[class*="ad-banner"]',
        'iframe[id*="google_ads_frame"]',
        'ins[class*="adsbygoogle"]',
    ]

    selectors_string = ', '.join([f'"{selector}"' for selector in ad_selectors])
    
    js_code = f"""
    (function() {{
        const adSelectors = [{selectors_string}];
        setInterval(() => {{
            adSelectors.forEach(selector => {{
                document.querySelectorAll(selector).forEach(ad => {{
                    ad.style.display = "none";
                }});
            }});
        }}, 1000);  /
    }})();"""

    browser.page().runJavaScript(js_code)

   block_ads(browser)
   ```

Extensions gives you the power to change browser variables and call it's functions or even make new functions it's a very raw, low level access that you may use to enhance the browser, why not port your favorite extension over?
