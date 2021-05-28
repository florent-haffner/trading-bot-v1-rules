from tokenize import String
from datetime import datetime
from json import dumps

from src.helpers.dateHelper import SIMPLE_DATE_STR
from src.helpers.params import MAXIMUM_FEES
from src.data.transactionAnalysisMongoUtils import create_domain_object, insert_analysis
from src.data.missionMongoUtils import get_all_missions
from src.services.slackEventService import send_transaction_analysis_to_slack
from src.services.transactionService import get_complete_transaction_per_day_asset


def calculate_win_loss_per_transactions(transactions):
    total = []
    beginningAmount = 0
    nbr_positive_transactions = 0
    for transaction in transactions:
        type_of_trade = ['buy', 'sell']
        print(transaction['buy'], '->', transaction['sell'])
        transactionAmount = []
        for trade in type_of_trade:
            try:
                field = transaction[trade]['fields']
                amountPerTransaction = field['quantity'] * field['price']

                if not beginningAmount:
                    beginningAmount = amountPerTransaction

                # Fees are applies twice : while buying AND selling
                fees = amountPerTransaction * MAXIMUM_FEES
                net_amount = amountPerTransaction - fees

                transactionAmount.append(net_amount)
            except KeyError:
                pass

        if len(transactionAmount) == 1:
            current = -transactionAmount[0]
            total.append(current)
        else:
            totalPerTransaction = -transactionAmount[0] + transactionAmount[1]
            if totalPerTransaction > 0:
                nbr_positive_transactions = nbr_positive_transactions + 1
            total.append(totalPerTransaction)

    totalAmount = 0
    for amountPerTransaction in total:
        totalAmount = totalAmount + amountPerTransaction

    return len(transactions), totalAmount, beginningAmount, nbr_positive_transactions


# TODO -> not sure still useful
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
    results: list = []
    missions = list(get_all_missions())
    for mission in missions:
        for asset in mission['context']['assets']:

            print('\n[', asset, '] -> Calculating win/loss pet asset')
            transactionFromAsset = list(get_complete_transaction_per_day_asset(asset))
            nbrTransaction, amount, beginningAmount, nbrPositiveTransactions = \
                calculate_win_loss_per_transactions(transactionFromAsset)

            dto: dict = generate_dto(asset, round(beginningAmount, 2), nbrTransaction, nbrPositiveTransactions, round(amount, 3))
            print('Current analysis result', dto)
            results.append(dto)

    # Calculating the overall percentage
    asset: String = 'total'
    amountSum: int = 0
    nbrTransactionSum: int = 0
    nbrPositiveTransactionSum: int = 0
    resultsSum: int = 0
    for res in results:
        amountSum = amountSum + res['beginning_amount']
        nbrTransactionSum = nbrTransactionSum + res['nbr_transactions']
        nbrPositiveTransactionSum = nbrTransactionSum + res['nbr_positive_transactions']
        resultsSum = resultsSum + res['result']

    dto: dict = generate_dto(asset=asset,
                             beginning_amount=round(amountSum, 2),
                             nbr_transactions=nbrTransactionSum,
                             nbr_positive_transactions=nbrPositiveTransactionSum,
                             result=resultsSum)
    results.append(dto)

    # Store mock on MongoDB
    data = create_domain_object(results, 'daily')
    print('Analysis results')
    if store_results:
        insert_analysis(data)

        msg_to_send = f"""
        [BOT ANALYSIS OF THE DAY]
        {datetime.now().strftime(SIMPLE_DATE_STR)}
        {str(dumps(results, indent=2))}
        """
        send_transaction_analysis_to_slack(msg_to_send)


def generate_dto(asset, beginning_amount, nbr_transactions, nbr_positive_transactions, result):
    return {
        "asset": asset,
        "beginning_amount": beginning_amount,
        "nbr_transactions": nbr_transactions,
        "nbr_positive_transactions": nbr_positive_transactions,
        "result": result,
        "percent": round(result * 100 / beginning_amount, 2) if beginning_amount else 0
    }


if __name__ == '__main__':
    # store_results = False
    store_results = True
    calculate_win_and_loss_per_mission(store_results)
