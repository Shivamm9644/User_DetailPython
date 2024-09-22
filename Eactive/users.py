from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.config.from_object('config.Config')

app.secret_key = 'secret123'

mysql = MySQL(app)

@app.route('/hello')
def hello():
    return "Hello!"

@app.route('/users')
def users():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template('users.html', users=users)

@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO users (name, email, role) VALUES (%s, %s, %s)", (name, email, role))
        mysql.connection.commit()
        flash('User added successfully!')
        return redirect(url_for('users'))
    
    return render_template('new_users.html')

@app.route('/users/<int:id>')
def user_details(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE id = %s", [id])
    user = cursor.fetchone()
    
    if user:
        return render_template('user_details.html', user=user)
    else:
        flash('User not found!')
        return redirect(url_for('users'))

@app.errorhandler(404)
def page_not_found(e):
    return "Page not found", 404

if __name__ == '__main__':
    app.run(debug=True)
