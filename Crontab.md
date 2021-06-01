# Crontab

## crontab -l

    m h dom mon dow   command
    0 5 * * 1 sudo systemctl reboot
    0 4 * * * sudo journalctl --vacuum-time=1d -u tradingBot
    0 4 * * * sudo systemctl restart tradingBot
    0 16 * * * sudo systemctl restart tradingBot
    0 4 * * * sudo systemctl restart websocketKraken
    0 16 * * * sudo systemctl restart websocketKraken
    0 1 * * * /home/ubuntu/anaconda3/envs/trading-bot/bin/python /home/ubuntu/trading-bot-interval/transaction_closer_automate.py
    0 3 * * * /home/ubuntu/anaconda3/envs/trading-bot/bin/python /home/ubuntu/trading-bot-interval/transaction_closer_automate.py
    0 5 * * * /home/ubuntu/anaconda3/envs/trading-bot/bin/python /home/ubuntu/trading-bot-interval/transaction_closer_automate.py
    0 7 * * * /home/ubuntu/anaconda3/envs/trading-bot/bin/python /home/ubuntu/trading-bot-interval/transaction_closer_automate.py
    0 9 * * * /home/ubuntu/anaconda3/envs/trading-bot/bin/python /home/ubuntu/trading-bot-interval/transaction_closer_automate.py
    0 11 * * * /home/ubuntu/anaconda3/envs/trading-bot/bin/python /home/ubuntu/trading-bot-interval/transaction_closer_automate.py
    0 13 * * * /home/ubuntu/anaconda3/envs/trading-bot/bin/python /home/ubuntu/trading-bot-interval/transaction_closer_automate.py
    0 15 * * * /home/ubuntu/anaconda3/envs/trading-bot/bin/python /home/ubuntu/trading-bot-interval/transaction_closer_automate.py
    0 17 * * * /home/ubuntu/anaconda3/envs/trading-bot/bin/python /home/ubuntu/trading-bot-interval/transaction_closer_automate.py
    0 19 * * * /home/ubuntu/anaconda3/envs/trading-bot/bin/python /home/ubuntu/trading-bot-interval/transaction_closer_automate.py
    0 21 * * * /home/ubuntu/anaconda3/envs/trading-bot/bin/python /home/ubuntu/trading-bot-interval/transaction_closer_automate.py
    0 23 * * * /home/ubuntu/anaconda3/envs/trading-bot/bin/python /home/ubuntu/trading-bot-interval/transaction_closer_automate.py
    0 23 * * * /home/ubuntu/anaconda3/envs/trading-bot/bin/python3 /home/ubuntu/trading-bot-interval/walletEvolutionService.py
    0 23 * * * /home/ubuntu/anaconda3/envs/trading-bot/bin/python3 /home/ubuntu/trading-bot-interval/transaction_analysis_frontend.py
