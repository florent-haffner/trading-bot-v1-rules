from datetime import datetime, timedelta

from src.data.missionMongoUtils import getAllMissions
from src.data.tradeEventUtils import insertTradeEvent
from src.data.transactionMongoUtils import getAllTransaction, updateTransactionById
from src.helpers.dateHelper import DATE_STR
from src.services.krakenTradeService import getLastPrice
from src.services.tradeEventService import generateTradeEventDTO
from src.services.transactionService import updateToCompleteTransaction


def close_everything():
    missions = getAllMissions()
    interval = missions[0]['context']['interval']
    transactions = list(getAllTransaction())
    print('nbr transaction', len(transactions))

    transactions_to_closed: list = []
    for transaction in transactions:
        try:
            if transaction['sell']:
                pass
        except KeyError:
            transactions_to_closed.append(transaction)

    nbr_transactions_not_closed = len(transactions_to_closed)
    print('Nbr of transactions not closed', nbr_transactions_not_closed)
    if nbr_transactions_not_closed == 0:
        print('No transactions to closed')
        return

    previous_hour = datetime.now() - timedelta(hours=1)
    for transaction in transactions_to_closed:
        transactionId = transaction['_id']
        time = datetime.strptime(transaction['buy']['time'], DATE_STR)
        if time < previous_hour:
            print('Closing', transactionId)
            last_price = getLastPrice(transaction['buy']['fields']['asset'], 'EUR')
            volume = transaction['buy']['fields']['quantity']
            # print('volume', volume, 'price', last_price, 'in euro:', last_price * volume)
            type_of_trade = 'sell'
            point = generateTradeEventDTO(type_of_trade=type_of_trade,
                                          volume_to_buy=volume,
                                          asset=transaction['buy']['fields']['asset'],
                                          interval=interval,
                                          price=last_price)

            print('Updating', transactionId, 'to complete transaction')
            result = updateToCompleteTransaction(id=transactionId,
                                                 key=type_of_trade,
                                                 points=point)
            if result:
                del point['time']
                insertTradeEvent([point])

            # Finally update to make sure the transaction is closed
            updateTransactionById(transactionId, 'forced_closed', True)


if __name__ == '__main__':
    close_everything()
