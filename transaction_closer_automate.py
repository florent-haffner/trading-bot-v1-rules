from datetime import datetime, timedelta

from src.data.missionMongoUtils import get_all_missions
from src.data.tradeEventUtils import insert_trade_event
from src.data.transactionMongoUtils import update_transaction_by_id, get_all_transactions_since_midnight
from src.helpers.dateHelper import DATE_STR
from src.services.krakenTradeService import get_last_price
from src.services.tradeEventService import generate_trade_event_dto
from src.services.transactionService import update_to_complete_transaction


def close_everything(nbr_hours_before_closing_transaction: int):
    missions = get_all_missions()
    interval = missions[0]['context']['interval']
    transactions = list(get_all_transactions_since_midnight())
    print('nbr transactions', len(transactions))

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

    tree_hours_before = datetime.now() - timedelta(hours=nbr_hours_before_closing_transaction)
    for transaction in transactions_to_closed:
        transactionId = transaction['_id']
        time = datetime.strptime(transaction['buy']['time'], DATE_STR)

        if time < tree_hours_before:
            print('Closing', transactionId)
            last_price = get_last_price(transaction['buy']['fields']['asset'], 'EUR')
            volume = transaction['buy']['fields']['quantity']
            type_of_trade = 'sell'

            point = generate_trade_event_dto(type_of_trade=type_of_trade,
                                             quantity=volume,
                                             asset=transaction['buy']['fields']['asset'],
                                             interval=interval,
                                             price=last_price)

            print('Updating', transactionId, 'to complete transaction')
            result = update_to_complete_transaction(_id=transactionId,
                                                    key=type_of_trade,
                                                    points=point)

            if result:
                del point['time']
                insert_trade_event([point])

            # Finally update to make sure the transaction is closed
            update_transaction_by_id(transactionId, key='forced_closed', value=True)
            update_transaction_by_id(transactionId, key='lastUpdate', value=datetime.now().strftime(DATE_STR))


if __name__ == '__main__':
    close_everything(nbr_hours_before_closing_transaction=2)
