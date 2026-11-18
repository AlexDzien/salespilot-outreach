import unittest
from email.message import EmailMessage

from salespilot.reply_text import message_text, new_reply_text


class ReplyTextTest(unittest.TestCase):
    def test_new_text_excludes_original_message_and_attachments(self):
        message = EmailMessage()
        message.set_content("Proszę o kontakt jutro.\n\n> Przesyłam wcześniejszą ofertę.")
        message.add_attachment("Attachment text", subtype="plain", filename="notes.txt")
        self.assertEqual(new_reply_text(message_text(message)), "Proszę o kontakt jutro.")

    def test_html_only_conversation_preserves_reply_boundary(self):
        message = EmailMessage()
        message.set_content(
            "<p>Dziękuję za informację.</p><blockquote><p>Poprzednia wiadomość</p></blockquote>",
            subtype="html",
        )
        self.assertEqual(new_reply_text(message_text(message)), "Dziękuję za informację.")
