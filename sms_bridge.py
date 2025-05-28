#!/usr/bin/python3
import requests
import logging
import json
import time
import binascii

# Setup logging
logging.basicConfig(filename='sms_bridge.log', level=logging.INFO)

# Constants
SMS_SERVER_URL = 'http://192.168.6.1'
TELEGRAM_BOT_TOKEN = 'TELEGRAM BOT_TOKEN Here'
TELEGRAM_CHAT_ID = 'TELEGRAM CHAT ID Here'
REFERER_HEADER = {'Referer': 'http://192.168.6.1/index.html'}
POLL_INTERVAL = 10  # Seconds between checks

def fetch_sms_messages():
    response = requests.get(
        f'{SMS_SERVER_URL}/goform/goform_get_cmd_process?isTest=false&cmd=sms_data_total&page=0&data_per_page=500&mem_store=1&tags=10&order_by=order+by+id+desc',
        headers=REFERER_HEADER
    )
    sms_data = json.loads(response.text)
    return sms_data.get('messages', [])

def decode_content(content):
    """Decode hex-encoded UTF-16BE content without subprocess"""
    try:
        byte_data = binascii.unhexlify(content)
        return byte_data.decode('utf-16-be').strip()
    except Exception as e:
        logging.error(f"Decoding failed: {str(e)}")
        return "[DECODING ERROR]"

def send_message_to_telegram(chat_id, text):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=payload)
    return response.ok

def delete_sms(sms_id):
    data = {'isTest': 'false', 'goformId': 'DELETE_SMS', 'msg_id': f'{sms_id};', 'notCallback': 'true'}
    response = requests.post(f'{SMS_SERVER_URL}/goform/goform_set_cmd_process', headers=REFERER_HEADER, data=data)
    return response.ok

def process_messages():
    try:
        messages = fetch_sms_messages()
        for message in messages:
            sms_id = message['id']
            phone_number = message['number']
            content = message['content']
            decoded_content = decode_content(content)

            logging.info(f'Received SMS from {phone_number}')
            telegram_msg = f'📩 New SMS from {phone_number}:\n{decoded_content}'

            if send_message_to_telegram(TELEGRAM_CHAT_ID, telegram_msg):
                logging.info(f'Forwarded message from {phone_number}')
                if delete_sms(sms_id):
                    logging.info(f'Deleted SMS ID {sms_id}')
                else:
                    logging.warning(f'Failed to delete SMS ID {sms_id}')
            else:
                logging.error(f'Telegram send failed for {phone_number}')
    except Exception as e:
        logging.error(f"Processing error: {str(e)}")

if __name__ == "__main__":
    logging.info("SMS Bridge Service Started")
    while True:
        process_messages()
        time.sleep(POLL_INTERVAL)
