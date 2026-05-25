import os
import sys
import ctypes
import time
from PyQt6.QtCore import QUrl, pyqtSlot, QObject, QThread, pyqtSignal, QSettings
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtWebEngineWidgets import QWebEngineView 
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtGui import QIcon

# Presentation Engine Import
try:
    from ppt_engine import generate_ppt
except ImportError:
    def generate_ppt(query, save_dir=None):
        return "Success|Mock_Presentation.pptx"

class PPTWorker(QThread):
    result_ready = pyqtSignal(str)
    def __init__(self, song_query, save_directory):
        super().__init__()
        self.song_query = song_query
        self.save_directory = save_directory
    
    def run(self):
        start_time = time.time()
        try:
            path = generate_ppt(self.song_query, self.save_directory)
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            self.result_ready.emit(f"Success|{path}|{duration}")
        except Exception as err:
            self.result_ready.emit(f"Error|{str(err)}")

class BackendBridge(QObject):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

    @pyqtSlot()
    def open_settings_window(self):
        pass

    @pyqtSlot(str)
    def save_custom_path_direct(self, path):
        self.main_window.save_custom_path_direct(path)

    @pyqtSlot(result=str)
    def get_initial_path(self):
        return self.main_window.save_directory.replace(chr(92), '/')

    @pyqtSlot()
    def trigger_folder_picker(self):
        self.main_window.trigger_folder_picker()

    @pyqtSlot(str)
    def generate_lyrics(self, query):
        self.main_window.generate_lyrics(query)

class HeisenbergWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Heisenberg 2.0 (beta)")
        self.resize(840, 720)
        
        # --- PATH RESOLUTION ---
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        
        # --- QSettings Setup ---
        # This stores settings in the Windows Registry automatically
        self.settings = QSettings("HeisenbergOrg", "Heisenberg2.0")
        self.save_directory = self.settings.value("save_directory", os.path.expanduser("~"))

        # UI Setup
        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)
        
        profile = self.web_view.page().profile()
        profile.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)
        profile.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        
        self.channel = QWebChannel()
        self.bridge = BackendBridge(self)
        self.channel.registerObject("py_backend", self.bridge)
        self.web_view.page().setWebChannel(self.channel)

        # Loading paths
        web_url = QUrl.fromLocalFile(os.path.join(base_dir, "web", "index.html"))
        self.web_view.setUrl(web_url)
        
        # Icon setup
        icon_path = os.path.join(base_dir, "web", "Assets", "favicon.ico")
        self.setWindowIcon(QIcon(icon_path))

    def save_custom_path_direct(self, path):
        self.save_directory = path
        self.settings.setValue("save_directory", path)

    def trigger_folder_picker(self):
        selected = QFileDialog.getExistingDirectory(self, "Select Folder")
        if selected:
            self.save_custom_path_direct(selected)
            escaped = selected.replace(chr(92), '/')
            self.web_view.page().runJavaScript(f"window.updateTargetPathDisplay('{escaped}')")

    def generate_lyrics(self, query):
        self.worker = PPTWorker(query, self.save_directory)
        self.worker.result_ready.connect(self.on_generation_completed)
        self.worker.start()

    def on_generation_completed(self, payload):
        ui_message = payload
        if payload.startswith("Success"):
            parts = payload.split('|')
            full_path = parts[1]
            duration = parts[2]
            filename = os.path.basename(full_path)
            
            # Auto-open logic
            if os.path.exists(full_path) and sys.platform == "win32":
                os.startfile(full_path)
            
            ui_message = f"Success : Generated PPT saved as {filename}. PPT Generated in {duration} seconds."
            
        
        # --- ROBUST SANITIZATION ---
        # 1. Escape backslashes first
        # 2. Escape single quotes
        # 3. Remove newlines to prevent JS breaking
        clean_msg = ui_message.replace('\\', '\\\\').replace("'", "\\'").replace('\n', ' ')
        
        # Execute using a JSON-safe string approach
        js_code = f"window.handleBackendResponse('{clean_msg}');"
        self.web_view.page().runJavaScript(js_code)

if __name__ == "__main__":
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('heisenberg.version1')
    app = QApplication(sys.argv)
    window = HeisenbergWindow()
    window.show()
    sys.exit(app.exec())