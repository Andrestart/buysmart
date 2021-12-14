import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import pandas as pd


def app():
    st.write("""
    # *Welcome to BUY SMART*\n\n *Managing prices in the PAST, the PRESENT and the FUTURE. Pay less for your food.*
    """)

    portada = Image.open('images/cover.jpg')
    st.image(portada, use_column_width=True)