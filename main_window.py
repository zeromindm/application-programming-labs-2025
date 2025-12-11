import os
import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFileDialog, QMessageBox,
                             QGroupBox, QStatusBar, QSizePolicy)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

from iterator import ImagePathIterator
from image_viewer import ImageViewer
from styles import STYLES


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.iterator = None
        self.current_image_path = None
        self.init_ui()

    def init_ui(self) -> None:
        self.setWindowTitle('Просмотрщик изображений - Лабораторная работа №5')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        control_group = QGroupBox("Управление")
        control_group.setStyleSheet(STYLES["group_box"])
        control_layout = QHBoxLayout()

        self.select_file_btn = QPushButton("Выбрать файл аннотации")
        self.select_file_btn.setStyleSheet(STYLES["menu_button"])
        self.select_file_btn.clicked.connect(self.select_annotation_file)
        control_layout.addWidget(self.select_file_btn)

        self.next_btn = QPushButton("Следующее изображение")
        self.next_btn.setStyleSheet(STYLES["button"])
        self.next_btn.clicked.connect(self.show_next_image)
        self.next_btn.setEnabled(False)
        control_layout.addWidget(self.next_btn)

        self.reset_btn = QPushButton("Начать сначала")
        self.reset_btn.setStyleSheet(STYLES["button"])
        self.reset_btn.clicked.connect(self.reset_viewer)
        self.reset_btn.setEnabled(False)
        control_layout.addWidget(self.reset_btn)

        control_group.setLayout(control_layout)
        main_layout.addWidget(control_group)

        self.image_viewer = ImageViewer()
        self.image_viewer.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        main_layout.addWidget(self.image_viewer, 1)

        info_group = QGroupBox("Информация")
        info_group.setStyleSheet(STYLES["group_box"])
        info_layout = QVBoxLayout()

        self.info_label = QLabel("Загрузите файл аннотации для начала работы")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("font-size: 14px; padding: 10px;")
        info_layout.addWidget(self.info_label)

        self.progress_label = QLabel("")
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setStyleSheet("color: #666666; font-size: 12px;")
        info_layout.addWidget(self.progress_label)

        info_group.setLayout(info_layout)
        main_layout.addWidget(info_group)

        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet(STYLES["status_bar"])
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готов к работе")

        self.setStyleSheet(STYLES["main_window"])

    def select_annotation_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл аннотации (CSV)",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )

        if file_path:
            try:
                self.iterator = ImagePathIterator(file_path)

                if len(self.iterator) == 0:
                    QMessageBox.warning(
                        self,
                        "Предупреждение",
                        "Файл аннотации не содержит допустимых путей к изображениям"
                    )
                    return


                self.next_btn.setEnabled(True)
                self.reset_btn.setEnabled(True)

                self.iterator.reset()
                self.show_next_image()

                file_name = os.path.basename(file_path)
                self.info_label.setText(
                    f"Загружен файл аннотации: {file_name}\n"
                    f"Найдено изображений: {len(self.iterator)}"
                )
                self.status_bar.showMessage(f"Загружено {len(self.iterator)} изображений")

            except ValueError as e:
                QMessageBox.critical(self, "Ошибка", str(e))
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Ошибка",
                    f"Не удалось загрузить файл аннотации: {str(e)}"
                )

    def show_next_image(self) -> None:
        if self.iterator is None:
            return

        try:
            image_path = next(self.iterator)
            self.current_image_path = image_path

            if self.image_viewer.display_image(image_path):
                current_idx = self.iterator.get_current_index()
                total_count = self.iterator.get_total_count()
                self.progress_label.setText(
                    f"Изображение {current_idx} из {total_count}"
                )
                self.status_bar.showMessage(f"Загружено: {os.path.basename(image_path)}")

        except StopIteration:
            QMessageBox.information(
                self,
                "Информация",
                "Просмотрены все изображения в коллекции"
            )
            self.iterator.reset()
            self.show_next_image()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось загрузить изображение: {str(e)}"
            )

    def reset_viewer(self) -> None:
        if self.iterator:
            self.iterator.reset()
            self.show_next_image()
            self.status_bar.showMessage("Просмотр сброшен к началу")

    def closeEvent(self, event) -> None:
        reply = QMessageBox.question(
            self,
            'Подтверждение',
            'Вы уверены, что хотите выйти?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()