import streamlit as st
import numpy as np
import cv2
from PIL import Image

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
    web = Web()
    converter = Converter()

    if web.upload is not None:
        # Cargar la imagen usando PIL
        img = Image.open(web.upload)
        img = np.array(img)  # Convertir la imagen a un arreglo numpy

        # Mostrar la imagen original
        web.original.image(web.upload)

        # Convertir la imagen a mosaico
        img = converter.mosaic(img)
        
        # Mostrar la imagen convertida
        web.converted.image(img, caption="Pixelated Image")


