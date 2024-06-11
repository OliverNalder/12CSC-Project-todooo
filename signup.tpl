<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Signup</title>
</head>
<body>
    <h1>Create Account:</h1>
    <form action="/new" method="GET">
        <input type="text" size="100" maxlength="100" placeholder="{{user_text}}" name="username">
        <input type="text" size="100" maxlength="100" minlength="8" placeholder="Password" name="password">
        <input type="submit" name="save" value="save">
    </form>
</body>
</html>