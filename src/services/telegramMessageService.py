from telethon import TelegramClient, sync  # DO NOT REMOVE SYNC
from telethon.tl.functions.contacts import GetContactsRequest
from telethon.tl.types import InputPeerUser

from src.secret.SECRET_CONSTANT import __TELEGRAM_APP_ID, __TELEGRAM_APP_HASH, __TELEGRAM_PHONE_NBR


def send_message(message):
    """
    Use telegram to handle message send encrypted report to myself
    :param message: the message to send
    :return: None
    """
    client = TelegramClient('session', __TELEGRAM_APP_ID, __TELEGRAM_APP_HASH)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(__TELEGRAM_PHONE_NBR)
        client.sign_in(__TELEGRAM_PHONE_NBR, input('Enter the code: '))
    try:
        contacts = client(GetContactsRequest(0))
        for contact in contacts.users:
            if contact.username == 'nelth_fr':
                print(contact.id, contact.access_hash)
                print('[TELEGRAM] - Sending analysis results by message.')
                client.send_message(InputPeerUser(contact.id, contact.access_hash), message, parse_mode='html')
    except Exception as err:
        raise err
    client.disconnect()


if __name__ == '__main__':
    send_message('TEST_CONNECTION')
