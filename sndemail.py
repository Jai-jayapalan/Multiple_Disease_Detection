import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def send_email(message, to_email, image_path):
    # Email setup
    from_email = "jaijayathilak@gmail.com"
    from_password = "pexj wxdp thxc kgas"

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Disease Detection Result"

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(message, 'plain'))
    
    if image_path is not None:
        with open(image_path, 'rb') as img_file:
            img = MIMEImage(img_file.read())
            img.add_header('Content-Disposition', 'attachment', filename=image_path.split('/')[-1])
            msg.attach(img)

    try:
        # Create server object with SSL option
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        
        # Login to the email server
        server.login(from_email, from_password)
        
        # Send the email
        server.send_message(msg)
        
        # Terminate the SMTP session and close the connection
        server.quit()
        
        print("Successfully sent email to %s:" % (msg['To']))
    except smtplib.SMTPException as e:
        print("Error: unable to send email. Error detail:", e)
        
def sends_email(message, to_email):
    # Email setup
    from_email = "jaijayathilak@gmail.com"
    from_password = "pexj wxdp thxc kgas"

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Disease Detection Result"

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Create server object with SSL option
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        
        # Login to the email server
        server.login(from_email, from_password)
        
        # Send the email
        server.send_message(msg)
        
        # Terminate the SMTP session and close the connection
        server.quit()
        
        print("Successfully sent email to %s:" % (msg['To']))
    except smtplib.SMTPException as e:
        print("Error: unable to send email. Error detail:", e)

# Example usage
# send_email("Hello, this is a test email.", "jayjayathilak@gmail.com", "./media/patient00085_study1_view1_frontal.jpg")