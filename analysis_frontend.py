from tokenize import String
from typing import Dict, Any, List
from datetime import datetime
from json import dumps

from telethon import TelegramClient, sync  # DO NOT TOUCH THIS IMPORT
from telethon.tl.functions.contacts import GetContactsRequest
from telethon.tl.types import InputPeerUser

from src.helpers.dateHelper import SIMPLE_DATE_STR
from src.helpers.params import MAXIMUM_FEES
from src.data.analysisMongoUtils import createDomainObject, insertAnalysis
from src.secret.SECRET_CONSTANT import __TELEGRAM_APP_ID, __TELEGRAM_APP_HASH, __TELEGRAM_PHONE_NBR
from src.data.missionMongoUtils import getAllMissions
from src.data.transactionMongoUtils import getTransactionsByAsset
from src.services.transactionService import getTransaction, getTransactionPerDayAsset


def calculateWinLossPerTransactions(transactions):
    total = []
    beginningAmount = 0
    for transaction in transactions:
        typeOfTrade = ['buy', 'sell']
        print(transaction)
        transactionAmount = []
        for trade in typeOfTrade:
            try:
                field = transaction[trade]['fields']
                amountPerTransaction = field['quantity'] * field['price']

                if not beginningAmount:
                    beginningAmount = amountPerTransaction

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

    return len(transactions), totalAmount, beginningAmount


def getAllTransactions():
    print('\n[Getting all transaction]\n')
    missions = list(getAllMissions())
    transactions = {}
    for mission in missions:
        for asset in mission['context']['assets']:
            transactionsPerDay = list(getTransactionsByAsset(asset))
            print('Nbr of transaction', asset, ':', len(transactionsPerDay))
            transactions[asset] = transactionsPerDay
    return transactions


def getAllTransactionPerDay():
    print('\n[Getting all transaction per day]\n')
    missions = list(getAllMissions())
    transactions = {}
    for mission in missions:
        for asset in mission['context']['assets']:
            transactionsPerDay = list(getTransactionPerDayAsset(asset))
            print('Nbr of transaction', asset, ':', len(transactionsPerDay))
            transactions[asset] = transactionsPerDay
    return transactions


def calculateWInLossPerMission():
    print('\n[CALCULATING WIN/LOSS]\n')
    results: List = []
    missions = list(getAllMissions())
    for mission in missions:
        for asset in mission['context']['assets']:
            print('\n[', asset, '] -> Calculating win/loss pet asset')
            # transactionFromAsset = list(getTransactionsByAsset(asset))
            transactionFromAsset = list(getTransactionPerDayAsset(asset))
            print(transactionFromAsset)
            nbrTransaction, amount, beginningAmount = calculateWinLossPerTransactions(transactionFromAsset)

            dto: Dict[str, Any] = generateDTO(asset, round(beginningAmount, 2), nbrTransaction, round(amount, 3))
            print('Current analysis result', dto)
            results.append(dto)

    # Calculating the overall percentage
    asset: String = 'total'
    amountSum: int = 0
    nbrTransactionSum: int = 0
    resultsSum: int = 0
    for res in results:
        amountSum = amountSum + res['beginning_amount']
        nbrTransactionSum = nbrTransactionSum + res['nbr_transactions']
        resultsSum = resultsSum + res['result']

    dto: Dict[str, Any] = generateDTO(asset=asset,
                                      beginning_amount=round(amountSum, 2),
                                      nbr_transactions=nbrTransactionSum,
                                      result=resultsSum)
    results.append(dto)

    # Store mock on MongoDB
    data = createDomainObject(results, 'daily')
    insertAnalysis(data)

    msg_to_send = f"""
    <p>[BOT ANALYSIS OF THE DAY]</p>
    <p>{datetime.now().strftime(SIMPLE_DATE_STR)}</p>
    <p>{ str(dumps(results, indent=2)) }</p>
    """
    sendMessage(msg_to_send)


def generateDTO(asset, beginning_amount, nbr_transactions, result):
    return {
        "asset": asset,
        "beginning_amount": beginning_amount,
        "nbr_transactions": nbr_transactions,
        "result": result,
        "percent": round(result * 100 / beginning_amount, 2) if beginning_amount else 0
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
    calculateWInLossPerMission()
