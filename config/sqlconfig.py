import sqlalchemy as alch
import os
import dotenv
import pandas as pd

dotenv.load_dotenv()
password = os.getenv("pass")
dbName = "buysmart"

connectionData = f"mysql+pymysql://root:{password}@localhost/{dbName}"
engine = alch.create_engine(connectionData)