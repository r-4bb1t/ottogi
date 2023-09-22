import streamlit as st
from PIL import Image

image = Image.open('logo.png')

st.image(image, width=200)