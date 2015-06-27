from bot import Bot

class ModuleBase:
    def __init__(self, bot):
        self.name = "Piconche ne pige pas le python"
        self.bot = bot

    @staticmethod
    def checkForAttribute(object, attribute):
        exists = getattr(object, attribute, None)
        return exists is not None
        
    def notify_forward_from(self, message_id, from_attr, date, chat, forward_from):
        pass

    def notify_forward_date(self, message_id, from_attr, date, chat, forward_date):
        pass

    def notify_reply_to_message(self, message_id, from_attr, date, chat, reply_to_message):
        pass

    def notify_text(self, message_id, from_attr, date, chat, text):
        pass

    def notify_audio(self, message_id, from_attr, date, chat, audio):
        pass

    def notify_document(self, message_id, from_attr, date, chat, document):
        pass

    def notify_photo(self, message_id, from_attr, date, chat, photo):
        pass

    def notify_sticker(self, message_id, from_attr, date, chat, sticker):
        pass

    def notify_video(self, message_id, from_attr, date, chat, video):
        pass

    def notify_contact(self, message_id, from_attr, date, chat, contact):
        pass

    def notify_location(self, message_id, from_attr, date, chat, location):
        pass

    def notify_new_chat_participant(self, message_id, from_attr, date, chat, new_chat_participant):
        pass

    def notify_left_chat_participant(self, message_id, from_attr, date, chat, left_chat_participant):
        pass

    def notify_new_chat_title(self, message_id, from_attr, date, chat, new_chat_title):
        pass

    def notify_new_chat_photo(self, message_id, from_attr, date, chat, new_chat_photo):
        pass

    def notify_delete_chat_photo(self, message_id, from_attr, date, chat, delete_chat_photo):
        pass

    def notify_group_chat_created(self, message_id, from_attr, date, chat, created):
        pass
