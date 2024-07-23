<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edit Task</title>
    <link href='/static/style.css' rel='stylesheet'>
</head>
<body>
    <h1 class="left_heading">Edit the task with ID = {{no}}</h1>
    <form action="/edit/{{no}}" method="get">
        <input type="text" name="task" value="{{old}}" size="50" maxlength="100">
        <select name="status">
            <option>Open</option>
            <option>Closed</option>
        </select>
        <input type="submit" value="Delete" name="delete">
        <br>
        <textarea id="description" name="description" rows="4" cols="49" placeholder="Description (Optional)">{{old_desc}}</textarea>
        <br>
            <p class="left_heading">Priority:</p>
        <br>
            <select name="priority" class="priority">
            <option selected disabled hidden>{{old_priority}}</option>
            <option value="0">Low</option>
            <option value="1">Medium</option>
            <option value="2">High</option>
            </select>
        <br>
            <input type="date" name="due_date" value="{{old_due}}" min="{{created}}" required>
        <br>
        <input type="submit" name="save" value="Save">
    </form>
    <a href='/todo' class="alt_td"><button class="button_1">Back</button></a>
</body>
</html>