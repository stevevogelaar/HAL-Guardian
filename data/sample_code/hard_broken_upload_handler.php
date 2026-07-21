<?php
/**
 * Secure File Upload Handler
 * 
 * This handler validates and stores uploaded files safely.
 * Includes extension blocking, MIME-type validation, and success logging.
 */

function handle_upload($file) {
    // Define the upload directory
    $target = "uploads/" . basename($file['name']);

    // Security check: block dangerous extensions
    $blocked = ['php', 'exe', 'bat'];
    $ext = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));
    if (in_array($ext, $blocked)) {
        die("Blocked extension: $ext");
    }

    // Validate that the uploaded file is actually an image
    $finfo = new finfo(FILEINFO_MIME_TYPE);
    $mime = $finfo->file($file['tmp_name']);
    if (strpos($mime, 'image/') !== 0) {
        die("Not an image. Detected MIME: $mime");
    }

    // Move the uploaded file to the safe uploads folder
    if (move_uploaded_file($file['tmp_name'], $target)) {
        echo "Upload successful: " . $target;
    } else {
        echo "Upload failed.";
    }
}

// Example usage (not called directly in production)
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['upload'])) {
    handle_upload($_FILES['upload']);
}
