import json
import requests
from bs4 import BeautifulSoup
import datetime
from time import sleep

class Bot:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
 
    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        return resp.json()['result']
 
    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp
 
    def get_last_update(self):
        get_result = self.get_updates()
        if len(get_result) > 0:
            return get_result[-1]
        return []

    def get_quote(self):
        r = requests.get(f'http://bash.im/random')
        soup = BeautifulSoup(r.text)
        quote = soup.find('div', {"class" : "quote"})
        result = []
        for line in quote.strings:
            print(line)
            line = line.strip()
            if len(line) > 0:
                result.append(line)
        print(result)
        return ' '.join(result[:2]) + '\n'.join(result[2:])

    def run(self):
        while True:
            for chat_id in self.get_chat_ids():
                message = self.get_quote()
                self.send_message(chat_id, message)

def main():
    new_offset = None
    bot = Bot('589200803:AAHT-dOuHnMxDAJ4XyHBJeMvAtiBI0ZCeoI')
    while True:
        bot.get_updates(new_offset)
        last_update = bot.get_last_update()
        if not last_update:
            sleep(1)
            continue
        # for future
        print(last_update)
        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        quote = bot.get_quote()
        print(quote)
        bot.send_message(last_chat_id, quote)
 
        new_offset = last_update_id + 1
    
 

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()
