from dotenv import load_dotenv
from flask import Flask


app = Flask(__name__)

app.config["RESTFUL_JSON"] = {"ensure_ascii": False}


load_dotenv()
