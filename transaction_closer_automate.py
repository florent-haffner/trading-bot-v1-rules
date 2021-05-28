from datetime import datetime, timedelta

from src.data.missionMongoUtils import get_all_missions
from src.data.tradeEventUtils import insert_trade_event
from src.data.transactionMongoUtils import update_transaction_by_id, get_all_transactions_since_midnight, \
    get_transaction_by_id
from src.helpers.dateHelper import DATE_STR, DATE_UTC_TZ_STR
from src.services.krakenPrivateTradeService import get_last_price, create_new_order
from src.services.slackEventService import send_transaction_complete_to_slack, send_exception_to_slack
from src.services.tradeEventService import generate_trade_event_dto
from src.services.transactionService import update_to_complete_transaction


def lambda_handler(event, context):
    nbr_hours_before_closing_transaction: int
    nbr_hours_before_closing_transaction = event['nbr_hour']
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

    nbr_hours_before_closing = datetime.now() - timedelta(hours=nbr_hours_before_closing_transaction)
    for transaction in transactions_to_closed:
        transactionId = transaction['_id']
        time = datetime.strptime(transaction['buy']['time'], DATE_UTC_TZ_STR)

        if time < nbr_hours_before_closing:
            print('Closing', transactionId)
            last_price = get_last_price(transaction['buy']['fields']['asset'], 'EUR')
            quantity = transaction['buy']['fields']['quantity']
            type_of_trade = 'sell'

            point = generate_trade_event_dto(type_of_trade=type_of_trade,
                                             quantity=quantity,
                                             asset=transaction['buy']['fields']['asset'],
                                             interval=interval,
                                             price=last_price)

            print('Updating', transactionId, 'to complete transaction')
            transaction = update_to_complete_transaction(_id=transactionId, key=type_of_trade, points=point)
            if transaction:
                del point['time']
                insert_trade_event([point])
                asset: str = transaction['buy']['fields']['asset']
                currency: str = 'EUR'
                order_params = asset + currency, type_of_trade, quantity
                order_response = create_new_order(pair=order_params[0], type=order_params[1], quantity=order_params[2])
                if order_response['error']:
                    formatted_error: str = str(order_response) + '->' + str(order_response)
                    send_exception_to_slack(formatted_error)

            # Finally update to make sure the transaction is closed
            update_transaction_by_id(transactionId, key='forced_closed', value=True)
            update_transaction_by_id(transactionId, key='lastUpdate', value=datetime.now().strftime(DATE_STR))
            transaction = get_transaction_by_id(transactionId)
            transaction['_id'] = str(transaction['_id'])
            print('Transaction closed', transaction)
            send_transaction_complete_to_slack(transaction)


if __name__ == '__main__':
    event = {"nbr_hour": 1}
    lambda_handler(event, {})
