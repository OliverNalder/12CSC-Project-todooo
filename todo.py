import sqlite3
from bottle import route, run, debug, template, request, static_file, error, redirect
import os
import bcrypt
import re
import datetime
import gc

# only needed when you run Bottle on mod_wsgi
from bottle import default_app

# Initialize global variables
current_user = ''  # Keeps track of the current user
delete_detection = False  # Detects if a user is deleting their account
order = 'ASC'  # Default order for sorting tasks
sort_by = 'task'  # Default sorting criteria
current_date = datetime.datetime.now()
current_date = f"{current_date.strftime('%Y')}-{current_date.strftime('%m')}-{current_date.strftime('%d')}"

@route('/todo', method="GET")
def todo_list():
    # Redirect to login if no user is logged in
    if current_user == '':
        return redirect('/login')
    else:
        global order, sort_by  # Keep sorting options between pages

        # Handle sorting and ordering options
        if request.GET.save:
            new_order = request.GET.Order.strip()
            new_sort_by = request.GET.Sort_By.strip()

            if new_order == 'Ascending':
                order = 'ASC'
            elif new_order == 'Descending':
                order = 'DESC'

            if new_sort_by == 'Name':
                sort_by = 'task'
            elif new_sort_by != '':
                sort_by = new_sort_by

        # Fetch tasks from the database
        conn = sqlite3.connect(f'user_db/{current_user}.db')
        c = conn.cursor()
        c.execute(f"SELECT id, task, progress, due FROM todo WHERE status LIKE '1' ORDER BY {str(sort_by)} COLLATE NOCASE {str(order)}")
        result = c.fetchall()
        c.close()

        # Handle progress update
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

        # Render the todo list template
        output = template('make_table', rows=result)
        return output

@route('/archive_all/<no:int>')
def archive_all(no):
    # Redirect to login if no user is logged in
    if current_user == '':
        return redirect('/login')
    else:
        conn = sqlite3.connect(f'user_db/{current_user}.db')
        c = conn.cursor()
        if no == 0:
            c.execute("UPDATE todo SET status = 0 WHERE status = 1")  # Archive all open tasks
        elif no == 1:
            c.execute("UPDATE todo SET status = 1 WHERE status = 0")  # Unarchive all closed tasks
        conn.commit()
        c.close()
        return redirect('/todo')

@route('/closed')
def closed_list():
    # Redirect to login if no user is logged in
    if current_user == '':
        return redirect('/login')
    else:
        # Fetch closed tasks from the database
        conn = sqlite3.connect(f'user_db/{current_user}.db')
        c = conn.cursor()
        c.execute("SELECT id, task FROM todo WHERE status LIKE '0'")
        result = c.fetchall()
        c.close()

        # Render the closed tasks template
        output = template('archives_table', rows=result)
        return output

@route("/signup", method="GET")
def signup():
    username_placeholder = 'Username:'
    if request.GET.save:
        username = request.GET.username.strip()
        password = request.GET.password.strip()

        # Validate username
        if not re.match(r"^[a-zA-Z0-9]+$", username):
            return template('signup.tpl', user_text="Username may contain only alphanumeric characters")
        if " " in username:
            return template('signup.tpl', user_text="Username cannot contain spaces.")
        
        # Check if the username is already taken
        conn = sqlite3.connect('acc_info.db')
        c = conn.cursor()
        c.execute(f"SELECT username FROM acc_info WHERE username LIKE '{username}'")
        checker = c.fetchall()
        c.close()
        
        try:
            if checker[0][0] == username:
                username_placeholder = 'Username not available'
                return template('signup.tpl', user_text=username_placeholder)
        except IndexError:
            # Create new account and user database
            conn = sqlite3.connect('acc_info.db')
            c = conn.cursor()
            c.execute("INSERT INTO acc_info (username, password) VALUES (?, ?)", (username, bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())))
            conn.commit()
            c.close()
            user_database = os.path.join("user_db", f'{username}.db')
            conn = sqlite3.connect(user_database)  # Warning: This file is created in the current directory
            conn.execute("CREATE TABLE todo (id INTEGER PRIMARY KEY, task char(100) NOT NULL, status bool NOT NULL, progress INTEGER NOT NULL, description STRING, priority STRING, created DATE, due DATE)")
            conn.close()
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
        
        # Fetch account details from the database
        conn = sqlite3.connect('acc_info.db')
        c = conn.cursor()
        c.execute("SELECT username, password FROM acc_info WHERE username = ?", (username,))
        checker = c.fetchall()
        c.close()
        
        try:
            # Check if the password matches
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
        
        # Fetch account details from the database
        conn = sqlite3.connect('acc_info.db')
        c = conn.cursor()
        c.execute("SELECT username, password FROM acc_info WHERE username = ?", (username,))
        checker = c.fetchall()
        c.close()
        
        try:
            # Check if the password matches
            if bcrypt.checkpw(userBytes, checker[0][1]):
                global current_user
                global delete_detection
                delete_detection = True
                current_user = ''
                return redirect(f'/deleted/{username}')
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

