from flask import Flask, render_template
from flask_mysqldb import MySQL
from flask import jsonify
from datetime import datetime

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pTss4321!'
app.config['MYSQL_DB'] = 'myDb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql = MySQL(app)

@app.context_processor
def inject_year():
    return {'current_year': datetime.now().year}

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM course")
    data = cur.fetchall()
    # print(data)
    cur.close()
    return render_template('index.html', data=data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/course/<int:course_id>')
def course_detail(course_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM course WHERE ID = %s", (course_id,))
    course = cur.fetchone()  # Get a single course based on ID
    cur.close()
    
    if course:
        return render_template('course_detail.html', course=course)
    else:
        return "Course not found", 404  # Handle case if course does not exist


@app.route('/api/courses')
def get_courses_json():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM course")
    rows = cur.fetchall()
    cur.close()
    return jsonify(rows)


if __name__ == '__main__':
    app.run(debug=True)
