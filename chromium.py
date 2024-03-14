import PyQt5
import PyQt5.sip
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QToolBar, QLineEdit, QFileDialog, QListWidget, QWidget, QRadioButton, QVBoxLayout, QGridLayout, QLabel, QPushButton, QTabWidget, QMenu, QDialog, QTextBrowser,QShortcut
from PyQt5.QtGui import QIcon, QCursor, QKeySequence
from PyQt5.QtCore import QUrl, QUrlQuery
import sys
import requests 
import wget
import sqlite3
import os
import subprocess
from os.path import join, exists
import platform
import json
import tempfile

#checks if the Pyext folder exists if not it makes one
if not exists('Pyext'):
    os.makedirs('Pyext')

if not exists('temp'):
    os.makedirs('temp')

if not exists('Icons'):
    os.makedirs('Icons')
    with open('Icons/readme-icons.txt', 'w') as f:
        f.write("""
###### here you can custom icons that the browser can use instead of the defined ones here's a list of all the icon names that it checks for:
          -back.png 
          -download.png 
          -extensions.png 
          -forward.png 
          -history.png 
          -home.png 
          -more.png 
          -new-tab.png
          -refresh.png 
          -remove-tab.png 
          -settings-old.png 
          -settings.png  
#the recommended icon size is 16x16px you can find some vintage icons like the one i used at this link : https://www.iconarchive.com/
#you can also use your own icons just make sure to name them as the ones above and put them in the Icons folder
""")

extensions = []
ver = 15.2
tab_num = 0
checked_extensions = False
current_tab_index = -1  
valid_url_suffixes = [
    '.com', '.org', '.net', '.io', '.ai', '.co', '.edu', '.gov',
    '.uk', '.ru', '.in', '.de', '.fr', '.jp', '.nl', '.it', '.br', '.pl', '.ir',
    '.es', '.au', '.biz', '.info', '.me', '.tv', '.cc', '.cn', '.eu', '.xyz',
    '.site', '.online', '.us', '.ca', '.git', '.web', '.app', '.blog', '.shop',
    '.club', '.space', '.link', '.tech', '.dev', '.wiki', '.agency', '.email',
    '.cloud'
]

conn = sqlite3.connect('history.db')
conn.execute('CREATE TABLE IF NOT EXISTS history (history TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS downloads (downloads TEXT)')

def try_home():
    #checks for your current search engine
    global homepage
    try:
        with open('home.stg', 'r') as f:
            homepage = f.read()
    except FileNotFoundError:
        homepage = "https://google.com/" 

def try_path():
    #checks for the download folder if changed
    global path
    try:
        with open('path.stg', 'r') as f:
            path = f.read()
    except FileNotFoundError:
        if os.name == 'nt': 
            path = os.path.join(os.path.expanduser('~'), 'Downloads')
        else:  
            path = os.path.join(os.path.expanduser('~'), 'Downloads')

def try_theme():
    #checks if the theme is set
    global theme
    try:
        with open('theme.stg', 'r') as f:
            theme = f.read()
            if "none" in theme:
                theme = None
    except FileNotFoundError:
        theme = None


def check_extensions():
    #searches for extensions and saves them
    try:
        A = os.listdir('Pyext')
        for element in A:
            if '.py' in element or '.ext' in element:
                extensions.append(element)
                sys.path.append(f"Pyext/{element}")        
    except:
        pass

def scan_extensions(content):
    if "__pychromium_metadata__" in content:
        try:
            extension_data = json.loads(content.split("=")[1].strip())
            external_check = requests.post("https://nanodata.pythonanywhere.com/check", json=extension_data)
            if external_check.json().get("status") == "approved":
                return ("The extension is safe to run", False)
            elif external_check.json().get("status") == "dangerous":
                return (f"The extension is not safe to run and has been reported. Reason: {external_check.json().get('reason')}", True)
        except:
            pass
    else:
        pass
    dangerous_extensions = ["import os", "import requests", "import base64", "import subprocess", " import sys", "import shutil", "import socket", "import urllib", "import pickle", "import importlib", "import exec", "import eval", "open", "write", "read", "remove", "import unlink", "rmdir", "mkdir", "chdir", "chmod", "chown", "chroot", "close", "connect", "accept", "bind", "import listen", "import fork", "import kill", "import popen", "import system", "import spawn", "import start", "import fork", " import pipe"]

    found_extensions = [ext for ext in dangerous_extensions if ext in content]

    if found_extensions:
        warnings = []
        for ext in found_extensions:
            warnings.append(f"{ext}")
        
        warning_message = "The file you are trying to run is not safe. It contains the following potentially dangerous imports:\n\n" + "\n".join(warnings) + "\n\nThese imports can be used to run malicious code on your computer. Are you sure you want to run it?"
        return (warning_message, True)
    else:
        return ("No dangerous imports found. The file appears to be safe.", False)

    

