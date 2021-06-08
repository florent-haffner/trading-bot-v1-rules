# Trading-bot

Version : 0.7

## Dependency

Python management

     wget https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh

Bot dependencies :

    conda create -n trading-bot python=3.8

    conda activate trading-bot && pip3 install -r requirement.txt

## Launching services

    sudo cp *.service /lib/systemd/system/

    systemctl start tradingBot && systemctl enable tradingBot

To check the logs of the process : `journalctl -u {serviceName}`


## OLD - Infrastructure

Use docker to launch MongoDB + InfluxDB instances.

Set user for Influx :

    influx CREATE USER admin WITH PASSWORD '<password>' WITH ALL PRIVILEGES
