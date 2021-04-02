from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__,static_folder='./build', static_url_path='/')
api = Api(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__=="__main__":
    app.run(debug=True)