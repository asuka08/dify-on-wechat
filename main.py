import os.path
import sys
import json
import logging
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFormLayout, QDialog, \
    QDialogButtonBox, QMessageBox, QScrollArea, QWidget, QComboBox, QRadioButton, QButtonGroup, QSpinBox, QFileDialog, QApplication
from PyQt6.QtCore import pyqtSignal, QObject, Qt, QThread
from qt_material import apply_stylesheet
from common.log import logger  # 导入 logger
import app  # 导入 app.py
import time
from config import conf
from common.utils import resource_path


class LogHandler(logging.Handler):
    def __init__(self, signal):
        super().__init__()
        self.signal = signal

    def emit(self, record):
        log_entry = self.format(record)
        self.signal.emit(log_entry)


class Worker(QObject):
    data_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            app.run()  # 直接调用 app.py 中的 run 函数
        except Exception as e:
            self.error_occurred.emit(str(e))


class ArrayInputDialog(QDialog):
    def __init__(self, title, items=None):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(400, 200, 400, 300)
        self.layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()
        self.text_inputs = []

        self.add_button = QPushButton('添加项')
        self.add_button.clicked.connect(self.add_input)
        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.add_button)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

        if items:
            for item in items:
                self.add_input(item)

    def add_input(self, text=''):
        item_layout = QHBoxLayout()
        line_edit = QLineEdit(self)
        line_edit.setText(str(text))
        remove_button = QPushButton('删除', self)
        remove_button.clicked.connect(lambda: self.remove_input(item_layout))

        item_layout.addWidget(line_edit)
        item_layout.addWidget(remove_button)
        self.text_inputs.append((line_edit, item_layout))

        self.form_layout.addRow(f'Item {len(self.text_inputs)}:', item_layout)

    def remove_input(self, item_layout):
        for line_edit, layout in self.text_inputs:
            if layout == item_layout:
                self.text_inputs.remove((line_edit, layout))
                break
        for i in reversed(range(item_layout.count())):
            widget = item_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.form_layout.removeRow(item_layout)

    def get_items(self):
        return [line_edit.text() for line_edit, _ in self.text_inputs]


