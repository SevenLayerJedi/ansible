<?php 
    session_start();
    if (isset($_SESSION['id']) && isset($_SESSION['user_name'])){
    header("Location: home.php");
    exit();
    }
?>


<!DOCTYPE html>
<html>
<head>
    <title>LOGIN</title>
    <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
     <form action="login2.php" method="post">
        <h2>LOGIN</h2>
        <?php if (isset($_GET['error'])) { ?>
            <p class="error"><?php echo $_GET['error']; ?></p>
        <?php } ?>
        <label>User Name</label>
        <input type="text" name="uname" placeholder="User Name"><br>
        <label>Password</label>
        <input type="password" name="password" placeholder="Password"><br> 
        <button type="submit">Login</button>
     </form>
</body>
</html>
