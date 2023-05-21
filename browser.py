from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
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
ver = 4 #changr this to match your version
tab_num = 0
conn = sqlite3.connect('history.db')
conn.execute('CREATE TABLE IF NOT EXISTS history (history TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS downloads (downloads TEXT)')

def try_home():
    global homepage
    try:
        with open('home.stg', 'r') as f:
            homepage = f.read()
    except:
        homepage = "https://google.com/" 

def try_path():
    global path
    try:
        with open('path.stg', 'r') as f:
            path = f.read()
    except:
        path = None

def try_theme():
    global theme
    try:
        with open('theme.stg', 'r') as f:
            theme = f.read()
            if "none" in theme:
                theme = None
    except:
        theme = None


def check_extensions():
    try:
        A = os.listdir('Pyext')
        for element in A:
            if '.py' in element or '.ext' in element:
                extensions.append(element)
                sys.path.append(f"Pyext/{element}")        
    except:
        pass

def check_update():
    global app, win
    A = requests.post('http://moonpower007.pythonanywhere.com/script/', json={'version': ver}) #change this to match your server
    version = A.json().get('version')
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
    browser = tabs.currentWidget()
    url = search.text()
    if '://' in url:
        pass 
    elif '.io' in url or '.net' in url or '.git' in url or '.com' in url or '.org' in url:
        url = f"http://{url}"
    else:
        query = url.replace(" ","+")
        with open("home.stg", "r") as f:
            home = f.read()
            if "duckduckgo" in home:
                url = f"{homepage}/?q={query}"
            else:
                url = f"{homepage}/search?q={query}"
    browser.setUrl(QUrl(url))

def home_handler():
    try_home()
    browser = tabs.currentWidget()
    browser.setUrl(QUrl(homepage))

def back_handler():
    browser = tabs.currentWidget()
    browser.back()

def more_handler():
    global show
    if show == True:
        show = False
    else:
        show = True
    upper_bar2.setVisible(show)

def download_handler(dl):
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
    current_url = browser.url().toString()
    search.setText(current_url)
    conn.execute("INSERT INTO history VALUES (?)", (current_url,))
    conn.commit()

def go_to_link(url):
    url = url.text()
    browser = tabs.currentWidget()
    browser.setUrl(QUrl(url))

def history_handler():
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
        f.write('https://www.ecosia.org')

def theme_picker1():
    with open('theme.stg', 'w') as f:
        f.write('none')

def theme_picker2():
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
    conn.execute("DROP TABLE IF EXISTS history")
    conn.commit()


def settings_handler():
    sub.setWindowTitle('Settings')

    box.addWidget(download_info, 4,0)
    box.addWidget(button, 5,0)
    box.addWidget(history_info, 6,0)
    box.addWidget(clear_history, 7,0)
    sub.setLayout(box)
    button.clicked.connect(path_picker)
    clear_history.clicked.connect(history_cleaner)
    clear_history.show()
    button.show()
    sub.setFixedSize(350,150)
    sub.show()

def load_file(file):
    try_path()
    file_path = join(path, file.text())
    try:
        os.startfile(file_path)
    except:
        msg_dl.setWindowTitle("Error")
        msg_dl.setText("the application cannot found the specified file at the specified path (the path set in settings)")
        msg_dl.show()

def downloads_handler():
    list_dl.clear()
    all_dl = conn.execute("SELECT * FROM downloads").fetchall()
    for dl in all_dl:
        list_dl.addItem(dl[0])
    list_dl.itemClicked.connect(load_file)
    list_dl.show()

def forward_handler():
    browser = tabs.currentWidget()
    browser.forward()

def refresh_handler():
    browser = tabs.currentWidget()
    browser.reload()

def extensions_loader(extension):
    with open(join("Pyext", extension.text()), "rb") as f:
        exec(f.read())
            
def extension_handler():
    ext_list.setWindowTitle("Extensions")
    for X in extensions:
        ext_list.addItem(X)
    ext_list.itemClicked.connect(extensions_loader)
    ext_list.show()

def add_tabs_handler():
    global tab_num
    try_home()
    tab_num += 1
    tab = QWebEngineView()
    tab.load(QUrl(homepage))
    tabs.addTab(tab, f"tab {tab_num}")

def remove_tab_handler():
    tabs.removeTab(tabs.currentIndex())


app = QApplication(sys.argv)
check_update()
check_extensions()
try_theme()
win = QMainWindow()
browser = QWebEngineView()
upper_bar = QToolBar()
upper_bar2 = QToolBar()
search = QLineEdit()
list = QListWidget()
sub = QWidget()
box = QGridLayout()
download_info = QLabel('Choose preferred download folder')
history_info = QLabel('Clear search history')
button = QPushButton('Select folder', win)
clear_history = QPushButton('clear history', win)
list_dl = QListWidget()
msg_dl = QMessageBox()
ext_list = QListWidget()
tabs = QTabWidget()
button.hide()
clear_history.hide()


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


QWebEngineProfile.defaultProfile().downloadRequested.connect(download_handler)
tabs.show()
app.setWindowIcon(QIcon(icon_path))
win.setWindowTitle("Py Chromium")
if theme == None:
    pass 
else:
    app.setStyleSheet(theme)
win.show()
sys.exit(app.exec_())
