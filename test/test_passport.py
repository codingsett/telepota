import time
import telepot
from telepot.utils import clean_data
import telepot.test_settings as st

class AdminBot(telepot.Bot):

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(chat_id)
        bot.sendAnimation(chat_id, open('TestFiles/tenor.gif', 'rb'), thumb=open('TestFiles/tenor.gif', 'rb'))

    def on_passport_data(self, msg):
        chat_id, passport_data = telepot.glance(msg, flavor='all_passport_data')
        output = clean_data(bot, passport_data, 'TestFiles/private.key')

    def on_poll_data(self, msg):
        poll_id, extra_data, chat_id = telepot.glance(msg, flavor='poll_data')
        print(poll_id, extra_data, chat_id)


TOKEN = st.TOKEN

bot = AdminBot(TOKEN)
bot.message_loop()
print('Send me a text message ...')

while 1:
    time.sleep(1)
