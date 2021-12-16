import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import pandas as pd


def app():
    st.write("""
    # *Welcome to BUY SMART*\n\n *Managing data from the PAST, the PRESENT and the FUTURE. Pay less for your food.*
    """)
    st.sidebar.image("images/Andres Perez logo2.png", use_column_width=True)
    portada = Image.open('images/cover2.jpg')
    st.image(portada, use_column_width=True)