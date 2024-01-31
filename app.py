from flask import Flask  , render_template , request  ,redirect , Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') 

db = SQLAlchemy(app)

alltodo = [] 
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200),unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.id} - {self.title}'

@app.route("/", methods=['GET', 'POST'])
def home():
    global alltodo
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        print(request.form)
        todo = Todo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()
        # return render_template('index.html', alltodo=alltodo)
    alltodo = Todo.query.all()
    return render_template('index.html', alltodo=alltodo)


@app.route('/about')
def about():
    return render_template('about.html')



@app.route("/delete/<int:id>")
def product(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


@app.route('/update/<int:id>' , methods = ['GET' , 'POST'])
def update(id):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        todo = Todo.query.filter_by(id=id).first()
        todo.title = title
        todo.description = description
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(id=id).first()
    return render_template('update.html', todo=todo)




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
