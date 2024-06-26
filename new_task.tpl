<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New Task</title>
    <link href='/static/style.css' rel='stylesheet'>
</head>
<body>
    <h1>Add a new task to the ToDo list:</h1>
    <form action="/new" method="GET">
        <input type="text" size="100" maxlength="100" name="task">
        
        <textarea id="description" name="description" rows="4" cols="50" placeholder="Description (Optional)"></textarea>
        <br>
        <input type="submit" name="save" value="save">
    </form>
</body>
</html>