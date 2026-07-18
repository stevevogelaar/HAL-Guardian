<?php
// sample: deliberately flawed login handler for demo
$host = "localhost";
$user = "root";
$pass = "P@ssw0rd123";
$conn = new mysqli($host, $user, $pass, "app_db");

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$username = $_POST['username'];
$password = $_POST['password'];

$query = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
$result = $conn->query($query);

if ($result && $result->num_rows > 0) {
    $row = $result->fetch_assoc();
    echo "Welcome, " . $row['username'];
    // debug
    var_dump($row);
} else {
    echo "Login failed";
}

// TODO: add logout
// TODO: hash passwords
?>
