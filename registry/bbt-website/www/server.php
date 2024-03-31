<?php
session_start();
// initializing variables
$username = "";
$email    = "";
$errors = array();
// connect to the database
$db = mysqli_connect('10.200.1.91', 'admin', 'admin', 'bbt');