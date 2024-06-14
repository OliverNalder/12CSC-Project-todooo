<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>Login:</h1>
    <form action="/login" method="GET">
        <input type="text" size="100" maxlength="100" placeholder="{{user_text}}" name="username">
        <input type="password" size="100" maxlength="100" minlength="8" placeholder="{{password_text}}" name="password">
        <input type="submit" name="save" value="save">
    </form>
</body>
</html>