import streamlit as st
from PIL import Image

def layout():
    logo = Image.open("logo.png")
    st.sidebar.image(logo, use_column_width=True)
    st.image("logo.png", width=100) 