class ConfigDialog(QDialog):
    def __init__(self, config_path):
        super().__init__()
        self.config_path = config_path
        self.initUI()

    def initUI(self):
        self.setWindowTitle('修改配置')
        self.setGeometry(400, 200, 800, 600)  # 增加窗口大小

        self.layout = QVBoxLayout(self)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QFormLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)
        self.text_inputs = {}

        # Load config
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except Exception as e:
            logger.exception(e)
            QMessageBox.critical(self, "错误", f"加载配置时出错: {e}")
            self.close()

        # Create text inputs for each config item
        for key, value in self.config.items():
            self.add_config_item(key, value)

        # Add new config item button
        self.add_button = QPushButton('添加配置项', self)
        self.add_button.clicked.connect(self.add_new_config_item)
        self.layout.addWidget(self.add_button)

        # # Import and Export buttons
        # self.import_button = QPushButton('导入配置', self)
        # self.import_button.clicked.connect(self.import_config)
        # self.layout.addWidget(self.import_button)
        #
        # self.export_button = QPushButton('导出配置', self)
        # self.export_button.clicked.connect(self.export_config)
        # self.layout.addWidget(self.export_button)

        # Dialog buttons
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel, self)
        self.button_box.accepted.connect(self.save_config)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

    def add_config_item(self, key, value):
        h_layout = QHBoxLayout()
        if isinstance(value, list):
            button = QPushButton(f'{key} (编辑列表)', self)
            button.clicked.connect(lambda _, k=key, v=value: self.edit_list(k, v))
            h_layout.addWidget(button)
        else:
            widget = None
            if isinstance(value, bool):
                widget = QWidget(self)
                layout = QHBoxLayout(widget)
                true_radio = QRadioButton('是')
                false_radio = QRadioButton('否')
                if value:
                    true_radio.setChecked(True)
                else:
                    false_radio.setChecked(True)
                button_group = QButtonGroup(widget)
                button_group.addButton(true_radio)
                button_group.addButton(false_radio)
                layout.addWidget(true_radio)
                layout.addWidget(false_radio)
                self.text_inputs[key] = button_group
                h_layout.addWidget(widget)
            elif isinstance(value, int):
                widget = QSpinBox(self)
                widget.setValue(value)
                self.text_inputs[key] = widget
                h_layout.addWidget(widget)
            else:
                widget = QLineEdit(self)
                widget.setText(str(value))
                widget.setMinimumWidth(400)
                self.text_inputs[key] = widget
                h_layout.addWidget(widget)

        # remove_button = QPushButton('x', self)
        # remove_button.setProperty('class', 'danger')
        # remove_button.clicked.connect(lambda _, k=key: self.remove_config_item(k))
        # h_layout.addWidget(remove_button)

        self.scroll_layout.addRow(QLabel(key), h_layout)

    def remove_config_item(self, key):
        if key in self.text_inputs:
            widget = self.text_inputs.pop(key)
            widget.deleteLater()
        else:
            items = self.scroll_layout.findChildren(QPushButton, key)
            if items:
                items[0].deleteLater()
                items[1].deleteLater()

    def edit_list(self, key, items):
        dialog = ArrayInputDialog(key, items)
        if dialog.exec():
            self.config[key] = dialog.get_items()

    def save_config(self):
        try:
            for key, widget in self.text_inputs.items():
                if isinstance(widget, QButtonGroup):
                    self.config[key] = widget.buttons()[0].isChecked()
                elif isinstance(widget, QSpinBox):
                    self.config[key] = widget.value()
                elif isinstance(widget, QLineEdit):
                    self.config[key] = widget.text()

            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)

            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存配置时出错: {e}")

    def add_new_config_item(self):
        dialog = NewConfigItemDialog(self)
        if dialog.exec():
            key, value = dialog.get_item()
            self.config[key] = value
            self.add_config_item(key, value)

    def import_config(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "导入配置文件", "", "JSON 文件 (*.json);;所有文件 (*)")
        if file_name:
            try:
                with open(file_name, 'r') as f:
                    imported_config = json.load(f)
                self.config.update(imported_config)
                self.initUI()  # Refresh the UI
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导入配置时出错: {e}")

    def export_config(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "导出配置文件", "", "JSON 文件 (*.json);;所有文件 (*)")
        if file_name:
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    current_config = json.load(f)
                with open(file_name, 'w', encoding='utf-8') as f:
                    json.dump(current_config, f, ensure_ascii=False, indent=4)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出配置时出错: {e}")


class NewConfigItemDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('添加新配置项')
        self.setGeometry(400, 200, 400, 200)
        self.layout = QVBoxLayout(self)

        self.key_edit = QLineEdit(self)
        self.value_edit = QLineEdit(self)
        self.type_combo = QComboBox(self)
        self.type_combo.addItems(['字符串', '整数', '布尔值', '字符串列表'])
        self.layout.addWidget(QLabel('键:'))
        self.layout.addWidget(self.key_edit)
        self.layout.addWidget(QLabel('值:'))
        self.layout.addWidget(self.value_edit)
        self.layout.addWidget(QLabel('类型:'))
        self.layout.addWidget(self.type_combo)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def get_item(self):
        key = self.key_edit.text()
        value = self.value_edit.text()
        type_ = self.type_combo.currentText()
        if type_ == '整数':
            value = int(value)
        elif type_ == '布尔值':
            value = value.lower() == 'true'
        elif type_ == '字符串列表':
            value = [value]
        return key, value


