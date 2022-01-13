import sys
sys.path.append("../")

from before_streamlit import getdata as g
from before_streamlit import perproduct as prod
from before_streamlit import scrapit as s

g.getmydata()
prod.toprophet()
s.choosesuper()