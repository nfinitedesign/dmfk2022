<?php
	use PHPMailer\PHPMailer\PHPMailer;
	use PHPMailer\PHPMailer\SMTP;
	use PHPMailer\PHPMailer\Exception;

	require_once __DIR__ . '/assets/contactform/Exception.php';
	require_once __DIR__ . '/assets/contactform/PHPMailer.php';
	require_once __DIR__ . '/assets/contactform/SMTP.php';

	$Name = $_POST['email-name'];
	$Email = $_POST['email-email'];
	$Subject = $_POST['email-subject'];
	$Message = $_POST['email-message'];
	$Category = $_POST['email-category');
	$Name  = $_POST['email-name'];

	$CopyFrom = 'DMFK2022 Freiburg - Fahrrad und Kurier Kru Freiburg e.V.';


    $DataReceived = ( !empty( $_REQUEST['submitted'] ) ) ? $_REQUEST['submitted'] : '';

    if( !empty( $DataReceived ) )
    {

        $name   = trim($_REQUEST['name']);
        $email  = trim($_REQUEST['email']);

        //You can now save this into database or use data to validate user or transactions

        echo "Name is :  $name";
        echo "<br>Email is : $email";
    }

	// passing true in constructor enables exceptions in PHPMailer
	$mail = new PHPMailer(true);

	try {
		// Server settings
		$mail->SMTPDebug = SMTP::DEBUG_OFF; // for detailed debug output
		$mail->isSMTP();
		$mail->Host = 'mail.zeus08.de';
		$mail->SMTPAuth = true;
		$mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
		$mail->Port = 587;

		$mail->Username = 'xxxxx';
		$mail->Password = 'xxxx+';

		// Sender and recipient settings
		$mail->setFrom('kontaktformular@dmfk2022.de', 'Kontaktformular DMFK Website');
		$mail->addAddress('lo0o0o0o0ngcat@gmail.com', 'Kontaktformular DMFK Website');
		$mail->addReplyTo($Email, $Name); // to set the reply to

		// Setting the email content
		$mail->IsHTML(true);
		$mail->Subject = "Send email using Gmail SMTP and PHPMailer";
		$mail->Body = 'HTML message body. <b>Gmail</b> SMTP email body.';
		$mail->AltBody = 'Plain text message body for non-HTML email client. Gmail SMTP email body.';

		$mail->send();
		echo "Email message sent.";
	} catch (Exception $e) {
		echo "Error in sending email. Mailer Error: {$mail->ErrorInfo}";
	}
?>