def server_handler():
    #sets the server url for the update
    server_url = update_server.text()
    with open("server.stg", "w") as f:
        f.write(server_url)

def check_update():
    #tries to check for an update 
    global app
    try:
        server = open("server.stg").read()
        A = requests.post(server, json={'version': int(ver)})
        version = A.json().get('version')
    except:
        version = 0

    if version > int(ver):
        msg = QMessageBox()
        msg.setWindowTitle('Update handler')
        msg.setIcon(QMessageBox.Question)
        msg.setText(f'version : {version} is available do you want to update?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg.exec_()
        if result == QMessageBox.Yes:
            system = platform.system()
            if system.lower() == 'windows':
                try:
                    wget.download(server, 'Py-Chromium.exe')
                    win.hide()
                    os.startfile('Py-Chromium.exe')
                    app.exit()
                except:
                    msg_err = QMessageBox()
                    msg_err.setWindowTitle('Download Error')
                    msg_err.setText('Couldn\'t download the Windows version of the app. Please ensure Py-Chromium.exe exists on the server.')
                    msg_err.setIcon(QMessageBox.Critical)
                    msg_err.exec_()

            elif system.lower() == 'darwin':
                try:
                    wget.download(server, 'Py-Chromium.app')
                    win.hide()
                    opener = "open"
                    subprocess.call([opener, 'Py-Chromium.app'])
                    app.exit()
                except:
                    msg_err = QMessageBox()
                    msg_err.setWindowTitle('Download Error')
                    msg_err.setText('Couldn\'t download the Mac version of the app. Please ensure Py-Chromium.app exists on the server.')
                    msg_err.setIcon(QMessageBox.Critical)
                    msg_err.exec_()
        else:
            pass
    else:
        pass

def search_handler():
    # When you hit enter on the search bar, this is the logic behind it.
    browser = tabs.currentWidget()
    url = search.text().strip()

    if url.startswith('file:///'):
        pass
    
    # Check if the entered text is a URL
    elif '://' in url or any(url.endswith(suffix) for suffix in valid_url_suffixes):
        if not url.startswith(('http://', 'https://')):
            url = f"http://{url}"  # Default to HTTP if no scheme is provided

    else:
        # Treat the entered text as a search query
        query = url.replace(" ", "+")
        try:
            with open("home.stg", "r") as f:
                homepage = f.read().strip()
                if "duckduckgo" in homepage:
                    url = f"{homepage}/?q={query}"
                elif "ecosia" in homepage:
                    url = f"{homepage}/search?q={query}"
                else:
                    url = f"{homepage}/search?q={query}"
        except FileNotFoundError:
            url = f"{homepage}/search?q={query}"

    browser.setUrl(QUrl(url))

def home_handler():
    #goes to the home page
    try_home()
    browser = tabs.currentWidget()
    browser.setUrl(QUrl(homepage))

def back_handler():
    #goes back
    browser = tabs.currentWidget()
    browser.back()

def show_more_menu():
    file_menu.exec_(QCursor.pos())

def download_handler(dl):
    # When a download signal is caught alerts the user if the user answer is yes download the file to their destination
    global path
    file_url = dl.url().toString()
    file_name = file_url.split('/')[-1] 
    print(file_name)
    try_path()
    if path:
        save_path = join(path, file_name)
        dl.setPath(save_path)
    
    if file_name.lower().endswith('.pdf'):
        msg = QMessageBox()
        msg.setWindowTitle("PDF Detected")
        msg.setText(f"Do you want to open or download the PDF: {file_name}?")
        msg.setIcon(QMessageBox.Question)  
        open_button = msg.addButton("Open", QMessageBox.YesRole)
        download_button = msg.addButton("Download", QMessageBox.AcceptRole)
        cancel_button = msg.addButton(QMessageBox.Cancel)
        result = msg.exec_()

        if msg.clickedButton() == open_button:
            handle_pdf(file_url)
        elif msg.clickedButton() == download_button:
            dl.accept() 
            conn.execute("INSERT INTO downloads VALUES (?)", (file_name,))
            conn.commit()

    else:
        msg = QMessageBox()
        msg.setWindowTitle("Download Handler")
        msg.setText(f"Are you sure you want to download {file_name}?")
        msg.setIcon(QMessageBox.Question) 
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg.exec_()
        
        if result == QMessageBox.Yes:
            dl.accept()
            conn.execute("INSERT INTO downloads VALUES (?)", (file_name,))
            conn.commit()




def download_pdf(url):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            temp_pdf, temp_pdf_path = tempfile.mkstemp(suffix='.pdf')
            os.close(temp_pdf)  
            with open(temp_pdf_path, 'wb') as f:
                f.write(response.content)

            return temp_pdf_path
        return None
    except:
        pass



def handle_pdf(file_url):
    temp_pdf_path = None
    if file_url.startswith("http"):
        temp_pdf_path = download_pdf(file_url)
        if temp_pdf_path is None:
            QMessageBox.critical(None, "Download Error", "Failed to download the PDF.")
            return
        file_url = temp_pdf_path

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    pdfjs_html_path = os.path.join(base_path, 'pdfjs', 'pdfjs.html')
    pdfjs_worker_path = os.path.join(base_path, 'pdfjs', 'pdf.worker.js')
    images_path = os.path.join(base_path, 'pdfjs', 'images')
    cmaps_path = os.path.join(base_path, 'pdfjs', 'cmaps')
    if not os.path.exists(pdfjs_html_path) or not os.path.exists(pdfjs_worker_path):
        QMessageBox.critical(None, "PDF Viewer Error", "The PDF viewer or worker file cannot be found download the file to view.")
        return
    
    with open(pdfjs_html_path, 'r') as file:
        html_content = file.read()
    
    modified_html_content = html_content.replace("{PDFJS_WORKER_PATH}", pdfjs_worker_path)
    modified_html_content = modified_html_content.replace("{IMAGES_URL}", images_path)
    modified_html_content = modified_html_content.replace("{CMAPS_URL}", cmaps_path)

    temp_html_file, temp_html_path = tempfile.mkstemp(suffix='.html')
    os.close(temp_html_file)  

    with open(temp_html_path, 'w') as file:
        file.write(modified_html_content)


    if os.path.isfile(file_url):
        file_url = QUrl.fromLocalFile(file_url).toString().split(":")[1]
    viewer_url = f"file:///{temp_html_path}?file={file_url}"

    new_tab = QWebEngineView()
    new_tab.setUrl(QUrl(viewer_url))
    tabs.addTab(new_tab, "PDF Viewer")





def history_writer():
    #writes to history upon any change
    current_url = browser.url().toString()
    search.setText(current_url)
    conn.execute("INSERT INTO history VALUES (?)", (current_url,))
    conn.commit()

def go_to_link(url):
    #changes the url link
    url = url.text()
    browser = tabs.currentWidget()
    browser.setUrl(QUrl(url))

def history_handler():
    #writes the history to a db. if it doesn't exist, it makes one.
    try:
        all = conn.execute("SELECT * FROM history").fetchall()
    except:
        conn.execute("CREATE TABLE history (history TEXT)")
        all = conn.execute("SELECT * FROM history").fetchall()
    for previous in all:
        list.addItem(previous[0])
    list.show()
    list.itemClicked.connect(go_to_link)


def path_picker():
    #downloads folder path if changed from normal
    folder_picker = QFileDialog.getExistingDirectory()
    if folder_picker:
        with open('path.stg', 'w') as f:
            f.write(folder_picker)

def engine_picker(home_path):
    #sets the search engine
    with open('home.stg', 'w') as f:
        f.write(home_path)

def theme_picker1():
    with open('theme.stg', 'w') as f:
        f.write('none')

def theme_picker2():
    #toggles dark mode
    with open('theme.stg', 'w') as f:
        f.write("""
    QWidget {
        background-color: #2b2b2b;
        color: #ffffff;
    }
    QTabBar::tab {
        color: #2b2b2b;
    }
    """)

def history_cleaner():
    #drops all history
    conn.execute("DROP TABLE IF EXISTS history")
    conn.commit()


def settings_handler():
    #shows the settings and it's layout
    sub.setWindowTitle('Settings')
    
    layout = QVBoxLayout()
    
    layout.addWidget(update_server_info)
    layout.addWidget(update_server)
    layout.addWidget(toggle_server)
    layout.addWidget(setting_info)
    layout.addWidget(radio1)
    layout.addWidget(radio2)
    layout.addWidget(radio3)
    layout.addWidget(radio_eco)
    layout.addWidget(theme_info)
    layout.addWidget(radio4)
    layout.addWidget(radio5)
    layout.addWidget(download_info)
    layout.addWidget(button)
    layout.addWidget(history_info)
    layout.addWidget(clear_history)
    
    sub.setLayout(layout)
    
    button.clicked.connect(path_picker)
    clear_history.clicked.connect(history_cleaner)
    radio1.clicked.connect(lambda: engine_picker("https://google.com/"))
    radio2.clicked.connect(lambda: engine_picker("https://bing.com/"))
    radio3.clicked.connect(lambda: engine_picker("https://duckduckgo.com/"))
    radio_eco.clicked.connect(lambda: engine_picker("https://ecosia.org"))
    radio4.clicked.connect(theme_picker1)
    radio5.clicked.connect(theme_picker2)
    toggle_server.clicked.connect(server_handler)
    
    clear_history.show()
    button.show()

    sub.setFixedSize(300, 500)
    sub.show()


def load_file(file):
    #executes a downloaded file
    try_path()
    file_path = join(path, file.text())
    try:
        if sys.platform == "win32":
            os.startfile(file_path)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, file_path])
    except:
        msg_dl.setWindowTitle("Error")
        msg_dl.setText("the application cannot found the specified file at the specified path (the path set in settings)")
        msg_dl.setIcon(QMessageBox.Critical)
        msg_dl.show()

