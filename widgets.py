import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QDialog, QLineEdit, QTableView, QFileDialog
from PyQt5 import QtGui
from PyQt5.QtSql import QSqlTableModel
from utils import read_json, write_json, anonymize_dir
from uploader import clear_all_pacs, upload_to_pacs


class UploadDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.all_pacs = read_json('pacs.json')

    def _get_dict_info_as_str(self):
        stri = ''
        for k,v in self.all_pacs.items():
            stri = stri + k + ' : ' + v + '\n'
        return stri

    def initUI(self):
        d_grid = QGridLayout()
        d_grid.setSpacing(10)
        self.setLayout(d_grid)
        self.setGeometry(300, 300, 550, 350)

        self.upload_button = QPushButton("Upload",self)
        self.clear_button = QPushButton("Clear",self)
        self.path_label = QLabel('Your selected folder:', self)
        self.pacs_label = QLabel(self._get_dict_info_as_str(), self)
        self.path_input = QLineEdit('Please Select the Folder to Upload', self)
        self.close_button = QPushButton("Close",self)
        qfd = QFileDialog()
        qfd.setFileMode(4)
        self.path_input.setText(qfd.getExistingDirectory())
        d_grid.addWidget(self.path_label, 0, 0, Qt.AlignTop)
        d_grid.addWidget(self.path_input, 1, 0, Qt.AlignTop) 
        d_grid.addWidget(self.pacs_label, 2, 0, Qt.AlignTop) 
        d_grid.addWidget(self.upload_button, 3, 0, Qt.AlignBottom) 
        d_grid.addWidget(self.close_button, 3, 2, Qt.AlignBottom)
        d_grid.addWidget(self.clear_button, 3, 1, Qt.AlignBottom)
        self.upload_button.clicked.connect(self.upload_event) 
        self.close_button.clicked.connect(self.close_dialog) 
        self.clear_button.clicked.connect(self.clear_event) 
        self.setWindowTitle("Upload to Pacs")
        self.setWindowModality(Qt.ApplicationModal)
        self.exec_()

    def upload_event(self):
        upload_to_pacs(self.path_input.text())

    def clear_event(self):
        clear_all_pacs()

    def close_dialog(self): 
        self.close()

class AnonymizeUploadDialog(UploadDialog):
    def __init__(self):
        super().__init__()
        self.all_pacs = read_json('pacs.json')

    def upload_event(self):
        anonymized_dcms = anonymize_dir(self.path_input.text())
        upload_to_pacs(self.path_input.text(), anonymize=True)
        for dcm in anonymized_dcms:
            os.remove(dcm)


class ConfigDialog(QDialog):
    def __init__(self):
        self.all_pacs = {}
        super().__init__()

    def _get_dict_info_as_str(self):
        stri = ''
        for k,v in self.all_pacs.items():
            stri = stri + k + ' : ' + v + '\n'
        return stri

    def initUI(self):
        d_grid = QGridLayout()
        d_grid.setSpacing(10)
        self.setLayout(d_grid)
        self.setGeometry(300, 300, 550, 350)
        self.add_button = QPushButton("Add",self)
        self.host_label = QLabel('Host:', self)
        self.host_input = QLineEdit('localhost', self)
        # self.host_input = QLineEdit('192.168.1.102', self)
        self.port_label = QLabel('Port:', self)
        self.port_input = QLineEdit('8042', self)
        self.show_all   = QLabel('Please Enter the Configs of Pacs',self)
        d_grid.addWidget(self.add_button, 0, 0, Qt.AlignTop)
        d_grid.addWidget(self.host_label, 0, 1, Qt.AlignTop)
        d_grid.addWidget(self.host_input, 0, 2, Qt.AlignTop)
        d_grid.addWidget(self.port_label, 0, 3, Qt.AlignTop)
        d_grid.addWidget(self.port_input, 0, 4, Qt.AlignTop)
        d_grid.addWidget(self.show_all, 1, 0, Qt.AlignTop)

        self.add_button.clicked.connect(self.add_line)

        self.setWindowTitle("Config Pacs")
        self.setWindowModality(Qt.ApplicationModal)
        self.exec_()

    def add_line(self):
        self.all_pacs[self.host_input.text()] = self.port_input.text()
        self.show_all.setText(self._get_dict_info_as_str())
        write_json(self.all_pacs, os.path.join(os.getcwd(), 'pacs.json'))

    def get__all_pacs(self):
        return self.all_pacs
        
class MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        
        #Grid Layout
        grid = QGridLayout()
        grid.setSpacing(10)
        #Local Posion Label
        self.greeting_label = QLabel('Hallo Herr', self)
        grid.addWidget(self.greeting_label, 0, 0, Qt.AlignTop)

        self.config_button = QPushButton('Config')
        self.config_button.clicked.connect(self.pop_config_dialog)
        grid.addWidget(self.config_button, 1, 0, Qt.AlignBottom)  

        self.upload_button = QPushButton('Upload')
        self.upload_button.clicked.connect(self.pop_upload_dialog)
        grid.addWidget(self.upload_button, 1, 1, Qt.AlignBottom)

        self.upload_button = QPushButton('Anonymous Upload')
        self.upload_button.clicked.connect(self.pop_upload_anonymize_dialog)
        grid.addWidget(self.upload_button, 1, 2, Qt.AlignBottom)

        self.setLayout(grid)
        self.setGeometry(300, 300, 350, 100)
        self.setWindowTitle('Uploader')
        self.show()

    def pop_config_dialog(self):
        config_dialog = ConfigDialog()
        config_dialog.initUI()

    def pop_upload_dialog(self):
        upload_dialog = UploadDialog()
        upload_dialog.initUI()

    def pop_upload_anonymize_dialog(self):
        upload_dialog = AnonymizeUploadDialog()
        upload_dialog.initUI()
