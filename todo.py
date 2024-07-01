import sqlite3
from bottle import route, run, debug, template, request, static_file, error, redirect
import os
import bcrypt
import re

# only needed when you run Bottle on mod_wsgi
from bottle import default_app

current_user = ''
order = 'ASC'
sort_by = 'task'


@route('/todo', method="GET")
def todo_list():

    if current_user == '':
        return redirect('/login')
    else:
        global order, sort_by #saved as global to save between websites


        if request.GET.save:
            new_order = request.GET.Order.strip()
            new_sort_by = request.GET.Sort_By.strip()

            if new_order == 'ascending':
                order = 'ASC'

            elif new_order == 'descending':
                order = 'DESC'

            if new_sort_by == 'name':
                sort_by = 'task'
            elif new_sort_by != '':
                sort_by = new_sort_by

        

        conn = sqlite3.connect(f'user_db/{current_user}.db')
        c = conn.cursor()
        c.execute(f"SELECT id, task, progress FROM todo WHERE status LIKE '1' ORDER BY {str(sort_by)} COLLATE NOCASE {str(order)}")
        result = c.fetchall()
        c.close()

        new_order = result

        if request.GET.progress_save:
            new_value = request.GET.slider.strip()
            new_id = request.GET.value_id.strip()
            conn = sqlite3.connect(f'user_db/{current_user}.db')
            c = conn.cursor()
            if new_value == '8':
                c.execute("UPDATE todo SET progress = ?, status = ? WHERE id LIKE ?", (0, 0, new_id))
                conn.commit()
            else:
                c.execute("UPDATE todo SET progress = ? WHERE id LIKE ?", (new_value, new_id))
                conn.commit()
            
            c.close()

            return redirect('/todo')

        output = template('make_table', rows=result)
        return output

    
@route('/archive_all/<no:int>')
def archive_all(no):
    if no == 0:
        conn = sqlite3.connect(f'user_db/{current_user}.db')
        c = conn.cursor()
        c.execute("UPDATE todo SET status = 0 WHERE status = 1")
        conn.commit()
        c.close()
        return redirect('/todo')
    elif no == 1:
        conn = sqlite3.connect(f'user_db/{current_user}.db')
        c = conn.cursor()
        c.execute("UPDATE todo SET status = 1 WHERE status = 0")
        conn.commit()
        c.close()
        return redirect('/todo')


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
            c.execute("INSERT INTO acc_info (username,password) VALUES (?,?)", (username, bcrypt.hashpw(request.GET.password.strip().encode('utf-8'), bcrypt.gensalt())))
            conn.commit()
            c.close
            user_database = os.path.join("user_db", f'{username}.db')
            conn = sqlite3.connect(user_database) # Warning: This file is created in the current directory
            conn.execute("CREATE TABLE todo (id INTEGER PRIMARY KEY, task char(100) NOT NULL, status bool NOT NULL, progress INTEGER NOT NULL, description STRING)")
            global current_user
            current_user = username
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

        userBytes = password.encode('utf-8')
        
        conn = sqlite3.connect('acc_info.db')
        c = conn.cursor()
        c.execute("SELECT username,password FROM acc_info WHERE username = ?", (username,))
        checker = c.fetchall()
        
        c.close()
        try:
            if bcrypt.checkpw(userBytes, checker[0][1]):

                global current_user
                current_user = username
                return redirect('/')
            else:
                username_placeholder = 'Invalid Username or Password'
                password_placeholder = 'Invalid Username or Password'
                return template('login.tpl', user_text=username_placeholder, password_text=password_placeholder)

        except IndexError:
            username_placeholder = 'Invalid Username or Password'
            password_placeholder = 'Invalid Username or Password'
            return template('login.tpl', user_text=username_placeholder, password_text=password_placeholder)
        
          
       
    else:
        return template('login.tpl', user_text=username_placeholder, password_text=password_placeholder)

@route('/delete_account', method='GET')
def delete_account():
    username_placeholder = 'Username:'
    password_placeholder = 'Password:'
    if request.GET.delete_acc:
        username = request.GET.username.strip()
        password = request.GET.password.strip()

        userBytes = password.encode('utf-8')
        
        conn = sqlite3.connect('acc_info.db')
        c = conn.cursor()
        c.execute("SELECT username,password FROM acc_info WHERE username = ?", (username,))
        checker = c.fetchall()
        
        c.close()
        try:
            if bcrypt.checkpw(userBytes, checker[0][1]):

                global current_user
                current_user = ''
                user_database = os.path.join("user_db", f'{username}.db')
                os.remove(user_database)
                return redirect('/')
            else:
                username_placeholder = 'Invalid Username or Password'
                password_placeholder = 'Invalid Username or Password'
                return template('delete_acc.tpl', user_text=username_placeholder, password_text=password_placeholder)

        except IndexError:
            username_placeholder = 'Invalid Username or Password'
            password_placeholder = 'Invalid Username or Password'
            return template('delete_acc.tpl', user_text=username_placeholder, password_text=password_placeholder)
        
          
       
    else:
        return template('delete_acc.tpl', user_text=username_placeholder, password_text=password_placeholder)
        

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
    
    elif request.GET.delete:
        conn = sqlite3.connect(f'user_db/{current_user}.db')
        c = conn.cursor()
        c.execute("DELETE FROM todo WHERE id LIKE ?", (str(no)))
        c.close()
        conn.commit()
        return redirect('/todo')
    
    else:
        conn = sqlite3.connect(f'user_db/{current_user}.db')
        c = conn.cursor()
        c.execute("SELECT task,description FROM todo WHERE id LIKE ?", (str(no)))
        cur_data = c.fetchone()
        c.close()

        return template('edit_task', old=cur_data[0], no=no, old_desc=cur_data[1])


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
    c.execute("SELECT task, status, progress, description FROM todo WHERE id LIKE ?", (str(no)))
    info = c.fetchall()
    print(info)
    if info[0][1] == '1':
        status = "Open"
    else:
        status = "Closed"

    c.close()
    return template('viewer', no=no, task=info[0][0], status=status, progress=info[0][2], description=info[0][3])

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
