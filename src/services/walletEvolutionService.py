from src.data.walletEvolutionMongoUtils import get_all_wallet_evolution, generate_wallet_evolution_dto, \
    create_wallet_evolution
from src.services.krakenPrivateTradeService import get_account_balance


def get_wallet_evolution():
    return get_all_wallet_evolution()


def insert_wallet_evolution(event: dict):
    account_balance: float = float(get_account_balance()['result']['ZEUR'])
    wallet_evolution = generate_wallet_evolution_dto(event, account_balance)
    return create_wallet_evolution(wallet_evolution)


if __name__ == '__main__':
    evolutions = list(get_all_wallet_evolution())
    print(evolutions)

    event = {}
    # event = {'type': 'withdrawals', 'value': 0}
    # event = {'type': 'funds', 'value': 0}
    insert_wallet_evolution(event)

    evolutions = list(get_all_wallet_evolution())
    print(evolutions)
