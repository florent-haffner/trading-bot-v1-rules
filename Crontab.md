# Crontab

## crontab -l

    # m h  dom mon dow   command
    0 5 * * 1 sudo systemctl reboot
    0 4 * * * sudo journalctl --vacuum-time=1d -u tradingBot 
    0 * * * * sudo systemctl daemon-reload && sudo systemctl restart tradingBot
    0 23 * * * /home/ubuntu/anaconda3/envs/trading-bot/bin/python3 /home/ubuntu/trading-bot-interval/analysis_frontend.py
