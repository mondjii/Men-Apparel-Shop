import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(name:str, subject:str,  pnum:str ,email:str ,mess:str,) -> None:
    sender_account = {'email': 'sample sender@gmail.com', 'password': 'sample app key', 'name': 'Men Apparel@ContactUs'}

    recipient_email = 'sample receiver@gmail.com'

    message = MIMEMultipart()
    message['From'] = f'{sender_account["name"]} <{sender_account["email"]}>'
    message['To'] = recipient_email
    message['Subject'] = f'{subject}'

    body = f'''
    Name: {name}
    Phone Number: 63+ {pnum}
    Email: {email}
    Message:
    {mess}
    '''
    message.attach(MIMEText(body,'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()  # Use TLS for security
        server.login(sender_account['email'], sender_account['password'])
        text = message.as_string()
        server.sendmail(sender_account['email'], recipient_email, text)
        server.quit()

    print("Email sent successfully!")
