from relay.aws import AWS
from relay.logger import logger
from email.mime.text import MIMEText
from relay.config import AWS_SES_CONFIG_SET, REPLY_EMAIL
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from relay.locker_api import store_reply_record


class SES(AWS):
    def __init__(self):
        super().__init__()
        self.service = 'ses'

    @staticmethod
    def add_body_to_message(msg, message_body):
        charset = "UTF-8"
        # Create a multipart/alternative child container.
        msg_body = MIMEMultipart("alternative")

        # Encode the text and HTML content and set the character encoding.
        # This step is necessary if you're sending a message with characters
        # outside the ASCII range.
        if "Text" in message_body:
            body_text = message_body["Text"]["Data"]
            text_part = MIMEText(body_text.encode(charset), "plain", charset)
            msg_body.attach(text_part)
        if "Html" in message_body:
            body_html = message_body["Html"]["Data"]
            html_part = MIMEText(body_html.encode(charset), "html", charset)
            msg_body.attach(html_part)
        # Attach the multipart/alternative child container to the multipart/mixed
        # parent container.
        msg.attach(msg_body)
        return msg

    @staticmethod
    def add_attachments_to_message(msg, attachments):
        # attach attachments
        for actual_att_name, attachment in attachments:
            # Define the attachment part and encode it using MIMEApplication.
            attachment.seek(0)
            att = MIMEApplication(attachment.read())

            # Add a header to tell the email client to treat this
            # part as an attachment, and to give the attachment a name.
            att.add_header("Content-Disposition", "attachment", filename=actual_att_name)
            # Add the attachment to the parent container.
            msg.attach(att)
            attachment.close()
        return msg

    @staticmethod
    def start_message_with_headers(subject, from_address, to_address, reply_address):
        # Create a multipart/mixed parent container.
        msg = MIMEMultipart("mixed")
        # Add subject, from and to lines.
        msg["Subject"] = subject
        msg["From"] = from_address
        msg["To"] = to_address
        msg["Reply-To"] = reply_address
        return msg

    def ses_send_raw_email(self, from_address, to_address, subject, message_body, attachments, mail,
                           reply_address=REPLY_EMAIL):
        msg_with_headers = self.start_message_with_headers(subject, from_address, to_address, reply_address)
        msg_with_body = self.add_body_to_message(msg_with_headers, message_body)
        msg_with_attachments = self.add_attachments_to_message(msg_with_body, attachments)
        try:
            ses_response = self.client.send_raw_email(
                Source=from_address,
                Destinations=[to_address],
                RawMessage={
                    "Data": msg_with_attachments.as_string(),
                },
                ConfigurationSetName=AWS_SES_CONFIG_SET,
            )

            store_reply_record(mail, ses_response)
        except ClientError as e:
            logger.error(f'[!] ses_client_error_raw_email:{e.response["Error"]}')
            return False
        return True


ses_client = SES()
