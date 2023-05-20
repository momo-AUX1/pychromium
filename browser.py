from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QToolBar, QLineEdit, QFileDialog, QListWidget, QWidget, QRadioButton, QVBoxLayout, QGridLayout, QLabel, QCheckBox, QPushButton, QErrorMessage
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
ver = 2

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
    A = requests.post('http://moonpower007.pythonanywhere.com/script/', json={'version': ver})
    version = A.json().get('version')
    if version > ver:
        msg = QMessageBox()
        msg.setWindowTitle('update handler')
        msg.setText(f'version : {version} is available do you want to update?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg.exec_()
        if result == QMessageBox.Yes:
            wget.download('http://moonpower007.pythonanywhere.com/script/', 'main.py')
            print('run main.py')
            exit()
        else:
            pass
    else:
        pass

def search_handler():
    url = search.text()
    if '://' in url:
        pass 
    elif '.io' in url or '.net' in url or '.git' in url or '.com' in url or '.org' in url:
        url = f"http://{url}"
    else:
        query = url.replace("","+")
        url = f"{homepage}/search?q={query}"
    browser.setUrl(QUrl(url))

def home_handler():
    try_home()
    browser.setUrl(QUrl(homepage))

def back_handler():
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
    browser.setUrl(QUrl(url))

def history_handler():
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


def settings_handler():
    sub.setWindowTitle('Settings')
    box.addWidget(setting_info, 0, 0)
    box.addWidget(radio1, 1,0)
    box.addWidget(radio2, 1,1)
    box.addWidget(download_info, 2,0)
    box.addWidget(button, 3,0)
    sub.setLayout(box)
    button.clicked.connect(path_picker)
    radio1.clicked.connect(engine_picker1)
    radio2.clicked.connect(engine_picker2)
    button.show()
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
    browser.forward()

def refresh_handler():
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
    


app = QApplication(sys.argv)
check_update()
check_extensions()
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
setting_info = QLabel('Choose preferred engine')
download_info = QLabel('Choose preferred download folder')
button = QPushButton('Select folder', win)
list_dl = QListWidget()
msg_dl = QMessageBox()
ext_list = QListWidget()
button.hide()


try_home()
browser.load(QUrl(homepage))
upper_bar.addWidget(search)
back = upper_bar.addAction('back')
home = upper_bar.addAction('home')
more = upper_bar.addAction('more')
win.setCentralWidget(browser)
win.addToolBar(upper_bar)
win.addToolBar(upper_bar2)
upper_bar2.hide()

forward = upper_bar2.addAction('forward')
refresh = upper_bar2.addAction('refresh')
history = upper_bar2.addAction('history')
settings = upper_bar2.addAction('settings')
downloads = upper_bar2.addAction('downloads')
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


QWebEngineProfile.defaultProfile().downloadRequested.connect(download_handler)

win.show()
sys.exit(app.exec_())