def downloads_handler():
    #shows everything you downloaded
    list_dl.setWindowTitle("Downloads")
    list_dl.clear()
    all_dl = conn.execute("SELECT * FROM downloads").fetchall()
    for dl in all_dl:
        list_dl.addItem(dl[0])
    list_dl.itemClicked.connect(load_file)
    list_dl.show()

def forward_handler():
    #goes forward 
    browser = tabs.currentWidget()
    browser.forward()

def refresh_handler():
    #refreshes the page
    browser = tabs.currentWidget()
    browser.reload()

def extensions_loader(extension):
    #loads extensions
    with open(join("Pyext", extension.text()), "r") as f:
        content = f.read()
    scan_results, dangerous = scan_extensions(content)
    if dangerous:
        msg = QMessageBox()
        msg.setWindowTitle("Extension warning")
        msg.setIcon(QMessageBox.Warning)
        msg.setText(scan_results)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg.exec()
        if result == QMessageBox.Yes:
            exec(content)
        else:
            pass
    else:
        exec(content)
            
def extension_handler():
    global checked_extensions
    #sets every extension as clickable and only appends them once then passes it to extension_loader
    ext_list.setWindowTitle("Extensions")
    if checked_extensions == False:
        for extension in extensions:
            ext_list.addItem(extension)
        checked_extensions = True
    else:
        pass
    ext_list.itemClicked.connect(extensions_loader)
    ext_list.show()

