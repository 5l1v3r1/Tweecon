#!/usr/bin/python3
#-*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import optparse, json, smtplib, sys, time, re, random, os, sys, requests
from elasticsearch import Elasticsearch
from datetime import datetime
from terminaltables import SingleTable

#COLORS
colors=['\033[0m',   # 0}  WHITE
		'\033[31m',  # 1}  RED
		'\033[32m',  # 2}  YELLOW
		'\033[33m',  # 3}  PURPLE
		'\033[34m',  # 4}  CYAN
		'\033[35m',  # 5}  MAGENT
		'\033[36m',  # 6}  CURL ____
		'\033[1m',   # 7}  WHITE LOW
		'\033[4m',   # 8}  WHITE HIGH
		'\033[0m',   # 9}  WHITE (FUCK)
		'\033[40m',  # 10} BACKGROUND GREY
		'\033[41m',  # 11} BACKGROUND RED
		'\033[42m',  # 12} BACKGROUND GREEN
		'\033[43m',  # 13} BACKGROUND YELLOW
		'\033[32m']   # 14}  GREEN

version='1.0'

#CONFIGURE YOUR API CREDENTIALS HERE
class APIKEYS:
        CONSUMER_KEY=''
        CONSUMER_SECRET=''
        ACCESS_TOKEN=''
        ACCESS_SECRET=''

class StdOutListener(StreamListener):
    def on_data(self, data):
        list_data=json.loads(data)
        tweet=(list_data['text'])
        username=list_data['user']['screen_name']
        print(colors[4]+username+colors[0]+": "+tweet)

        list_data['timestamp'] = datetime.now

    def on_error(self, status_code):
        if status_code == 420:
            return False

def confirmation():
    try:
        if APIKEYS.CONSUMER_KEY=='':
            print('[!] You Have Not Setup Your API Credentials In Tweecon.py! Please Add API Creds!')
            exit()
        else:
            table_data=[
            ['Identifier','Value'],
            ['Consumer Key',APIKEYS.CONSUMER_KEY],
            ['Consumer Secret',APIKEYS.CONSUMER_SECRET],
            ['Access Token',APIKEYS.ACCESS_TOKEN],
            ['Access Secret',APIKEYS.ACCESS_SECRET]
            ]
            table=SingleTable(table_data,title='Please Confirm API Credentials')
            #print(table.table)
            ans=input("[Y/n] ")
            if ans=='y':
                print('[?] Keyword For Search')
                keyword=input('keyword> ')
                print('=' * 50)
                print('Displaying Results Containing: '+keyword)
                print('=' * 50)
                search(keyword)
            else:
                print('Please Re-Enter API Keys in Tweecon.py')
                exit()
    except KeyboardInterrupt:
        print('Exiting Tweecon..')
        exit()
    except KeyError:
        pass

def search(xyz):
    l=StdOutListener()
    auth=OAuthHandler(APIKEYS.CONSUMER_KEY,APIKEYS.CONSUMER_SECRET)
    auth.set_access_token(APIKEYS.ACCESS_TOKEN,APIKEYS.ACCESS_SECRET)
    stream=Stream(auth,l)
    stream.filter(track=[xyz], async=True)

confirmation()
