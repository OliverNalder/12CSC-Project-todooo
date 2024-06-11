import sqlite3
from bottle import route, run, debug, template, request, static_file, error, redirect

# only needed when you run Bottle on mod_wsgi
from bottle import default_app


@route('/todo', method=["GET", "POST"])
def todo_list():

    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task, progress FROM todo WHERE status LIKE '1'")
    result = c.fetchall()
    c.close()

    if request.GET.slider():
        new_value = request.GET.slider.strip()
        value_id = request.GET.slider.id()
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("UPDATE todo SET progress ? WHERE id LIKE ?", (new_value, value_id))
        c.close()
    

    output = template('make_table', rows=result)
    return output

@route('/closed')
def closed_list():
    conn = sqlite3.connect('todo.db')
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
        password = request.GET.password()


        conn = sqlite3.connect('acc_info.db')
        c = conn.cursor()
        c.execute("SELECT username FROM acc_info WHERE username LIKE ?", (username))
        checker = c.fetchall()
        c.close()
        if checker:
            username_placeholder = 'Username not avalible'
            return template('signup.tpl', username_placeholder)
        else:
            conn = sqlite3.connect('acc_info.db')
            c = conn.cursor()
            c.execute("INSERT INTO acc_info (username,password) VALUES (?,?)", (username, password))
            conn.commit()
            c.close
            return redirect('/')
    else:
        return template('signup.tpl', user_text=username_placeholder)
        
    


@route('/new', method='GET')
def new_item():

    if request.GET.save:

        new = request.GET.task.strip()
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()

        c.execute("INSERT INTO todo (task,status,progress) VALUES (?,?,?)", (new, 1, 0))
        new_id = c.lastrowid

        conn.commit()
        c.close()

        return '<p>The new task was inserted into the database, the ID is %s</p><a href="/todo">ToDo List</a>' % new_id

    else:
        return template('new_task.tpl')


@route('/edit/<no:int>', method='GET')
def edit_item(no):

    if request.GET.save:
        edit = request.GET.task.strip()
        status = request.GET.status.strip()

        if status == 'open':
            status = 1
        else:
            status = 0

        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("UPDATE todo SET task = ?, status = ? WHERE id LIKE ?", (edit, status, no))
        conn.commit()

        return '<p>The item number %s was successfully updated</p>\n<a href="/todo">ToDo List</a>' % no
    else:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT task FROM todo WHERE id LIKE ?", (str(no)))
        cur_data = c.fetchone()

        return template('edit_task', old=cur_data, no=no)


@route('/item<item:re:[0-9]+>')
def show_item(item):

        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT task FROM todo WHERE id LIKE ?", (item,))
        result = c.fetchall()
        c.close()

        if not result:
            return 'This item number does not exist!'
        else:
            return 'Task: %s' % result[0]


@route('/help')
def help():

    return static_file('/static/help.html', root='.')


@route('/json<json:re:[0-9]+>')
def show_json(json):

    conn = sqlite3.connect('todo.db')
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