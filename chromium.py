from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QToolBar, QLineEdit, QFileDialog, QListWidget, QWidget, QRadioButton, QVBoxLayout, QGridLayout, QLabel, QCheckBox, QPushButton, QErrorMessage, QTabWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
import sys
import requests 
import wget
import sqlite3
import os
from os.path import join, exists

if not exists('Pyext'):
    os.makedirs('Pyext')

extensions = []

show = False
ver = 6
tab_num = 0
conn = sqlite3.connect('history.db')
conn.execute('CREATE TABLE IF NOT EXISTS history (history TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS downloads (downloads TEXT)')

def try_home():
    #checks for your current search engine
    global homepage
    try:
        with open('home.stg', 'r') as f:
            homepage = f.read()
    except:
        homepage = "https://google.com/" 

def try_path():
    #checks for the download folder if changed
    global path
    try:
        with open('path.stg', 'r') as f:
            path = f.read()
    except:
        path = None

def try_theme():
    #checks if the theme is set
    global theme
    try:
        with open('theme.stg', 'r') as f:
            theme = f.read()
            if "none" in theme:
                theme = None
    except:
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

def check_update():
    #tries to check for an update on my server (change this to your own check !!!!!)
    global app, win
    try:
        A = requests.post('http://moonpower007.pythonanywhere.com/script/', json={'version': ver})
        version = A.json().get('version')
    except:
        version = 0
    if version > ver:
        msg = QMessageBox()
        msg.setWindowTitle('update handler')
        msg.setText(f'version : {version} is available do you want to update?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg.exec_()
        if result == QMessageBox.Yes:
            wget.download('http://moonpower007.pythonanywhere.com/script/', 'Py Chromium.exe')
            win.hide()
            os.startfile('Py Chromium.exe')
            app.exit()
            exit()
        else:
            pass
    else:
        pass

def search_handler():
    #when you hit enter on the search bar this is the logic behind it.
    browser = tabs.currentWidget()
    url = search.text()
    if '://' in url:
        pass 
    elif '.io' in url or '.net' in url or '.git' in url or '.com' in url or '.org' in url:
        url = f"http://{url}"
    else:
        query = url.replace(" ","+")
        try:
            with open("home.stg", "r") as f:
                if "duckduckgo" in f.read():
                    url = f"{homepage}/?q={query}"
                elif "ecosia" in f.read():
                    url = f"{homepage}/search?q={query}"
                else:
                    url = f"{homepage}/search?q={query}"
        except:
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

def more_handler():
    #toggles between the extended and mini help bar
    global show
    show = True if show == False else False
    upper_bar2.setVisible(show)

def download_handler(dl):
    #when a download signal is caught alerts the user if the user answer is yes download the file to their destination
    global path
    try_path()
    if path:
        path = join(path, dl.path().split('/')[-1])
        dl.setPath(path)
    file = dl.path().split('/')[-1]
    msg = QMessageBox()
    msg.setWindowTitle("Download Handler")
    msg.setText(f"are you sure you want to download {file}?")
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    result = msg.exec()
    if result == QMessageBox.Yes:
        dl.accept()
        conn.execute("INSERT INTO downloads VALUES (?)",(file,))
        conn.commit()
    else:
        pass

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

def engine_picker1():
    with open('home.stg', 'w') as f:
        f.write('https://google.com/')

def engine_picker2():
    with open('home.stg', 'w') as f:
        f.write('https://bing.com/')

def engine_picker3():
    with open('home.stg', 'w') as f:
        f.write('https://duckduckgo.com/')

def engine_picker4():
    with open('home.stg', 'w') as f:
        f.write('https://ecosia.org')

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

def CSP_handler():
    #disbales CSP
    global csp_value
    csp_value = False
    csp_value = not csp_value
    settings = browser.settings()
    settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, csp_value)


