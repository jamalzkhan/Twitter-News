#!/bin/bash

if [ "$1" = "drop" ];
then
  if [ "$2" = "local" ];
  then
    mongo twitter_news --eval "db.dropDatabase()"
  fi
  if [ "$2" = "remote" ];
  then
    ssh autotut@rafal.io 'twitter_news/control.sh drop local'
  fi
fi

if [ "$1" = "restart" ];
then
  if [ "$2" = "local" ];
  then
    killall -9 python
    python main_process.py
  fi
  if [ "$2" = "remote" ];
  then
    ssh autotut@rafal.io 'cd twitter_news && ./restart.sh'
  fi
fi

