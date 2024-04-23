import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename

smtp_server = "smtp.titan.email"
smtp_port = 465
smtp_username = "test@enormt.se"
smtp_password = "Test123@"
smtp_receiver="mouayad1998@hotmail.com"

email_subject= "Test Email"
email_body = """\
Hi,
How are you?
Real Python has many great tutorials.
"""

files_to_attach = ['./test.pdf', './cover.txt']

def create_email(subject, sender_email, receiver_email, files_list, text_body):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    part1 = MIMEText(text_body, "plain")
    message.attach(part1)
    
    for file_path in files_list:
        with open(file_path, "rb") as file:
            part = MIMEApplication(
                file.read(),
                Name=basename(file_path)
            )
            part['Content-Disposition'] = f'attachment; filename="{basename(file_path)}"'
            message.attach(part)
    return message;
        
def send_email(smtp_server, port,username, password, receiver, message):
    try:
        # Use SMTP_SSL for a direct SSL connection
        with smtplib.SMTP_SSL(smtp_server, port) as server:
            server.login(username, password)
            server.sendmail(username, receiver, message.as_string())
            print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


