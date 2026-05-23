from flask import Flask, render_template, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(200), nullable=False)
    Description = db.Column(db.String(500))
    Date_created = db.Column(db.DateTime, default=datetime.utcnow)
    Completed = db.Column(db.Boolean, default=False)
    
    def __repr__(self) -> str:
        return f"{self.Sno} - {self.Title}"

@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']

        todo = Todo(Title=title, Description=desc)
        
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('todo.html', allTodo = allTodo)

@app.route('/complete/<int:sno>')
def complete(sno):

    todo = Todo.query.filter_by(Sno=sno).first()

    todo.Completed = True

    db.session.commit()

    return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)