class ConfigEditor(QtWidgets.QWidget):
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()
        self.config_path = "config.json"
        self.worker = None
        self.thread = None

        self.log_handler = LogHandler(self.log_signal)
        self.log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(self.log_handler)
        logger.setLevel(logging.INFO)

        self.log_signal.connect(self.update_output)

    def closeEvent(self, event):
        # 阻止窗口立即关闭
        event.ignore()

        # 创建一个消息框
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle("正在保存配置")
        msg_box.setText("正在保存配置，请稍候...")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.NoButton)
        msg_box.show()

        # 创建一个事件循环
        loop = QtCore.QEventLoop()

        # 在另一个线程中保存配置
        QtCore.QTimer.singleShot(0, lambda: self.save_config(loop))

        # 阻塞关闭事件，直到保存配置完成
        loop.exec()

        # 关闭消息框并接受关闭事件
        msg_box.accept()
        event.accept()

    def save_config(self, loop):
        # 在这里添加保存配置的代码
        conf().save_user_datas()
        loop.quit()

    def initUI(self):
        self.setWindowTitle('客服助手')
        self.setWindowIcon(QtGui.QIcon(resource_path("favicon.ico")))
        self.setGeometry(300, 300, 800, 600)


        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # 计算窗口左上角的位置
        x = (screen_width - self.width()) // 2
        y = int(screen_height * 0.1)  # 偏上位置，可以根据需要调整比例

        self.move(x, y)

        self.label = QtWidgets.QLabel('Close the window to see the event in action.', self)
        self.label.setGeometry(50, 50, 300, 50)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Left side: Text output
        self.output = QTextEdit(self)
        self.output.setReadOnly(True)
        self.layout.addWidget(self.output, 3)

        # Right side: Buttons
        self.buttons_layout = QVBoxLayout()

        # Top Buttons
        self.modify_button = QPushButton('修改配置', self)
        self.modify_button.setProperty('class', 'warning')
        self.modify_button.clicked.connect(self.modify_config)
        self.buttons_layout.addWidget(self.modify_button)

        self.import_button = QPushButton('导入配置', self)
        self.import_button.clicked.connect(self.import_config)
        self.buttons_layout.addWidget(self.import_button)

        self.export_button = QPushButton('导出配置', self)
        self.export_button.clicked.connect(self.export_config)
        self.buttons_layout.addWidget(self.export_button)

        self.buttons_layout.addStretch()

        # Bottom Buttons
        self.start_button = QPushButton('开始服务', self)
        self.start_button.clicked.connect(self.start_service)
        self.buttons_layout.addWidget(self.start_button)

        self.stop_button = QPushButton('停止服务', self)
        self.stop_button.clicked.connect(self.stop_service)
        self.buttons_layout.addWidget(self.stop_button)

        self.exit_button = QPushButton('退出', self)
        self.exit_button.setProperty('class', 'danger')
        self.exit_button.clicked.connect(self.close_application)
        self.buttons_layout.addWidget(self.exit_button, alignment=Qt.AlignmentFlag.AlignBottom)

        self.layout.addLayout(self.buttons_layout, 1)

    def modify_config(self):
        try:
            dialog = ConfigDialog(self.config_path)
            if dialog.exec():
                self.output.append("配置已修改")
                logger.info("Configuration modified.")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"修改配置时出错: {e}")
            logger.error(f"Error modifying config: {e}")

    def import_config(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "导入配置文件", "", "JSON 文件 (*.json);;所有文件 (*)")
        if file_name:
            try:
                with open(file_name, 'r') as f:
                    imported_config = json.load(f)
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(imported_config, f, ensure_ascii=False, indent=4)
                self.output.append("配置已导入")
                logger.info("Configuration imported.")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导入配置时出错: {e}")
                logger.error(f"Error importing config: {e}")

    def export_config(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "导出配置文件", "", "JSON 文件 (*.json);;所有文件 (*)")
        if file_name:
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    current_config = json.load(f)
                with open(file_name, 'w', encoding='utf-8') as f:
                    json.dump(current_config, f, ensure_ascii=False, indent=4)
                self.output.append("配置已导出")
                logger.info("Configuration exported.")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出配置时出错: {e}")
                logger.error(f"Error exporting config: {e}")

    def start_service(self):
        try:
            if self.worker is None:
                self.worker = Worker()  # 创建 Worker 实例
                self.worker.data_ready.connect(self.update_output)
                self.worker.error_occurred.connect(self.show_error)
                self.thread = QThread()
                self.worker.moveToThread(self.thread)
                self.thread.started.connect(self.worker.run)
                self.thread.start()
                logger.info("Service started.")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"启动服务时出错: {e}")
            logger.error(f"Error starting service: {e}")

    def stop_service(self):
        try:
            if self.worker:
                self.thread.terminate()
                self.worker = None
                self.thread = None
                self.output.append("服务已停止")
                logger.info("Service stopped.")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"停止服务时出错: {e}")
            logger.error(f"Error stopping service: {e}")

    def update_output(self, data):
        self.output.append(data)

    def show_error(self, error):
        QMessageBox.critical(self, "错误", error)
        logger.error(error)

    def close_application(self):
        self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = ConfigEditor()
    apply_stylesheet(app, theme='light_cyan_500.xml')
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
