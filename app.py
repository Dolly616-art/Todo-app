from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION']= False
db=SQLAlchemy(app)
 
class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(length=100),nullable=True )
    desc=db.Column(db.String(length=300),nullable=True)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)


    def __repr__(self):
        return f"  {self.sno} - {self.title}"


with app.app_context():
         db.create_all()


@app.route("/",methods=['GET','POST'])
def Home_page():
    if request.method=='POST':
        if 'title' in request.form:
            title = request.form['title']
            desc = request.form['desc']       
            todo=Todo(title=title,desc=desc)
            db.session.add(todo)
            db.session.commit()
            
    allTodo=Todo.query.all()
    return  render_template('index.html',allTodo=allTodo)

@app.route("/show")
def products():
    allTodo=Todo.query.all()
    print(allTodo)
    return "<p>this is my products!</p>"

@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
     
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        if todo:
            todo.title = title
            todo.desc = desc
            db.session.commit()
            return redirect("/")
        else:
            return "No todo found for the given sno"
         
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
     
 
    return  redirect("/")

if __name__ == "__main__":
    app.run(debug=True,port=8000)
    