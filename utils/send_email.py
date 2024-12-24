# Import the SandMailHandler class from the mail handler module
from core.mail_handler.sand_mail import SandMailHandler

# Initialize an instance of the SandMailHandler class
mail_handler = SandMailHandler()

def send_forgot_password_mail(to, context):
    """
    Sends a 'Forgot Password' email to the specified recipient.

    Parameters:
    to (str): The recipient's email address.
    context (dict): A dictionary containing context variables for the email template.

    Returns:
    None
    """
    template = 'email/forgot_password.html'  # Path to the email template for 'Forgot Password'
    mail_handler.send_email(to, context, template)  # Send the email using the mail handler

def send_welcome_mail(to, context):
    """
    Sends a 'Welcome' email to the specified recipient.

    Parameters:
    to (str): The recipient's email address.
    context (dict): A dictionary containing context variables for the email template.

    Returns:
    None
    """
    template = 'email/welcome_mail.html'  # Path to the email template for 'Welcome'
    mail_handler.send_email(to, context, template)  # Send the email using the mail handler

def send_welcome_mail_with_password(to, context):
    """
    Sends a 'Welcome with Password' email to the specified recipient.

    Parameters:
    to (str): The recipient's email address.
    context (dict): A dictionary containing context variables for the email template.

    Returns:
    None
    """
    template = 'email/welcome_mail_with_password.html'  # Path to the email template for 'Welcome with Password'
    mail_handler.send_email(to, context, template)  # Send the email using the mail handler
