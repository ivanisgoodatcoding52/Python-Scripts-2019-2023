+we3import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser_tabs = QTabWidget()
        self.browser_tabs.setDocumentMode(True)
        self.browser_tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.browser_tabs.currentChanged.connect(self.current_tab_changed)
        self.browser_tabs.setTabsClosable(True)
        self.browser_tabs.tabCloseRequested.connect(self.close_current_tab)
        
        self.setCentralWidget(self.browser_tabs)
        self.statusBar()

        # Navigation bar
        navbar = QToolBar("Navigation")
        self.addToolBar(navbar)

        # New Tab button
        new_tab_btn = QAction("New Tab", self)
        new_tab_btn.triggered.connect(lambda: self.add_new_tab(set_current=False))
        navbar.addAction(new_tab_btn)

        # Back button
        back_btn = QAction("Back", self)
        back_btn.triggered.connect(lambda: self.browser_tabs.currentWidget().back())
        navbar.addAction(back_btn)

        # Forward button
        forward_btn = QAction("Forward", self)
        forward_btn.triggered.connect(lambda: self.browser_tabs.currentWidget().forward())
        navbar.addAction(forward_btn)

        # Reload button
        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(lambda: self.browser_tabs.currentWidget().reload())
        navbar.addAction(reload_btn)

        # Home button
        home_btn = QAction("Home", self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        # Inspect Element button
        inspect_btn = QAction("Inspect Element", self)
        inspect_btn.triggered.connect(self.inspect_element)
        navbar.addAction(inspect_btn)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        # Bookmarks bar
        self.bookmarks_bar = QToolBar("Bookmarks")
        self.addToolBar(Qt.TopToolBarArea, self.bookmarks_bar)

        # Sample bookmarks (add your own here)
        self.add_bookmark("Google", "http://www.google.com")
        self.add_bookmark("YouTube", "http://www.youtube.com")
        self.add_bookmark("Python", "http://www.python.org")

        self.browser_tabs.currentChanged.connect(self.update_url_bar)

        # Add a new tab
        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')

        self.showMaximized()

    def add_new_tab(self, qurl=None, label="Blank", set_current=True):
        if qurl is None:
            qurl = QUrl('')

        browser = QWebEngineView()
        browser.setUrl(qurl)

        # Enable developer tools
        page = QWebEnginePage()
        browser.setPage(page)
        page.setView(browser)

        i = self.browser_tabs.addTab(browser, label)
        if set_current:
            self.browser_tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_url(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.browser_tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.browser_tabs.currentWidget().url()
        self.update_url_bar(qurl, self.browser_tabs.currentWidget())
    
    def close_current_tab(self, i):
        if self.browser_tabs.count() < 2:
            return

        self.browser_tabs.removeTab(i)

    def navigate_home(self):
        self.browser_tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser_tabs.currentWidget().setUrl(QUrl(url))

    def update_url(self, qurl, browser=None):
        if browser != self.browser_tabs.currentWidget():
            return
        self.url_bar.setText(qurl.toString())

    def update_url_bar(self, qurl, browser=None):
        qurl = self.browser_tabs.currentWidget().url()
        self.url_bar.setText(qurl.toString())
        self.url_bar.setCursorPosition(0)

    def add_bookmark(self, name, url):
        bookmark_btn = QAction(name, self)
        bookmark_btn.triggered.connect(lambda: self.browser_tabs.currentWidget().setUrl(QUrl(url)))
        self.bookmarks_bar.addAction(bookmark_btn)

    def inspect_element(self):
        current_tab = self.browser_tabs.currentWidget()
        page = current_tab.page()
        page.setDevToolsPage(QWebEnginePage())
        dev_tools = QWebEngineView()
        dev_tools.setPage(page.devToolsPage())
        dev_tools.show()

app = QApplication(sys.argv)
QApplication.setApplicationName("My Browser")
window = Browser()
app.exec_()