def add_tabs_handler(url=None):
    global tab_num
    new_tab = QWebEngineView()
    tab_num += 1
    new_tab_index = tabs.addTab(new_tab, f"tab {tab_num}")

    # Set initial URL if provided
    if url:
        new_tab.setUrl(QUrl(url))
    else:
        new_tab.setUrl(QUrl(homepage))

    # Connect the titleChanged signal
    new_tab.titleChanged.connect(lambda title, index=new_tab_index: update_tab_title(index, title))


def update_tab_title(tab_index, new_title):
    if new_title:
        tabs.setTabText(tab_index, new_title)

def update_current_tab_index(index):
    global current_tab_index
    current_tab_index = index

def remove_tab_handler():
    #removes the current tab the user is on
    tabs.removeTab(tabs.currentIndex())

def about_handler():
    dialog = QDialog()
    dialog.setWindowTitle("About Py Chromium")
    dialog.setFixedSize(400, 300)
    layout = QVBoxLayout(dialog)
    about_text = QTextBrowser()
    about_text.setOpenExternalLinks(False)  
    def on_link_clicked(url):
        browser.setUrl(url)
        about_text.setHtml(about_text.toHtml())

    about_text.anchorClicked.connect(on_link_clicked)
    about_text.setHtml(f"""
    <h1>Py Chromium</h1>
    <p><strong> Version:</strong> {str(float(ver))[:1]+'.'+str(float(ver)).split(str(float(ver))[:1])[1]}</p>
    <p>A lightweight web browser built with Python and PyQt. </p>
    <p><strong> © <a href='https://github.com/momo-AUX1'>Mohammed</a> 2024</strong></p>
    <p> Powered by:</p>
    <ul>
    <li>Python 3: <a href="https://www.python.org/"> https://www.python.org/</a></li>
    <li>PyQt5 (Qt): <a href="https://www.riverbankcomputing.com/software/pyqt/"> https://www.riverbankcomputing.com/software/pyqt/</a> </li>
    <li>Chromium: <a href="https://www.chromium.org/">https://www.chromium.org/</a></li>
    <li>SQLite: <a href="https://www.sqlite.org/">https://www.sqlite.org/</a></li>
    <li>Requests: <a href="https://requests.readthedocs.io/en/master/"> https://requests.readthedocs.io/en/master/</a> </li>
    <li>Wget: <a href="https://www.gnu.org/software/wget/"> https://www.gnu.org/software/wget/</a></li>
    </ul>
    <p>All product names, logos, and brands are the property of their respective owners. The use of these names, logos, and brands does not imply endorsement. </p>""")
    layout.addWidget(about_text)
    close_button = QPushButton('Close')
    close_button.clicked.connect(dialog.close)
    layout.addWidget(close_button)
    dialog.exec_()


