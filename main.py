import sys
from PySide6.QtWidgets import QApplication
from ui import MainWindow
from worker import VideoWorker

def main():
    app = QApplication(sys.argv)
    worker = VideoWorker()
    window = MainWindow()
    window.set_worker(worker)
    window.show()
    worker.start()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()