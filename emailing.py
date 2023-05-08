import smtplib
# for more complex email massages
from email.message import EmailMessage
import ssl
import os
# gives metadata about images
import imghdr

SENDER = 'peychev.vn@gmail.com'
RECEIVER = 'peychev.vn@gmail.com'
PASSWORD = os.getenv('PASSWORD')

def send_email(image_path):
    email_message = EmailMessage()
    email_message['Subject'] = 'A new customer showed up!'
    email_message.set_content('Hey, there is a new customer')

    # we read in binary mode as it is an image, not a text file
    with open(image_path, 'rb') as file:
        content = file.read()

    # we need to specify if it is png or jpg or whatever in subtype
    email_message.add_attachment(content, maintype='image', subtype=imghdr.what(None, content))

    # Creating gmail server by setting host
    gmail = smtplib.SMTP('smtp.gmail.com', 587)

    # Start the server
    gmail.ehlo()
    gmail.starttls()

    # Login to gmail of the sender
    gmail.login(SENDER, PASSWORD)

    # Send email
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())

    # Quit SMTP object at the end
    gmail.quit()


if __name__ == '__main__':
    send_email(image_path='images/100.png')

