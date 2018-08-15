from flask import Flask, render_template, request, redirect
import os
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "appdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

@app.route('/', methods=['GET','POST'])
def index():
    if request.form:
        app = App(app_name=request.form.get("app_name"))
        db.session.add(app)
        db.session.commit()
    apps=App.query.all()
    return render_template("index.html", apps=apps)

@app.route("/update", methods=['POST'])
def update():
    newapp = request.form.get("newapp")
    oldapp=request.form.get("oldapp")
    app=App.query.filter_by(app_name=oldapp).first()
    app.app_name=newapp
    print(newapp)
    print(oldapp)
    db.session.commit()
    return redirect('/')

@app.route("/delete", methods=['POST'])
def delete():
    app_name= request.form.get("app_name")
    app=App.query.filter_by(app_name=app_name).first()
    db.session.delete(app)
    db.session.commit()
    return redirect('/')

class App(db.Model):
    app_name=db.Column(db.String(120), unique=True, nullable=False, primay_key=True)
    def __repr__(self):
        return "<App_Name: {})".format(self.app_name)
if __name__ == "__main__":
    app.run(debug=True)

