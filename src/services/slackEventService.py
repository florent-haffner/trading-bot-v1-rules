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


def send_transaction_complete_to_slack(event):
    channel = SlackChannelsEnum.TransactionComplete.value
    send_message_via_slack(channel, event)


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
