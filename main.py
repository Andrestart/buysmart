from re import T
import streamlit as st
from PIL import Image
from multipage import MultiPage
from pages import home
from pages import graphs
from pages import price
from pages import structure

# from pages import mapas

app = MultiPage()


app.add_page("Index", home.app)
app.add_page("Project structure", structure.app)
app.add_page("Prediction graphs", graphs.app)
app.add_page("What's cheaper?", price.app)


app.run()