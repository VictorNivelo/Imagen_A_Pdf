import sys
import os
import webbrowser
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QFileDialog,
    QProgressBar,
    QMessageBox,
    QLineEdit,
    QMenuBar,
    QAction,
    QComboBox,
    QScrollArea,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt, QStandardPaths, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PIL import Image


class PDFConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Convertidor de Imágenes a PDF")
        self.setMinimumSize(700, 600)
        self.imagen_paths = []
        self.ruta_pdf = ""
        self.ruta_imagen = ""
        self.modo_oscuro = False
        self.load_config()

        icon_path = "..\\Imagen_A_Pdf\\Imagenes\\Iconos\\"
        self.icon_claro = QIcon(os.path.join(icon_path, "Icono_claro.png"))
        self.icon_oscuro = QIcon(os.path.join(icon_path, "Icono_oscuro.png"))
        self.icon_engranaje = QIcon(os.path.join(icon_path, "Engranaje.png"))
        self.icon_imagen = QIcon(os.path.join(icon_path, "Imagen.png"))
        self.icon_pdf = QIcon(os.path.join(icon_path, "Pdf.png"))

        self.temas = {
            "Claro": """
                QWidget {
                    background-color: #f9f9f9;
                    color: #000000;
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 8px;
                    padding: 12px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QLabel {
                    color: #333333;
                    font-size: 18px;
                }
                QLineEdit, QTextEdit {
                    background-color: #ffffff;
                    color: #333333;
                    font-size: 16px;
                    border: 1px solid #cccccc;
                    border-radius: 5px;
                }
                QComboBox {
                    background-color: #ffffff;
                    color: #333333;
                    font-size: 16px;
                    border: 1px solid #cccccc;
                    border-radius: 5px;
                }
                QProgressBar {
                    height: 20px;
                    background-color: #e0e0e0;
                    border-radius: 5px;
                }
            """,
            "Oscuro": """
                QWidget {
                    background-color: #2e2e2e;
                    color: #ffffff;
                }
                QPushButton {
                    background-color: #008CBA;
                    color: white;
                    border-radius: 8px;
                    padding: 12px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #007B9E;
                }
                QLabel {
                    color: #ffffff;
                    font-size: 18px;
                }
                QLineEdit, QTextEdit {
                    background-color: #4a4a4a;
                    color: #ffffff;
                    font-size: 16px;
                    border: 1px solid #cccccc;
                    border-radius: 5px;
                }
                QComboBox {
                    color: #ffffff;
                    font-size: 16px;
                    border: 1px solid #cccccc;
                    border-radius: 5px;
                }
                QProgressBar {
                    height: 20px;
                    background-color: #555555;
                    border-radius: 5px;
                }
            """,
        }

        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        menu = menu_bar.addMenu("Opciones")

        cambiar_ruta_action = QAction(
            "Seleccionar carpeta predeterminada para PDFs", self
        )
        cambiar_ruta_action.triggered.connect(self.seleccionar_ruta_pdf)
        menu.addAction(cambiar_ruta_action)

        cambiar_imagen_ruta_action = QAction(
            "Seleccionar carpeta predeterminada para cargar imágenes", self
        )
        cambiar_imagen_ruta_action.triggered.connect(self.seleccionar_ruta_imagen)
        menu.addAction(cambiar_imagen_ruta_action)

        cambiar_tema_action = QAction("Establecer modo claro/oscuro", self)
        cambiar_tema_action.triggered.connect(self.cambiar_tema)
        menu.addAction(cambiar_tema_action)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        title_label = QLabel("Convertidor de Imágenes a PDF")
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        self.combo_tamanio_hoja = QComboBox()
        self.combo_tamanio_hoja.addItems(
            ["Mantener tamaño original", "Ajustar a hoja", "A5", "A4", "Carta", "Legal"]
        )
        self.combo_tamanio_hoja.setCurrentText("Mantener tamaño original")
        layout.addWidget(self.combo_tamanio_hoja)

        self.select_button = QPushButton("Seleccionar Imágenes", self)
        self.select_button.setIcon(self.icon_imagen)
        self.select_button.setIconSize(QSize(20, 20))
        self.select_button.clicked.connect(self.seleccionar_imagenes)
        layout.addWidget(self.select_button)

        self.image_list_label = QLabel("Imágenes seleccionadas:")
        layout.addWidget(self.image_list_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.image_container = QWidget()
        self.image_layout = QHBoxLayout(self.image_container)
        self.image_container.setLayout(self.image_layout)
        self.scroll_area.setWidget(self.image_container)
        layout.addWidget(self.scroll_area)

        self.nombre_pdf_label = QLabel("Nombre del archivo PDF:")
        layout.addWidget(self.nombre_pdf_label)

        self.nombre_pdf_input = QLineEdit()
        self.nombre_pdf_input.setFont(QFont("Arial", 16))
        layout.addWidget(self.nombre_pdf_input)

        self.convert_button = QPushButton("Convertir a PDF", self)
        self.convert_button.setIcon(self.icon_pdf)
        self.convert_button.setIconSize(QSize(20, 20))
        self.convert_button.clicked.connect(self.convertir_a_pdf)
        self.convert_button.setEnabled(False)
        layout.addWidget(self.convert_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        self.aplicar_tema()

    def load_config(self):
        if os.path.exists("configuracion.txt"):
            with open("configuracion.txt", "r") as file:
                lines = file.readlines()
                if len(lines) >= 3:
                    self.ruta_imagen = lines[0].strip()
                    self.ruta_pdf = lines[1].strip()
                    self.modo_oscuro = lines[2].strip().lower() == "oscuro"

    def save_config(self):
        with open("configuracion.txt", "w") as file:
            file.write(
                f"{self.ruta_imagen}\n{self.ruta_pdf}\n{'Oscuro' if self.modo_oscuro else 'Claro'}\n"
            )

    def cambiar_tema(self):
        self.modo_oscuro = not self.modo_oscuro
        self.aplicar_tema()

    def aplicar_tema(self):
        if self.modo_oscuro:
            self.setStyleSheet(self.temas["Oscuro"])
        else:
            self.setStyleSheet(self.temas["Claro"])

    def seleccionar_imagenes(self):
        file_dialog = QFileDialog()
        nuevas_imagenes, _ = file_dialog.getOpenFileNames(
            self,
            "Seleccionar Imágenes",
            self.ruta_imagen,
            "Imágenes (*.png *.jpg *.jpeg)",
        )
        if nuevas_imagenes:
            self.imagen_paths.extend(nuevas_imagenes)
            self.update_image_preview()

    def update_image_preview(self):
        for i in reversed(range(self.image_layout.count())):
            widget = self.image_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        for path in self.imagen_paths:
            label = QLabel()
            pixmap = QPixmap(path).scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio)
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.image_layout.addWidget(label)

        self.image_list_label.setText(
            f"Imágenes seleccionadas: {len(self.imagen_paths)}"
        )
        self.convert_button.setEnabled(len(self.imagen_paths) > 0)

    def seleccionar_ruta_pdf(self):
        self.ruta_pdf = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar Carpeta para Guardar PDF",
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DocumentsLocation
            ),
        )
        if self.ruta_pdf:
            self.save_config()

    def seleccionar_ruta_imagen(self):
        self.ruta_imagen = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar Carpeta de Imágenes",
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.PicturesLocation
            ),
        )
        if self.ruta_imagen:
            self.save_config()

    def convertir_a_pdf(self):
        output_filename, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar PDF",
            os.path.join(
                self.ruta_pdf, self.nombre_pdf_input.text() or "documento.pdf"
            ),
            "PDF Files (*.pdf)",
        )
        if output_filename:
            self.progress_bar.setVisible(True)
            self.progress_bar.setMaximum(len(self.imagen_paths))

            images = []
            try:
                for i, path in enumerate(self.imagen_paths):
                    img = Image.open(path).convert("RGB")
                    tamanio_hoja = self.combo_tamanio_hoja.currentText()
                    if tamanio_hoja == "A5":
                        img = img.resize((420, 595))
                    elif tamanio_hoja == "A4":
                        img = img.resize((595, 842))
                    elif tamanio_hoja == "Carta":
                        img = img.resize((612, 792))
                    elif tamanio_hoja == "Legal":
                        img = img.resize((612, 1008))
                    images.append(img)
                    self.progress_bar.setValue(i + 1)

                if images:
                    images[0].save(
                        output_filename, save_all=True, append_images=images[1:]
                    )
                    self.status_label.setText(
                        f"¡PDF guardado exitosamente en:\n{output_filename}!"
                    )
                    self.status_label.setStyleSheet("color: green;")
                    self.confirmar_abrir_ruta(output_filename)
            except Exception as e:
                self.status_label.setText(f"Error: {str(e)}")
                self.status_label.setStyleSheet("color: red;")
            finally:
                self.progress_bar.setVisible(False)

    def confirmar_abrir_ruta(self, output_filename):
        respuesta = QMessageBox.question(
            self,
            "Abrir PDF",
            "¿Te gustaría abrir el PDF en su ubicación?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if respuesta == QMessageBox.StandardButton.Yes:
            carpeta = os.path.dirname(output_filename)
            webbrowser.open(f"file://{carpeta}")

    def closeEvent(self, event):
        self.save_config()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFConverterApp()
    window.show()
    sys.exit(app.exec())
