<?php
session_start();
// initializing variables
$username = "admin";
$email    = "admin";
$db_server = "10.200.1.91";
$db_port = "3306";
$errors = array();
// connect to the database
$db = mysqli_connect('localhost', 'root', '', 'registration');