from src.helpers.params import MAXIMUM_FEES
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
    missions = list(getAllMissions())
    for mission in missions:
        for asset in mission['context']['assets']:
            print('\n[', asset, '] -> Calculating win/loss pet asset')
            # transactionFromAsset = list(getTransactionsByAsset(asset))
            transactionFromAsset = list(getTransactionPerDayAsset(asset))
            nbrTransaction, amount = calculateWinLossPerTransactions(transactionFromAsset)
            print('Nbr transactions', nbrTransaction, 'amount in Euro', round(amount, 3))


if __name__ == '__main__':
    # getLastEventByTypeAndAsset('GRT', 'buy')

    calculateWInLossPerMission()

    # getAllTransactionPerDay()
