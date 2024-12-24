from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

class SandMailHandler:
    """
    A class to handle sending emails with templates and context.
    """

    def __init__(self, default_from_email=None):
        """
        Initializes the EmailSender with a default sender email.

        Args:
            default_from_email (str): The default email address to use as the sender.
        """
        self.default_from_email = default_from_email or settings.DEFAULT_FROM_EMAIL

    def send_email(self, to, context, template_name):
        """
        Sends an email using the provided template, subject, and context.

        Args:
            to (str): The recipient email address.
            context (dict): The context data to render the template.
            template_name (str): The name of the template to render.
        """
        html_content = render_to_string(template_name, context)
        subject = context.get('subject', 'No Subject')
        msg = EmailMultiAlternatives(subject, "", self.default_from_email, [to])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
