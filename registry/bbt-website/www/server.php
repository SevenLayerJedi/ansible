<?php
session_start();
// initializing variables
$username = "admin";
$email    = "admin";
$db_server = "10.200.1.91";
$dbname = "bbt";
$errors = array();
// connect to the database
$db = mysqli_connect($servername, $username, $password, $dbname);
