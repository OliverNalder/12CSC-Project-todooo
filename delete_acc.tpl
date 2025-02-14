<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Delete Account</title>
    <link href='/static/style.css' rel='stylesheet'>
</head>
<body>
    <div class="left_title">
        <h1>Login to delete account:</h1>
    </div>
    <form action="/delete_account" method="GET">
        <input type="text" size="100" maxlength="100" placeholder="{{user_text}}" name="username">
        <br>
        <input type="password" size="100" maxlength="100" minlength="8" placeholder="{{password_text}}" name="password">
        <br>
        <input type="submit" name="delete_acc" value="Delete Account">
    </form>
    <a href='/' class="alt_td"><button class="button_1">Back</button></a>
</body>
</html>