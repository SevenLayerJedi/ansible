<?php
$sname= "10.200.1.91";
$uname= "admin";
$password = "admin";
$db_name = "bbt";
$conn = mysqli_connect($sname, $uname, $password, $db_name);

if (!$conn) {
    echo "Connection failed!";
}
