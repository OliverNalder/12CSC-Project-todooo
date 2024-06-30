<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Signup</title>
    <link href='/static/style.css' rel='stylesheet'>
</head>
<body>
    <div class="left_title">
        <h1>Create Account:</h1>
    </div>
    <form action="/signup" method="GET">
        <input type="text" size="100" maxlength="100" placeholder="{{user_text}}" name="username" required>
        <br>
        <input type="text" size="100" maxlength="100" minlength="8" placeholder="Password:" name="password" required>
        <br>
        <input type="submit" name="save" value="save">
    </form>
</body>
</html>