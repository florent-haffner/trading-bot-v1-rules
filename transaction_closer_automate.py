from datetime import datetime, timedelta

from src.data.missionMongoUtils import getAllMissions
from src.data.transactionMongoUtils import getAllTransaction, updateTransactionById
from src.helpers.dateHelper import DATE_STR
from src.helpers.params import MAXIMUM_PERCENTAGE_EUR
from src.services.krakenTradeService import getAccountBalance, getLastPrice

def close_everything():
    missions = getAllMissions()
    nbr_asset_on_trade = len(missions[0]['context']['assets'])
    transactions = list(getAllTransaction())
    print('nbr transaction', len(transactions))

    transactions_to_closed: list = []
    for transaction in transactions:
        try:
            if transaction['sell']:
                pass
        except KeyError:
            transactions_to_closed.append(transaction)

    print('Nbr of transactions to closed', len(transactions_to_closed))
    now = datetime.now()
    previous_hour = now - timedelta(hours=1)
    for transaction in transactions_to_closed:
        id = transaction['_id']
        time = datetime.strptime(transaction['buy']['time'], DATE_STR)
        if time < previous_hour:
            last_price = getLastPrice(transaction['buy']['fields']['asset'], 'EUR')
            volume = transaction['buy']['fields']['quantity']
            print('volume', volume, 'price', last_price, 'in euro:', last_price * volume)

        # # TODO -> wait to make sure before closing the transaction
        # updateTransactionById(id, 'forced_closed', False)


if __name__ == '__main__':
    close_everything()
