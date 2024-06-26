<?php include "db_conn.php"; ?>
<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="utf-8">
 <meta http-equiv="X-UA-Compatible" content="IE=edge">
 <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
 <meta name="description" content="">
 <meta name="author" content="">
 <title>BugBounty Tools - Dashboard</title>

 <link href="css/bootstrap.min.css" rel="stylesheet">
 <link href="font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">
 <link href="css/sb-admin.css" rel="stylesheet">
</head>
<body class="bg-dark">
 <div class="container">
   <div class="card card-login mx-auto mt-5">
     <div class="card-header">Login</div>
     <div class="card-body">
       <form method="post" action="login2.php">
          
          <?php if (isset($_GET['error'])) { ?>
            <p class="error"><?php echo $_GET['error']; ?></p>
        <?php } ?>
         <div class="form-group">
           <label for="exampleInputEmail1">Username</label>
           <input class="form-control"  type="text" name="uname">
         </div>
         <div class="form-group">
           <label for="exampleInputPassword1">Password</label>
           <input class="form-control"  type="password" name="password">
         </div>
         <div class="form-group">
           <div class="form-check">
             <label class="form-check-label">
               <input class="form-check-input" type="checkbox"> Remember Password</label>
           </div>
         </div>
         <button type="submit" class="btn btn-primary btn-block" name="login_user">Login</button>
       </form>
       <div class="text-center">
         <a class="d-block small mt-3" href="register.php">Register an Account</a>
      <!-- <a class="d-block small" href="forgot-password.php">Forgot Password?</a>-->
       </div>
     </div>
   </div>
 </div>

 <script src="js/jquery.min.js"></script>
 <script src="js/bootstrap.bundle.min.js"></script>
 <script src="js/jquery.easing.min.js"></script>
</body>
</html>