def settings_handler():
    #shows the settings and it's layout
    sub.setWindowTitle('Settings')
    
    layout = QVBoxLayout()
    
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
    layout.addWidget(csp_toggle_info)
    layout.addWidget(toggle_csp)
    
    sub.setLayout(layout)
    
    button.clicked.connect(path_picker)
    clear_history.clicked.connect(history_cleaner)
    radio1.clicked.connect(engine_picker1)
    radio2.clicked.connect(engine_picker2)
    radio3.clicked.connect(engine_picker3)
    radio_eco.clicked.connect(engine_picker4)
    radio4.clicked.connect(theme_picker1)
    radio5.clicked.connect(theme_picker2)
    toggle_csp.clicked.connect(CSP_handler)
    
    clear_history.show()
    button.show()

    sub.setFixedSize(300, 500)
    sub.show()


def load_file(file):
    #executes a downloaded file
    try_path()
    file_path = join(path, file.text())
    try:
        os.startfile(file_path)
    except:
        msg_dl.setWindowTitle("Error")
        msg_dl.setText("the application cannot found the specified file at the specified path (the path set in settings)")
        msg_dl.show()

def downloads_handler():
    #shows everything you downloaded
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
    with open(join("Pyext", extension.text()), "rb") as f:
        exec(f.read())
            
def extension_handler():
    #sets every extension as clickable then passes it to extension_loader
    ext_list.setWindowTitle("Extensions")
    for X in extensions:
        ext_list.addItem(X)
    ext_list.itemClicked.connect(extensions_loader)
    ext_list.show()

def add_tabs_handler():
    #adds new tabs !
    global tab_num
    try_home()
    tab_num += 1
    tab = QWebEngineView()
    tab.load(QUrl(homepage))
    tabs.addTab(tab, f"tab {tab_num}")

def remove_tab_handler():
    #removes the current tab the user is on
    tabs.removeTab(tabs.currentIndex())

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
upper_bar2 = QToolBar()
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
csp_toggle_info = QLabel('toggle CSP on/off might fix Bing')
history_info = QLabel('Clear search history')
button = QPushButton('Select folder', win)
clear_history = QPushButton('clear history', win)
toggle_csp = QPushButton('toggle csp', win)
list_dl = QListWidget()
msg_dl = QMessageBox()
ext_list = QListWidget()
tabs = QTabWidget()
button.hide()
clear_history.hide()


#chen compiled via pyinstaller search for the icon
if getattr(sys, 'frozen', False):
    icon_path = join(sys._MEIPASS, 'chromium.ico')
else:
    icon_path = './chromium.ico'

try_home()
browser = QWebEngineView()
browser.load(QUrl(homepage))
home_browser = tabs.addTab(browser, 'home')

upper_bar.addWidget(search)
back = upper_bar.addAction('back')
home = upper_bar.addAction('home')
more = upper_bar.addAction('more')
win.setCentralWidget(tabs)
win.addToolBar(upper_bar)
win.addToolBar(upper_bar2)
upper_bar2.hide()

forward = upper_bar2.addAction('forward')
refresh = upper_bar2.addAction('refresh')
history = upper_bar2.addAction('history')
settings = upper_bar2.addAction('settings')
downloads = upper_bar2.addAction('downloads')
add_tabs = upper_bar2.addAction('new tab')
remove_tab = upper_bar2.addAction('remove current tab')
extenions = upper_bar2.addAction('extenstions')

browser.urlChanged.connect(history_writer)
search.returnPressed.connect(search_handler)
search.setStyleSheet('border-radius:7px; border:1px solid;')
back.triggered.connect(back_handler)
home.triggered.connect(home_handler)
more.triggered.connect(more_handler)

history.triggered.connect(history_handler)
settings.triggered.connect(settings_handler)
downloads.triggered.connect(downloads_handler)
forward.triggered.connect(forward_handler)
refresh.triggered.connect(refresh_handler)
extenions.triggered.connect(extension_handler)
add_tabs.triggered.connect(add_tabs_handler)
remove_tab.triggered.connect(remove_tab_handler)

#download handler
QWebEngineProfile.defaultProfile().downloadRequested.connect(download_handler)

#show the tabs
tabs.show()

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