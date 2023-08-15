import sys
import os
from PySide6.QtCore import (QCoreApplication, QSettings, Qt)
from PySide6.QtWidgets import (QApplication, QPushButton, QLabel, QFileDialog,
                               QDialog, QHBoxLayout, QVBoxLayout)
from DirectorySync import DirectorySync


class Ui_Form(QDialog):
    def __init__(self, parent=None):
        super(Ui_Form, self).__init__(parent)
        self.srcPath = [""]
        self.dstPath = [""]
        self.setupUi()
        self.loadSettings()

    def setupUi(self):
        self.resize(600, 300)
        layoutbase = QVBoxLayout()
        self.layout1 = QHBoxLayout()
        self.layout2 = QHBoxLayout()
        self.layout3 = QHBoxLayout()

        self.label1 = QLabel()
        self.label1.setObjectName(u"label1")
        self.label1.setAlignment(Qt.AlignJustify | Qt.AlignCenter)

        self.label2 = QLabel()
        self.label2.setObjectName(u"label2")
        self.label2.setAlignment(Qt.AlignJustify | Qt.AlignCenter)

        self.layout2.addWidget(self.label1)
        self.layout2.addWidget(self.label2)

        self.btn1 = QPushButton("Source Path", self)
        self.btn2 = QPushButton("Destination Path", self)
        self.startBtn = QPushButton("SYNC START", self)

        self.layout1.addWidget(self.btn1)
        self.layout1.addWidget(self.btn2)
        self.layout3.addWidget(self.startBtn)

        layoutbase.addLayout(self.layout1)
        layoutbase.addLayout(self.layout2)
        layoutbase.addLayout(self.layout3)

        # Connect the buttons to the lambda functions to get the directory path
        self.btn1.clicked.connect(
            lambda: self.get_directory_path(self.srcPath, "pathSrc"))
        self.btn2.clicked.connect(
            lambda: self.get_directory_path(self.dstPath, "pathDst"))
        self.startBtn.clicked.connect(self.onStartSync)

        self.setLayout(layoutbase)
        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle(
            QCoreApplication.translate("Form", u"DirectorySynchronizer", None))

    def get_directory_path(self, path: list, setting_key: str):
        directory = QFileDialog.getExistingDirectory(self, "Select a folder:")
        print("dd", directory)
        print("pp", path)
        if directory:  # Check if a directory was selected
            path[0] = directory
            settings = QSettings("AdCream", "DirectorySynchronizer")
            settings.setValue(setting_key, directory)
            settings.setValue("geometry", self.saveGeometry())

        print("log:path ", "src: ", self.srcPath[0], "dst: ", self.dstPath[0])

        self.format_label_text(self.srcPath[0], self.dstPath[0])

    def loadSettings(self):
        # Load the directory paths from QSettings and set them to the labels
        settings = QSettings("AdCream", "DirectorySynchronizer")
        self.srcPath[0] = settings.value("pathSrc", "")
        self.dstPath[0] = settings.value("pathDst", "")
        self.format_label_text(self.srcPath[0], self.dstPath[0])

    def onStartSync(self):
        synchronizer = DirectorySync(self.srcPath[0], self.dstPath[0])
        synchronizer.syncDirectories()

    def format_label_text(self, src_dir: str, dst_dir: str) -> (str, str):
        # Split the paths into parts
        src_parts = src_dir.split(os.sep)
        dst_parts = dst_dir.split(os.sep)

        # Find the common prefix
        common_prefix = os.path.commonprefix([src_parts, dst_parts])
        common_path = os.sep.join(common_prefix)

        # Find the unique tails for each path
        src_unique = os.sep.join(src_parts[len(common_prefix):])
        dst_unique = os.sep.join(dst_parts[len(common_prefix):])

        # Format the paths
        self.label1.setText(common_path + "\n" + src_unique)
        self.label2.setText(common_path + "\n" + dst_unique)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    form = Ui_Form()
    form.show()

    sys.exit(app.exec())
