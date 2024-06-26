<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task Viewer</title>
</head>
<body>
    <h1>Viewing Task with id #{{no}}</h1>
    <h3>Currently {{status}}</h3>
    <p>{{task}}{{int(progress) * 12.5}}{{description}}</p>
</body>
</html>