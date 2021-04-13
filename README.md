# MoneyMakr-bot

# Infrastructure

Use docker to launch MongoDB + InfluxDB instances.

Set user for Influx :

    influx CREATE USER admin WITH PASSWORD '<password>' WITH ALL PRIVILEGES

Python's bot dependencies :

    conda create -n trading-bot python=3.8 && conda activate trading-bot
    pip3 install -r requirements.txt

## How to use

`$HOME/anaconda3/envs/trading-bot/bin/python -m src.main`

`cp tradingBot.service /lib/systemd/system/tradingBot.service`


## Env - OBSOLETE CURRENTLY

GPU acceleration /w CUDA and cuDNN, here version used on Arch linux.
```
cuda-11.0 11.0.3-3
cudnn8-cuda11.0 8.0.3.33-1
```
