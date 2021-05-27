from datetime import datetime
from enum import Enum

import requests

from src.helpers.dateHelper import SIMPLE_DATE_STR


class SlackChannelsEnum(Enum):
    Exception = "https://hooks.slack.com/services/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"
    TradeEvent = "https://hooks.slack.com/services/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"
    TransactionAnalysis = "https://hooks.slack.com/services/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"
    TransactionComplete = "https://hooks.slack.com/services/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"


def send_message_via_slack(url: str, message: str):
    data = {"text": message}
    return requests.post(url=url, json=data)


def send_exception_to_slack(err):
    channel = SlackChannelsEnum.Exception.value
    send_message_via_slack(channel, err)


def send_trade_event_to_slack(event):
    channel = SlackChannelsEnum.TradeEvent.value
    send_message_via_slack(channel, event)


def send_transaction_analysis_to_slack(event):
    channel = SlackChannelsEnum.TransactionAnalysis.value
    send_message_via_slack(channel, event)


def clean_transaction_event(event: dict) -> str:
    # TODO -> remove if there is no bug
    # {'_id': '60af5f61fc6f8ab3a49418ab', 'dateOfCreation': '2021-05-27T10:59:13Z', 'lastUpdate': '2021-05-27T11:00:55Z', 'version': 1.0,
    # 'buy': {'time': '2021-05-27 10:59:13.184528+00:00', 'measurement': 'tradeEvent', 'tags': {'typeOfTrade': 'buy', 'interval': 5}, 'fields': {'asset': 'LINK', 'quantity': 1.742664636405641, 'price': 27.09668}},
    # 'sell': {'time': '2021-05-27 11:00:55.907287+00:00', 'measurement': 'tradeEvent', 'tags': {'typeOfTrade': 'sell', 'interval': 5}, 'fields': {'asset': 'LINK', 'quantity': 1.742664636405641, 'price': 27.2441, 'transactionId': '60af5f61fc6f8ab3a49418ab'}},
    # 'forced_closed': False}
    dto = {
        'id': event['_id'],
        'dateOfCreation': event['dateOfCreation'],
        'lastUpdate': event['lastUpdate'],
        'asset': event['buy']['fields']['asset'],
        'foced_closed': [event]['forced_closed'],
        'buy': {
            'quantity': [event]['buy']['fields']['quantity'],
            'price': [event]['buy']['fields']['price']
        },
        'sell': {
            'quantity': [event]['sell']['fields']['quantity'],
            'price': [event]['sell']['fields']['price']
        }
    }
    return str(dto)


def send_transaction_complete_to_slack(event: dict):
    channel = SlackChannelsEnum.TransactionComplete.value
    str_dto: str = clean_transaction_event(event)
    send_message_via_slack(channel, str_dto)


def create_trade_event_message(title, input_params, results):
    return f"""
        {title} - {str(datetime.now().strftime(SIMPLE_DATE_STR))}
        Input params -> {input_params}
        API results -> {results}
    """


if __name__ == '__main__':
    send_exception_to_slack('Exception -> terrible exception')
    send_trade_event_to_slack('Trade event -> new event')
    send_transaction_analysis_to_slack('New trade analysis')
