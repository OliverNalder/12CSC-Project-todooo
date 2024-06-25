import sqlite3
from bottle import route, run, debug, template, request, static_file, error, redirect
import os

# only needed when you run Bottle on mod_wsgi
from bottle import default_app

current_user = ''



@route('/todo', method=["GET", "POST"])
def todo_list():


    

    conn = sqlite3.connect(f'user_db/{current_user}.db')
    c = conn.cursor()
    c.execute("SELECT id, task, progress FROM todo WHERE status LIKE '1'")
    result = c.fetchall()
    c.close()

    '''if request.GET.slider():
        new_value = request.GET.slider.strip()
        value_id = request.GET.slider.id()
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("UPDATE todo SET progress ? WHERE id LIKE ?", (new_value, value_id))
        c.close()'''
    

    output = template('make_table', rows=result)
    return output

@route('/closed')
def closed_list():
    conn = sqlite3.connect(f'user_db/{current_user}.db')
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '0'")
    result = c.fetchall()
    c.close

    output = template('archives_table', rows=result)
    return output

@route("/signup", method="GET")
def signup():
    username_placeholder = 'Username:'
    if request.GET.save:
        username = request.GET.username.strip()
        password = request.GET.password.strip()


        
        
        conn = sqlite3.connect('acc_info.db')
        c = conn.cursor()
        c.execute(f"SELECT username FROM acc_info WHERE username LIKE '{username}'")
        checker = c.fetchall()
        c.close()
        

        
        try:
            if checker[0][0] == username:
                username_placeholder = 'Username not avalible'
                return template('signup.tpl', user_text=username_placeholder)
        except IndexError:
            conn = sqlite3.connect('acc_info.db')
            c = conn.cursor()
            c.execute("INSERT INTO acc_info (username,password) VALUES (?,?)", (username, password))
            conn.commit()
            c.close
            user_database = os.path.join("user_db", f'{username}.db')
            conn = sqlite3.connect(user_database) # Warning: This file is created in the current directory
            conn.execute("CREATE TABLE todo (id INTEGER PRIMARY KEY, task char(100) NOT NULL, status bool NOT NULL, progress INTEGER NOT NULL, description STRING)")

            return redirect('/')
    else:
        return template('signup.tpl', user_text=username_placeholder)
        
    
@route('/login', method='GET')
def login():
    
    username_placeholder = 'Username:'
    password_placeholder = 'Password:'
    if request.GET.save:
        username = request.GET.username.strip()
        password = request.GET.password.strip()

        
        conn = sqlite3.connect('acc_info.db')
        c = conn.cursor()
        c.execute("SELECT username FROM acc_info WHERE (username,password) = (?,?)", (username,password))
        checker = c.fetchall()
        
        c.close()

        try:
            if checker[0][0] == username:
                global current_user
                current_user = username
                return redirect('/')

        except IndexError:
            username_placeholder = 'Invalid Username or Password'
            password_placeholder = 'Invalid Username or Password'
            return template('login.tpl', user_text=username_placeholder, password_text=password_placeholder)
        
          
       
    else:
        return template('login.tpl', user_text=username_placeholder, password_text=password_placeholder)

@route('/new', method='GET')
def new_item():

    if request.GET.save:

        new = request.GET.task.strip()
        desc = request.GET.description.strip()
        conn = sqlite3.connect(f'user_db/{current_user}.db')
        c = conn.cursor()

        c.execute("INSERT INTO todo (task,status,progress,description) VALUES (?,?,?,?)", (new, 1, 0, desc))
        new_id = c.lastrowid
 
        conn.commit()
        c.close()

        return redirect('/todo')

    else:
        return template('new_task.tpl')


@route('/edit/<no:int>', method='GET')
def edit_item(no):

    if request.GET.save:
        edit = request.GET.task.strip()
        status = request.GET.status.strip()
        desc = request.GET.description.strip()
        print(edit, status, desc)

        if status == 'open':
            status = 1
        else:
            status = 0

        conn = sqlite3.connect(f'user_db/{current_user}.db')
        c = conn.cursor()
        c.execute("UPDATE todo SET task = ?, status = ?, description = ? WHERE id LIKE ?", (edit, status, desc, no))
        conn.commit()
        c.close()
        return redirect('/todo')
    else:
        conn = sqlite3.connect(f'user_db/{current_user}.db')
        c = conn.cursor()
        c.execute("SELECT task,description FROM todo WHERE id LIKE ?", (str(no)))
        cur_data = c.fetchall()
        print(cur_data)
        c.close()
        return template('edit_task', old=cur_data[0][0], no=no, old_desc=cur_data[0][1])


@route('/item<item:re:[0-9]+>')
def show_item(item):

        conn = sqlite3.connect(f'user_db/{current_user}.db')
        c = conn.cursor()
        c.execute("SELECT task FROM todo WHERE id LIKE ?", (item,))
        result = c.fetchall()
        c.close()

        if not result:
            return 'This item number does not exist!'
        else:
            return 'Task: %s' % result[0]

@route('/view/<no:int>')
def view_item(no):
    conn = sqlite3.connect(f'user_db/{current_user}.db')
    c = conn.cursor()
    c.execute("SELECT task, status, progress, description FROM todo WHERE id LIKE ?", (no))
    task, status, progress, description = c.fetchall()
    print(task)
    print(status)
    print(progress)
    print(description)
    c.close()
    return template('viewer', no=no, task=task, status=status, progress=progress, description=description)

@route('/help')
def help():

    return static_file('/static/help.html', root='.')


@route('/json<json:re:[0-9]+>')
def show_json(json):

    conn = sqlite3.connect(f'user_db/{current_user}.db')
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (json,))
    result = c.fetchall()
    c.close()

    if not result:
        return {'task': 'This item number does not exist!'}
    else:
        return {'task': result[0]}


@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'

@route('/')
def main():
    return template('main_page')

@route('/static/<filepath:path>')
def load_static(filepath):
    return static_file(filepath, root='./static')


debug(True)
run(reloader=True)


print("Hello World!")