@route('/deleted/<username>')
def deleted(username):
    global delete_detection
    if delete_detection:
        try:
            # Delete user database and account information
            conn = sqlite3.connect(f'user_db/{username}.db')
            conn.close()
            gc.collect()
            os.remove(f"user_db/{username}.db")
            conn = sqlite3.connect('acc_info.db')
            c = conn.cursor()
            c.execute("DELETE FROM acc_info WHERE username LIKE ?", (username,))
            c.close()
            conn.commit()
        except PermissionError:
            return redirect(f'/deleted/{username}')
        delete_detection = False
        return redirect('/')
    return redirect('/')

@route('/new', method='GET')
def new_item():
    if current_user == '':
        return redirect('/login')
    else:
        global current_date

        if request.GET.save:
            # Get new task details from the request
            new = request.GET.task.strip()
            desc = request.GET.description.strip()
            priority = request.GET.priority.strip()
            due_date = request.GET.due_date.strip()
            conn = sqlite3.connect(f'user_db/{current_user}.db')
            c = conn.cursor()

            # Insert the new task into the database
            c.execute("INSERT INTO todo (task, status, progress, description, priority, created, due) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                      (new, 1, 0, desc, priority, current_date, due_date))
            conn.commit()
            c.close()
            return redirect('/todo')
        else:
            return template('new_task.tpl', date=current_date)

@route('/edit/<no:int>', method='GET')
def edit_item(no):
    if current_user == '':
        return redirect('/login')
    else:
        if request.GET.save:
            # Get edited task details from the request
            edit = request.GET.task.strip()
            status = request.GET.status.strip()
            desc = request.GET.description.strip()
            priority = request.GET.priority.strip()
            due_date = request.GET.due_date.strip()

            # Convert status to boolean
            if status == 'Open':
                status = 1
            else:
                status = 0

            # Update the task in the database
            conn = sqlite3.connect(f'user_db/{current_user}.db')
            c = conn.cursor()
            c.execute("UPDATE todo SET task = ?, status = ?, description = ?, priority = ?, due = ? WHERE id LIKE ?", 
                      (edit, status, desc, priority, due_date, no))
            conn.commit()
            c.close()
            return redirect('/todo')

        elif request.GET.delete:
            # Delete the task from the database
            conn = sqlite3.connect(f'user_db/{current_user}.db')
            c = conn.cursor()
            c.execute("DELETE FROM todo WHERE id LIKE ?", (str(no),))
            c.close()
            conn.commit()
            return redirect('/todo')
        else:
            try:
                # Fetch the current task details
                conn = sqlite3.connect(f'user_db/{current_user}.db')
                c = conn.cursor()
                c.execute("SELECT task, description, priority, created, due FROM todo WHERE id LIKE ?", (str(no),))
                cur_data = c.fetchone()
                c.close()

                # Set the priority string for the template
                if cur_data[2] == 0:
                    old_priority = "Low"
                elif cur_data[2] == 1:
                    old_priority = "Medium"
                else:
                    old_priority = "High"

                # Render the edit task template
                return template('edit_task', old=cur_data[0], no=no, old_desc=cur_data[1], old_priority=old_priority, created=cur_data[3], old_due=cur_data[4])
            except TypeError:
                return redirect('/todo')

@route('/item<item:re:[0-9]+>')
def show_item(item):
    # Fetch a specific task by ID
    conn = sqlite3.connect(f'user_db/{current_user}.db')
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (item,))
    result = c.fetchall()
    c.close()

    if not result:
        return 'This item number does not exist!'
    else:
        return f'Task: {result[0]}'

@route('/view/<no:int>')
def view_item(no):
    if current_user == '':
        return redirect('/login')
    else:
        try:
            # Fetch detailed task information
            conn = sqlite3.connect(f'user_db/{current_user}.db')
            c = conn.cursor()
            c.execute("SELECT task, status, progress, description, priority, created, due FROM todo WHERE id LIKE ?", (str(no),))
            info = c.fetchall()
            c.close()

            # Convert status to string
            if info[0][1] == 1:
                status = "Open"
            else:
                status = "Closed"

            # Set description if not provided
            description = info[0][3] if info[0][3] else 'No description'

            # Render the task viewer template
            return template('viewer', no=no, task=info[0][0], status=status, progress=info[0][2], description=description, priority=info[0][4], created=str(info[0][5]), due=str(info[0][6]))
        except TypeError:
            return redirect('/todo')

@route('/help')
def help():
    return static_file('/static/help.html', root='.')

@route('/json<json:re:[0-9]+]')
def show_json(json):
    # Fetch task details and return as JSON
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