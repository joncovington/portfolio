<?php
ini_set("include_path", '/home/beehives/php:' . ini_get("include_path") );
error_reporting(E_ALL ^ E_NOTICE ^ E_DEPRECATED ^ E_STRICT);

include("/home/beehives/php/Mail.php");

echo("<p>" . $_POST('Name') . "</p>");
echo("<p>" . $_POST('Email') . "</p>");
echo("<p>" . $_POST('Message') . "</p>");
$host = "ssl://mail.joncovington.dev";
$username = "no_reply@joncovington.dev";
$password = "X!#h_C}1+ATM";
$port = "465";
$to = $_POST('Email');
$email_from = "no_reply@joncovington.dev";
$email_subject = "Test" ;
$email_body = "whatever you like" ;
$email_address = "no_reply@joncovington.dev";

$headers = array ('From' => $email_from, 'To' => $to, 'Subject' => $email_subject, 'Reply-To' => $email_address);
$smtp = Mail::factory('smtp', array ('host' => $host, 'port' => $port, 'auth' => true, 'username' => $username, 'password' => $password));
$mail = $smtp->send($to, $headers, $email_body);


if (PEAR::isError($mail)) {
echo("<p>" . $mail->getMessage() . "</p>");
} else {
echo("<p>Message successfully sent!</p>");
}
?>
// header("Location: ./index.html");
// die();

?>