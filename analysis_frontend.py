from tokenize import String
from typing import Dict, Any, List
from datetime import datetime
from json import dumps

from telethon import TelegramClient, sync  # DO NOT TOUCH THIS IMPORT
from telethon.tl.functions.contacts import GetContactsRequest
from telethon.tl.types import InputPeerUser

from src.helpers.dateHelper import SIMPLE_DATE_STR
from src.helpers.params import MAXIMUM_FEES
from src.data.analysisMongoUtils import create_domain_object, insert_analysis
from src.secret.SECRET_CONSTANT import __TELEGRAM_APP_ID, __TELEGRAM_APP_HASH, __TELEGRAM_PHONE_NBR
from src.data.missionMongoUtils import getAllMissions
from src.data.transactionMongoUtils import get_transactions_by_asset
from src.services.transactionService import getTransactionPerDayAsset, \
    get_complete_transaction_from_last_hours_per_asset


def calculate_win_loss_per_transactions(transactions):
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


# TODO -> not sure still usefull
"""
def get_all_transactions():
    print('\n[Getting all transaction]\n')
    missions = list(getAllMissions())
    transactions = {}
    for mission in missions:
        for asset in mission['context']['assets']:
            transactionsPerDay = list(get_transactions_by_asset(asset))
            print('Nbr of transaction', asset, ':', len(transactionsPerDay))
            transactions[asset] = transactionsPerDay
    return transactions
"""


# TODO -> not sure still usefull
"""
def get_all_transaction_per_day():
    print('\n[Getting all transaction per day]\n')
    missions = list(getAllMissions())
    transactions = {}
    for mission in missions:
        for asset in mission['context']['assets']:
            transactionsPerDay = list(get_complete_transaction_from_last_hours_per_asset(asset))
            print('Nbr of transaction', asset, ':', len(transactionsPerDay))
            transactions[asset] = transactionsPerDay
    return transactions
"""


def calculate_win_and_loss_per_mission(store_results: bool):
    print('\n[CALCULATING WIN/LOSS]\n')
    results: List = []
    missions = list(getAllMissions())
    for mission in missions:
        for asset in mission['context']['assets']:
            print('\n[', asset, '] -> Calculating win/loss pet asset')
            # transactionFromAsset = list(getTransactionsByAsset(asset))
            transactionFromAsset = list(getTransactionPerDayAsset(asset))
            print(transactionFromAsset)
            nbrTransaction, amount, beginningAmount = calculate_win_loss_per_transactions(transactionFromAsset)

            dto: Dict[str, Any] = generate_dto(asset, round(beginningAmount, 2), nbrTransaction, round(amount, 3))
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

    dto: Dict[str, Any] = generate_dto(asset=asset,
                                       beginning_amount=round(amountSum, 2),
                                       nbr_transactions=nbrTransactionSum,
                                       result=resultsSum)
    results.append(dto)

    # Store mock on MongoDB
    data = create_domain_object(results, 'daily')
    print('Analysis results')
    if store_results:
        insert_analysis(data)

        msg_to_send = f"""
        <p>[BOT ANALYSIS OF THE DAY]</p>
        <p>{datetime.now().strftime(SIMPLE_DATE_STR)}</p>
        <p>{ str(dumps(results, indent=2)) }</p>
        """
        send_message(msg_to_send)


def generate_dto(asset, beginning_amount, nbr_transactions, result):
    return {
        "asset": asset,
        "beginning_amount": beginning_amount,
        "nbr_transactions": nbr_transactions,
        "result": result,
        "percent": round(result * 100 / beginning_amount, 2) if beginning_amount else 0
    }


def send_message(message):
    """
        Use telegram to handle message send encrypted report to myself
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
    calculate_win_and_loss_per_mission(store_results=False)
