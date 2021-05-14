from typing import Dict, Any, List
from datetime import datetime
from json import dumps

from telethon import TelegramClient, sync  # DO NOT TOUCH THIS IMPORT
from telethon.tl.functions.contacts import GetContactsRequest
from telethon.tl.types import InputPeerUser

from src.helpers.dateHelper import SIMPLE_DATE_STR
from src.helpers.params import MAXIMUM_FEES
from src.secret.SECRET_CONSTANT import __TELEGRAM_APP_ID, __TELEGRAM_APP_HASH, __TELEGRAM_PHONE_NBR
from src.repository.missionRepository import getAllMissions
from src.repository.tradeTransactionRepository import getTransactionsByAsset
from src.services.timeseriesService import getTransactionPerDayAsset


def calculateWinLossPerTransactions(transactions):
    total = []
    for transaction in transactions:
        typeOfTrade = ['buy', 'sell']
        print(transaction)
        transactionAmount = []
        for trade in typeOfTrade:
            try:
                field = transaction[trade]['fields']
                amountPerTransaction = field['quantity'] * field['price']
                fees = amountPerTransaction * MAXIMUM_FEES
                net_amount = amountPerTransaction - fees
                transactionAmount.append(net_amount)
            except KeyError:
                pass

        if len(transactionAmount) == 1:
            current = -transactionAmount[0]
            total.append(current)
        else:
            totalPetTransaction = -transactionAmount[0] + transactionAmount[1]
            total.append(totalPetTransaction)

    totalAmount = 0
    for amountPerTransaction in total:
        totalAmount = totalAmount + amountPerTransaction

    return len(transactions), totalAmount


def getAllTransactionPerDay():
    print('\n[Getting all transaction per day]\n')
    missions = list(getAllMissions())
    for mission in missions:
        for asset in mission['context']['assets']:
            transactionsPerDay = list(getTransactionPerDayAsset(asset))
            print('Transaction per day', len(transactionsPerDay))


def calculateWInLossPerMission():
    print('\n[CALCULATING WIN/LOSS]\n')
    results: List = []
    missions = list(getAllMissions())
    for mission in missions:
        for asset in mission['context']['assets']:
            print('\n[', asset, '] -> Calculating win/loss pet asset')
            # transactionFromAsset = list(getTransactionsByAsset(asset))
            transactionFromAsset = list(getTransactionPerDayAsset(asset))
            nbrTransaction, amount = calculateWinLossPerTransactions(transactionFromAsset)

            dto: Dict[str, Any] = generateDTO(asset, nbrTransaction, round(amount, 3))
            print('Current analysis result', dto)
            results.append(dto)

    msg_to_send = f"""
    <p>[BOT ANALYSIS OF THE DAY]</p>
    <p>{datetime.now().strftime(SIMPLE_DATE_STR)}</p>
    <p>{ str(dumps(results, indent=2)) }</p>
    """
    sendMessage(msg_to_send)


def generateDTO(asset, nbr_transaction, amount_money):
    return {
        "asset": asset,
        "nbr_transactions": nbr_transaction,
        "amount_money": amount_money
    }


"""
    Use telegram to handle message send encrypted report to myself
"""
def sendMessage(message):
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
                print('[TELEGRAM] - Sending the following message', message)
                client.send_message(InputPeerUser(contact.id, contact.access_hash), message, parse_mode='html')

    except Exception as err:
        raise err

    client.disconnect()


if __name__ == '__main__':
    # getLastEventByTypeAndAsset('GRT', 'buy')

    calculateWInLossPerMission()

    # getAllTransactionPerDay()
