import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

class VideoPlayerApp(QMainWindow):
    def __init__(self, video_path):
        super().__init__()

        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.web_engine_view = QWebEngineView(self.central_widget)
        self.layout.addWidget(self.web_engine_view)

        # Set a dark theme for the web engine view
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.web_engine_view.page().setPalette(palette)

        self.web_engine_view.setUrl(QUrl.fromLocalFile(video_path))

def main():
    app = QApplication(sys.argv)

    # Replace 'path_to_your_video_file.mp4' with the actual path to your video file
    video_path = "path_to_your_video_file.mp4"

    window = VideoPlayerApp(video_path)
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
