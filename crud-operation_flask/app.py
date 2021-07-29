from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy      # for the database
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'    # to create the database
db = SQLAlchemy(app)               # adding the database to our app.py

class Todo(db.Model):                     # to create the model of what all properties be present inside our datbase
    id = db.Column(db.Integer, primary_key=True)             # through which we will call all the tasks.
    content = db.Column(db.String(200), nullable=False)         # content of the task.
    date_created = db.Column(db.DateTime, default=datetime.utcnow)      # time, when the task is added. 

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])      # main route page will use only post and  get methods
def index():
    if request.method == 'POST':
        task_content = request.form['content']        # task_content variable will take all the contents and store it to new_task variable through Todo model.
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)     # now add it to our databae
            db.session.commit()
            return redirect('/')    # after adding head back to the home route
        except:
            return 'There was an issue adding your task'      # if any problem throw an error 

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()       # to show all the tasks created on the datbase ,on the index page.
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')         
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)   # grab all the contents along with time and index number to this variable 

    try:
        db.session.delete(task_to_delete)        # .delete fuction will delete all the content
        db.session.commit()
        return redirect('/')                    # again come back to the home page
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])      # update page also will handle post and get request only.
def update(id):            
    task = Todo.query.get_or_404(id)      # to grab the id of the task where update is clicked.

    if request.method == 'POST':
        task.content = request.form['content']  # content of the home page will be updated by the  content of the updated page on the perticular id.
        try:
            db.session.commit()
            return redirect('/')          # again redirect it to the home page.
        except:
            return 'There was an issue updating your task'   # else throw an error.

    else:
        return render_template('update.html', task=task)      


if __name__ == "__main__":
    app.run(debug=True)          # to run the app.py file with showing the error on the webpage (if any).
