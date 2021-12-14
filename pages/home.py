import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import pandas as pd


def app():
    st.write("""
    # *Welcome to BUY SMART*
    """)
    portada = Image.open('images/cover.jpg')
    st.image(portada, use_column_width=True)