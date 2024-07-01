<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New Task</title>
    <link href='/static/style.css' rel='stylesheet'>
</head>
<body>
    <h1>Add a new task to the To Do list:</h1>
    <form action="/new" method="GET">
        <input type="text" size="100" maxlength="100" name="task" placeholder="Task Name:">
        <br>
        <textarea id="description" name="description" rows="8" cols="100" placeholder="Description (Optional)"></textarea>
        <br>
            <p>Priority:</p>
            <select name="priority">
            <option value="0">Low</option>
            <option value="1">Medium</option>
            <option value="2">High</option>
            </select>
        <br>
            <input type="date" name="due_date" value="{{date}}" min="{{date}}">
        <br>
        <input type="submit" name="save" value="save">
        <a href='/todo'>Back</a>
    </form>
</body>
</html>
