# Crontab

## crontab -l

    m h dom mon dow   command
    0 5 * * 1 sudo systemctl reboot
    0 4 * * * sudo journalctl --vacuum-time=1d -u tradingBot
    0 4 * * * sudo systemctl restart tradingBot
    0 16 * * * sudo systemctl restart tradingBot
    0 1 * * * sudo journalctl --vacuum-time=1d -u transactionCloserAutomate
    0 3 * * * sudo systemctl start transactionCloserAutomate
    0 5 * * * sudo systemctl start transactionCloserAutomate
    0 7 * * * sudo systemctl start transactionCloserAutomate
    0 9 * * * sudo systemctl start transactionCloserAutomate
    0 11 * * * sudo systemctl start transactionCloserAutomate
    0 13 * * * sudo systemctl start transactionCloserAutomate
    0 15 * * * sudo systemctl start transactionCloserAutomate
    0 17 * * * sudo systemctl start transactionCloserAutomate
    0 19 * * * sudo systemctl start transactionCloserAutomate
    0 21 * * * sudo systemctl start transactionCloserAutomate
    0 23 * * * sudo systemctl start transactionCloserAutomate
    0 23 * * * /home/ubuntu/anaconda3/envs/trading-bot/bin/python3 /home/ubuntu/trading-bot-interval/transaction_analysis_frontend.py
