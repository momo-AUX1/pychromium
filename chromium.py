import PyQt5
import PyQt5.sip
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QToolBar, QLineEdit, QFileDialog, QListWidget, QWidget, QRadioButton, QVBoxLayout, QGridLayout, QLabel, QCheckBox, QPushButton, QErrorMessage, QTabWidget, QTextEdit, QMenu, QDialog, QTextBrowser
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import QUrl
import sys
import requests 
import wget
import sqlite3
import os
from os.path import join, exists
import platform


#checks if the Pyext folder exists if not it makes one
if not exists('Pyext'):
    os.makedirs('Pyext')

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

show = False
ver = 12
tab_num = 0
checked_extensions = False
current_tab_index = -1  


valid_url_suffixes = [
    '.com', '.org', '.net', '.io', '.ai', '.co', '.edu', '.gov',
    '.uk', '.ru', '.in', '.de', '.fr', '.jp', '.nl', '.it', '.br', '.pl', '.ir',
    '.es', '.au', '.biz', '.info', '.me', '.tv', '.cc', '.cn', '.eu', '.xyz',
    '.site', '.online', '.us', '.ca', '.git', '.web', '.app', '.blog', '.shop',
    '.club', '.space', '.link', '.tech', '.dev', '.wiki', '.agency', '.email',
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

def server_handler():
    #sets the server url for the update
    server_url = update_server.text()
    with open("server.stg", "w") as f:
        f.write(server_url)

def check_update():
    #tries to check for an update 
    global app, win
    try:
        server = open("server.stg").read()
        A = requests.post(server, json={'version': ver})
        version = A.json().get('version')
    except:
        version = 0

    if version > ver:
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
                    os.startfile('Py Chromium.exe')
                    app.exit()
                    exit()
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
                    os.startfile('Py Chromium.app')
                    app.exit()
                    exit()
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
    
    # Check if the entered text is a URL
    if '://' in url or any(url.endswith(suffix) for suffix in valid_url_suffixes):
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

def show_more_menu():
    file_menu.exec_(QCursor.pos())

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
        os.startfile(file_path)
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
    with open(join("Pyext", extension.text()), "rb") as f:
        exec(f.read())
            
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
    about_text.setHtml("""
    <h1>Py Chromium</h1>
    <p><strong>Version:</strong> 1.2.0</p>
    <p>A lightweight web browser built with Python and PyQt.</p>
    <p><strong>© Mohammed 2024</strong></p>
    <p>Powered by:</p>
    <ul>
        <li>Python 3 - <a href="https://www.python.org/">https://www.python.org/</a></li>
        <li>PyQt5 (Qt) - <a href="https://www.riverbankcomputing.com/software/pyqt/">https://www.riverbankcomputing.com/software/pyqt/</a></li>
        <li>Chromium - <a href="https://www.chromium.org/">https://www.chromium.org/</a></li>
        <li>SQLite - <a href="https://www.sqlite.org/">https://www.sqlite.org/</a></li>
        <li>Requests - <a href="https://requests.readthedocs.io/en/master/">https://requests.readthedocs.io/en/master/</a></li>
        <li>Wget - <a href="https://www.gnu.org/software/wget/">https://www.gnu.org/software/wget/</a></li>
    </ul>
    <p>All product names, logos, and brands are property of their respective owners. Use of these names, logos, and brands does not imply endorsement.</p>
    """)
    layout.addWidget(about_text)
    close_button = QPushButton('Close')
    close_button.clicked.connect(dialog.close)
    layout.addWidget(close_button)
    dialog.exec_()


def close_current_tab(index):
    tabs.removeTab(index)

#### VIEW SOURCE UNDER CONSTRUCTION ####

#def view_source_handler():
#    browser = tabs.currentWidget()
#    browser.page().toHtml(view_source_callback)

#def view_source_callback(html):
#    source_tab = QTextEdit()
#    source_tab.setPlainText(html)
#    tab_index = tabs.addTab(source_tab, "Source")
#    tabs.setCurrentIndex(tab_index)

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
button = QPushButton('Select folder')
clear_history = QPushButton('Clear history')
toggle_csp = QPushButton('Toggle csp')
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

upper_bar.addWidget(search)


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
home = upper_bar.addAction(home_icon, 'home')
more = upper_bar.addAction(more_icon, 'Show/Hide More')

win.setCentralWidget(tabs)
win.addToolBar(upper_bar)
win.addToolBar(upper_bar2)
upper_bar2.hide()

forward = upper_bar2.addAction(forward_icon, 'forward')
refresh = upper_bar2.addAction(refresh_icon, 'refresh')
history = upper_bar2.addAction(history_icon, 'history')
settings = upper_bar2.addAction(settings_icon, 'settings')
downloads = upper_bar2.addAction(download_icon, 'downloads')
add_tabs = upper_bar2.addAction(new_tab_icon, 'new tab')
#remove_tab = upper_bar2.addAction(remove_tab_icon, 'remove current tab')
extenions = upper_bar2.addAction(extenions_icon, 'extenstions')



file_menu = QMenu()
file_menu.addAction('Forward', forward_handler)
file_menu.addAction('Refresh', refresh_handler)
file_menu.addAction('New Tab', add_tabs_handler)
file_menu.addAction('Downloads', downloads_handler)
file_menu.addAction('History', history_handler)
file_menu.addAction('Settings', settings_handler)
file_menu.addAction('Extensions', extension_handler)
file_menu.addAction('About', about_handler) 
file_menu.addAction('Exit', app.quit)



#view_source = upper_bar2.addAction('View Source')


browser.urlChanged.connect(history_writer)
search.returnPressed.connect(search_handler)
search.setStyleSheet('border-radius:7px; border:1px solid;')
back.triggered.connect(back_handler)
home.triggered.connect(home_handler)
more.triggered.connect(show_more_menu)
more.setMenu(file_menu)

history.triggered.connect(history_handler)
settings.triggered.connect(settings_handler)
downloads.triggered.connect(downloads_handler)
forward.triggered.connect(forward_handler)
refresh.triggered.connect(refresh_handler)
extenions.triggered.connect(extension_handler)
add_tabs.triggered.connect(add_tabs_handler)
#remove_tab.triggered.connect(remove_tab_handler)
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
