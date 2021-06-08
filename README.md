# Trading-bot

Version : 0.7

## Infrastructure

Use docker to launch MongoDB + InfluxDB instances.

Set user for Influx :

    influx CREATE USER admin WITH PASSWORD '<password>' WITH ALL PRIVILEGES

## Dependancy

Python management

     wget https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh

Bot dependencies :

    conda create -n trading-bot python=3.8

    conda activate trading-bot && pip3 install -r requirement.txt

## Launching services

    sudo cp *.service /lib/systemd/system/

    systemctl start tradingBot && systemctl enable tradingBot

Add automate closer to crontab.

To check the logs of the process : `journalctl _PID=1077`


## Env - OBSOLETE CURRENTLY

GPU acceleration /w CUDA and cuDNN, here version used on Arch linux.
```
cuda-11.0 11.0.3-3
cudnn8-cuda11.0 8.0.3.33-1
```
