<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task Viewer</title>
    <link href='/static/style.css' rel='stylesheet'>
</head>

<body>
    <div class="viewer_page">
        <h1>Viewing Task with id #{{no}}</h1>
        <h2>Currently {{status}}</h2>
        <p>Name: {{task}}</p>
        <p>Progress: {{int(progress) * 12.5}}%</p>
        <textarea id="description" name="description" rows="5" cols="35" disabled>{{description}}</textarea>
        %if priority == 0:
            <p>Priority: Low</p>
        %elif priority == 1:
            <p>Priority: Medium</p>
        %elif priority == 2:
            <p>Priority: High</p>
            %end
        <p>Date Created: {{created[-2]}}{{created[-1]}}/{{created[-5]}}{{created[-4]}}/{{created[0]}}{{created[1]}}{{created[2]}}{{created[3]}}</p>
        <p>Due Date: {{due[-2]}}{{due[-1]}}/{{due[-5]}}{{due[-4]}}/{{due[0]}}{{due[1]}}{{due[2]}}{{due[3]}}</p>
        <a href='/todo' class="viewer_button"><button class="button_1">Back</button></a>
    </div>
</body>
</html>