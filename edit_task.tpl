%#template for editing a task
%#the template expects to receive a value for "no" as well a "old", the text of the selected ToDo item
<link href='/static/style.css' rel='stylesheet'>
<p>Edit the task with ID = {{no}}</p>
<form action="/edit/{{no}}" method="get">
    <input type="text" name="task" value="{{old}}" size="100" maxlength="100">
    <select name="status">
        <option>open</option>
        <option>closed</option>
    </select>
    <input type="submit" value="delete" name="delete">
    <br>
    <textarea id="description" name="description" rows="4" cols="50" placeholder="Description (Optional)">{{old_desc}}</textarea>
    <br>
        <select name="priority">
        <option selected disabled hidden>{{old_priority}}</option>
        <option value="0">Low</option>
        <option value="1">Medium</option>
        <option value="2">High</option>
        </select>
    <br>
        <input type="date" name="due_date" value="{{old_due}}" min="{{created}}">
    <br>
    <input type="submit" name="save" value="save">
</form>
