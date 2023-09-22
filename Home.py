import streamlit as st
from components.layout.header import header
from PIL import Image

header()

image = Image.open('logo.png')

st.image(image, width=200)