# MoneyMakr-bot

# Infrastructure

Use docker to launch MongoDB + InfluxDB instances.

Config influxDB `influx CREATE USER admin WITH PASSWORD '<password>' WITH ALL PRIVILEGES`

## How to use

Check this out later, boy.

`$HOME/anaconda3/envs/trading-bot/bin/python -m src.main`

`cp tradingBot.service /lib/systemd/system/tradingBot.service`


## Env - OBSOLETE CURRENTLY

Python and general dependancies

    conda create -n trading-bot python=3.8 && conda activate trading-bot
    pip3 install -r requirements.txt

GPU acceleration /w CUDA and cuDNN, here version used on Arch linux.
```
cuda-11.0 11.0.3-3
cudnn8-cuda11.0 8.0.3.33-1
```
