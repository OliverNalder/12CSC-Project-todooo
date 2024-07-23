<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New Task</title>
    <link href='/static/style.css' rel='stylesheet'>
</head>
<body>
    <h1 class="left_heading">Add a new task to the To Do list:</h1>
    <form action="/new" method="GET">
        <input type="text" size="50" maxlength="100" name="task" placeholder="Task Name:">
        <br>
        <textarea id="description" name="description" rows="4" cols="49" placeholder="Description (Optional)"></textarea>
        <br>
            <p class="left_heading">Priority:</p>
        <br>
            <select name="priority" class="priority">
            <option value="0">Low</option>
            <option value="1">Medium</option>
            <option value="2">High</option>
            </select>
        <br>
            <input type="date" name="due_date" value="{{date}}" min="{{date}}" required>
        <br>
        <input type="submit" name="save" value="Save">
        
    </form>
    <a href='/todo' class="alt_td"><button class="button_1">Back</button></a>
</body>
</html>