def close_current_tab(index):
    tabs.removeTab(index)

def get_icon(icon_name):
    if getattr(sys, 'frozen', False):
        bundled_icon_path = join(sys._MEIPASS, 'Icons', f'{icon_name}.png')
        icon = QIcon(bundled_icon_path)
        if icon.isNull():
            return QIcon()  
        return icon
    else:
        user_defined_icon_path = f'Icons/{icon_name}.png'
        icon = QIcon(user_defined_icon_path)
        if icon.isNull():
            return QIcon()  
        return icon

#main app code
app = QApplication(sys.argv)

#checks for updates
check_update()

#checks for extensions
check_extensions()

#checks if the theme was set
try_theme()

win = QMainWindow()
browser = QWebEngineView()
upper_bar = QToolBar()
upper_bar.setMovable(False)
search = QLineEdit()
list = QListWidget()
sub = QWidget()
box = QGridLayout()
radio1 = QRadioButton('google')
radio2 = QRadioButton('bing')
radio3 = QRadioButton('duckduckgo')
radio_eco = QRadioButton('ecosia')
radio4 = QRadioButton('set light theme')
radio5 = QRadioButton('set dark theme')
setting_info = QLabel('Choose preferred engine')
theme_info = QLabel('Choose preferred theme (Requires restart)')
download_info = QLabel('Choose preferred download folder')
history_info = QLabel('Clear search history')
button = QPushButton('Select folder')
clear_history = QPushButton('Clear history')
list_dl = QListWidget()
msg_dl = QMessageBox()
ext_list = QListWidget()
tabs = QTabWidget()
tabs.setTabsClosable(True)
button.hide()
clear_history.hide()
update_server_info = QLabel('Update server (reads json for ex: {"version" : 5})')
update_server = QLineEdit()
toggle_server = QPushButton('set server')


