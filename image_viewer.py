from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class ImageViewer(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self) -> None:
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                border: 1px solid #cccccc;
                background-color: #f0f0f0;
            }
        """)
        self.layout.addWidget(self.image_label)

        self.info_label = QLabel("Изображение не загружено")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 12px;
                margin-top: 5px;
            }
        """)
        self.layout.addWidget(self.info_label)

        self.set_empty_image()

    def set_empty_image(self) -> None:
        self.image_label.setText("Выберите файл аннотации для начала работы")
        self.info_label.setText("Ожидание загрузки данных...")

    def display_image(self, image_path: str) -> bool:
        try:
            pixmap = QPixmap(image_path)

            if pixmap.isNull():
                self.image_label.setText(f"Не удалось загрузить изображение\n{image_path}")
                self.info_label.setText("Ошибка загрузки файла")
                return False

            label_size = self.image_label.size()
            if label_size.width() <= 0 or label_size.height() <= 0:
                label_size = self.size()

            scaled_pixmap = pixmap.scaled(
                label_size.width() - 20,
                label_size.height() - 20,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            self.image_label.setPixmap(scaled_pixmap)

            file_name = image_path.split('/')[-1] if '/' in image_path else image_path
            self.info_label.setText(
                f"Файл: {file_name}\n"
                f"Размер: {pixmap.width()}x{pixmap.height()}\n"
                f"Формат: {image_path.split('.')[-1].upper()}"
            )
            return True

        except Exception as e:
            self.image_label.setText(f"Ошибка при загрузке изображения\n{str(e)}")
            self.info_label.setText("Произошла ошибка")
            return False

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        if hasattr(self, 'current_image_path'):
            self.display_image(self.current_image_path)