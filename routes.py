from flask import url_for, render_template, request, redirect, session, g
from database import get_database
from app import app
# from werkzeug.security import generate_password_hash, check_password_hash


@app.teardown_request
def close_database(error):
    if hasattr(g, 'employee_manage.db'):
        g.employee_manage.db.close()
# didn't understand of above function & operator use.

def get_current_user():
    user = None
    if 'user' in session:
        user = session['user']
        db = get_database()
        user_cur = db.execute('select * from users where name = ?', [user])
        user = user_cur.fetchone()

    return user

@app.route('/')
def index():
    user = get_current_user()
    return render_template('home.html', user = user)

@app.route('/login', methods=["POST", "GET"])
def login():
    user = get_current_user()
    error = None
    db = get_database()
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']

        user_cursor = db.execute('select * from users where name = ?', [name])
        user = user_cursor.fetchone()

        if user:
            # if check_password_hash(user['password'], password):
            if password == user['password']:
                session['user'] = user['name']
                return redirect(url_for('dashboard'))

            else:
                error="Password did not match"

        else:
            error = "Username or Password didn't match. please try again"
    return render_template('login.html', loginerror = error, user = user)

@app.route('/register', methods=["POST","GET"])
def register():
    user = get_current_user()
    db = get_database()
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        # hashed_password = generate_password_hash(password)

        dbuser_cur = db.execute('select * from users where name = ?', [name])
        existing_username = dbuser_cur.fetchone()
        if existing_username:
            return render_template('register.html', registererror = 'Please take different username')


        db.execute('insert into users(name, password) values(?, ?)',[name, password])#can put hashed_password instead to unreadable in db
        db.commit()
        return redirect(url_for('index'))
    return render_template('register.html', user = user)

@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    db = get_database()

    emp_cur = db.execute('select * from emp')
    allemp = emp_cur.fetchall()

    return render_template('dashboard.html', user =user, allemp = allemp)


@app.route('/addnewemployee', methods = ["GET", "POST"])
def addnewemployee():
    user = get_current_user()
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']

        db = get_database()
        db.execute('insert into emp(name, email, phone, address) values(?,?,?,?)', [name, email, phone, address])
        db.commit()
        return redirect(url_for('dashboard'))

    return render_template('addnewemployee.html', user = user)

@app.route('/singleemployee/<int:empid>')
def singleemployee(empid):
    user = get_current_user()
    db = get_database()
    emp_cur = db.execute('select * from emp where empid = ?', [empid])
    single_emp = emp_cur.fetchone()

    return render_template('singleemployee.html', user = user, single_emp = single_emp)

@app.route('/fetchone/<int:empid>')
def fetchone(empid):
    user = get_current_user()
    db = get_database()
    emp_cur = db.execute('select * from emp where empid = ?', [empid])
    single_emp = emp_cur.fetchone()
    return render_template('updateemployee.html', user=user, single_emp=single_emp)

@app.route('/updateemployee', methods = ["GET", "POST"])
def updateemployee():
    user = get_current_user()
    if request.method == 'POST':
        empid = request.form['empid']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        db = get_database()
        db.execute('update emp set name = ?, email = ?, phone = ?, address = ? where empid = ?', [name, email, phone, address, empid])
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('updateemployee.html', user = user)

@app.route('/deleteemp/<int:empid>', methods = ["GET", "POST"])
def deleteemp(empid):
    user = get_current_user()
    if request.method == 'GET':
        db = get_database()
        db.execute('delete from emp where empid = ?', [empid])
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html', user = user)

@app.route('/logout')
def logout():
    session.pop('user', None)
    render_template('home.html')