#when compiled via pyinstaller search for the icon
if getattr(sys, 'frozen', False):
    if platform.system() == 'Darwin':
        icon_path = join(sys._MEIPASS, 'chromium-mac.icns')
    else:
        icon_path = join(sys._MEIPASS, 'chromium.ico')
else:
    if platform.system() == 'Darwin':
        icon_path = './chromium-mac.icns'
    else:
        icon_path = './chromium.ico'

try_home()
browser = QWebEngineView()
if len(sys.argv) > 1:
    browser.load(QUrl(sys.argv[1]))
else:
    browser.load(QUrl(homepage))
home_browser = tabs.addTab(browser, 'Home')
browser.titleChanged.connect(lambda title, index=home_browser: update_tab_title(index, title))

back_icon = get_icon('back')
home_icon = get_icon('home')
more_icon = get_icon('more')
refresh_icon = get_icon('refresh')
forward_icon = get_icon('forward')
settings_icon = get_icon('settings')
new_tab_icon = get_icon('new-tab')
remove_tab_icon = get_icon('remove-tab')
history_icon = get_icon('history')
extenions_icon = get_icon('extensions')
download_icon = get_icon('download')

back = upper_bar.addAction(back_icon, 'back')
forward = upper_bar.addAction(forward_icon, 'forward')
refresh = upper_bar.addAction(refresh_icon, 'refresh')
home = upper_bar.addAction(home_icon, 'home')
upper_bar.addWidget(search)
more = upper_bar.addAction(more_icon, 'Show/Hide More')



win.setCentralWidget(tabs)
win.addToolBar(upper_bar)



file_menu = QMenu()
file_menu.addAction('New Tab', add_tabs_handler)
file_menu.addAction('Downloads', downloads_handler)
file_menu.addAction('History', history_handler)
file_menu.addAction('Settings', settings_handler)
file_menu.addAction('Extensions', extension_handler)
file_menu.addAction('About', about_handler) 
file_menu.addAction('Exit', app.quit)


browser.urlChanged.connect(history_writer)
search.returnPressed.connect(search_handler)
search.setStyleSheet("""
QLineEdit{
    padding-top:3px;
    padding-left:8px;
    padding-bottom:3px;
    border:2px solid transparent;
    border-radius:6px;
    font-size:11pt;
    background-color: #ffffff;
    selection-background-color: #66c2ff;
    color: black;
}

QLineEdit:focus{
    border-color:#3696ff;
}

QLineEdit:hover{
    border-color:#d6d6d6
}
""")


new_tab_shortcut = QShortcut(QKeySequence('Ctrl+T'), win)
new_tab_shortcut.activated.connect(add_tabs_handler)
refresh_shortcut = QShortcut(QKeySequence('Ctrl+R'), win)
refresh_shortcut.activated.connect(refresh_handler)
downloads_shortcut = QShortcut(QKeySequence('Ctrl+J'), win)
downloads_shortcut.activated.connect(downloads_handler)
history_shortcut = QShortcut(QKeySequence('Ctrl+Y' if sys.platform == "darwin" else 'Ctrl+H'), win)
history_shortcut.activated.connect(history_handler)
remove_tab_shortcut = QShortcut(QKeySequence("Ctrl+W"), win)
remove_tab_shortcut.activated.connect(remove_tab_handler)
exit_shortcut = QShortcut(QKeySequence("Ctrl+Shift+W"), win)
exit_shortcut.activated.connect(lambda: exit())


back.triggered.connect(back_handler)
home.triggered.connect(home_handler)
more.triggered.connect(show_more_menu)
more.setMenu(file_menu)

forward.triggered.connect(forward_handler)
refresh.triggered.connect(refresh_handler)
#view_source.triggered.connect(view_source_handler)

#Download handler
QWebEngineProfile.defaultProfile().downloadRequested.connect(download_handler)

#show the tabs
tabs.show()
tabs.tabCloseRequested.connect(close_current_tab)
tabs.currentChanged.connect(update_current_tab_index)

#sets the icon
app.setWindowIcon(QIcon(icon_path))

#sets the title of the main app
win.setWindowTitle("Py Chromium")

#check the theme if exists
if theme == None:
    pass 
else:
    app.setStyleSheet(theme)

#show the app
win.show()
sys.exit(app.exec_())
