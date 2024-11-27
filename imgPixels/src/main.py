import streamlit as st
import numpy as np
import cv2
from PIL import Image
import sqlite3
import io
from datetime import datetime

# Configurar la base de datos SQLite
def init_db():
    conn = sqlite3.connect("images.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            upload_date TEXT,
            image BLOB
        )
    """)
    conn.commit()
    conn.close()

def save_image_to_db(name, upload_date, image_data):
    conn = sqlite3.connect("images.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO images (name, upload_date, image) VALUES (?, ?, ?)", 
                   (name, upload_date, image_data))
    conn.commit()
    conn.close()

def fetch_all_images():
    conn = sqlite3.connect("images.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, upload_date FROM images")
    records = cursor.fetchall()
    conn.close()
    return records

class Converter:
    def __init__(self) -> None:
        self.color_dict = {}

    def mosaic(self, img, ratio=0.1):
        small = cv2.resize(img, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
        return cv2.resize(small, img.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

class Web:
    def __init__(self) -> None:
        self.upload = None
        self.original = None
        self.converted = None
        self.draw_text()

    def draw_text(self):
        st.set_page_config(
            page_title="Pixelart-Converter",
            page_icon="🖼️",
            layout="centered",
            initial_sidebar_state="expanded",
        )
        st.title("PixelArt-Converter")
        self.upload = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png', 'webp'])
        self.original, self.converted = st.columns(2)
        self.original.title("Original Image")
        self.converted.title("Converted Image")

if __name__ == "__main__":
    # Inicializar la base de datos
    init_db()

    web = Web()
    converter = Converter()

    if web.upload is not None:
        # Obtener nombre de archivo y fecha actual
        file_name = web.upload.name
        upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Cargar la imagen usando PIL
        img = Image.open(web.upload)
        img = np.array(img)  # Convertir la imagen a un arreglo numpy

        # Guardar la imagen original en la base de datos
        img_bytes = io.BytesIO()
        img_pil = Image.fromarray(img)
        img_pil.save(img_bytes, format='PNG')  # Guardar como PNG en memoria
        save_image_to_db(file_name, upload_date, img_bytes.getvalue())

        # Mostrar la imagen original
        web.original.image(web.upload)

        # Convertir la imagen a mosaico
        img = converter.mosaic(img)
        
        # Mostrar la imagen convertida
        web.converted.image(img, caption="Pixelated Image")

    # Mostrar historial de imágenes subidas
    st.markdown("---")
    st.markdown("### Historial de imagenes.")
    uploaded_images = fetch_all_images()
    if uploaded_images:
        for name, date in uploaded_images:
            st.markdown(f"- **Nombre:** {name} | **Fecha:** {date}")
    else:
        st.markdown("No images uploaded yet.")
