import os
import base64
import requests
from pydub import AudioSegment
import sys
import io
import re
from PySide6.QtCore import QRunnable, Slot, Signal, QObject, QThread, QCoreApplication, QMetaObject, Qt, Q_ARG
import textwrap
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process, Event
import time
from global_config import *

base_logo = 'bạn đang nghe truyện audio trên kênh s truyện 2 4 7. nếu thấy hay đừng quên bấm like và sub cribe kênh nhé'

gcp_headers = {
            'authority': 'cxl-services.appspot.com',
            'accept': '*/*',
            'accept-language': 'vi-VN,vi;q=0.9',
            'content-type': 'text/plain;charset=UTF-8',
            'origin': 'https://www.gstatic.com',
            'referer': 'https://www.gstatic.com/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }

gcp_url = 'https://cxl-services.appspot.com/proxy?url=https://us-central1-texttospeech.googleapis.com/v1beta1/text:synthesize&token=0'

# format text
def formatText(text='', is_number = True):
        '''
        Format text 
        '''
        # remove any special character
        text = re.sub(r"[^\w~`!@$%^&*()?/\\:\s,.-;\'\"\[\{\}\]|+_\n]-"," ",text, flags=re.M)
        # remove number in [] like [1], [2],...
        text = re.sub(r"\[\d+\]", " ", text, flags=re.M)
        # replace chuong like chuong1: abc to chuong 1. abc
        result = re.search(r'^Chương\b.\d+:*', text,flags=re.I)
        if result:
            text = text.replace(result.group(0), result.group(0) + '. ')
        
        result1 = re.search(r'Trang\b.?\d+#.?\d', text,flags=re.I|re.M)
        if result1:
            text = text.replace(result1.group(0), '. ')

        # replace any break line to .
        text = re.sub(r'\n+', '. ', text, flags=re.M).strip()
        # remove duplicate special character
        text = re.sub('[^\w\s][^\w\s]+', '. ', text, flags=re.M)
        # repace !?:- to .
        
        for char in ['!', '?', ':', '-']:
            text = text.replace(char, '. ')
        
        # remove number
        if not is_number:
            text = re.sub(r'\d+', '. ', text, flags=re.M)
            
        # remove multilple . . . 
        text = re.sub(r'[\. ]{3,}', '. ', text, flags=re.M)
        
        return ' '.join(text.split())

# format payload
def format_payload(text='',pitch=-0.3,speakingRate=1.05, isFormat = True):
    '''
    Format and encode payload with args:
        + pitch: -0.3
        + speakingRate: 1.05
    Return payload data
    '''
    if isFormat:
        text = formatText(text)
    return str({"input": {"text": f"{text}"}, "voice": {"languageCode": "vi-VN", "name": "vi-VN-Neural2-A"},
                    "audioConfig": {"audioEncoding": "LINEAR16", "pitch": pitch, "speakingRate": speakingRate, "effectsProfileId": ["small-bluetooth-speaker-class-device"]}}).encode()
        
#request data to server
def handle_request( url='', headers = '', payload=''):
    try:
        response = requests.post(url=url, headers=headers, data=payload)
        if response.status_code == 200 or response.status_code == 201:
            return {'status': True, 'result': response.json()['audioContent']}
        else:
            return {'status': False, 'status_code': response.status_code, 'message': response.text}
    except Exception as message:
        print(message)
        return {'status': False,'status_code': 0, 'message': message}


# combine audio
def combine_audio(audio_path='', audio_name='', audio_data=[]):
    try:
        audio_content = b''
        for audio in audio_data:
            audio_content += base64.b64decode(audio)
        audio_segment = AudioSegment.from_file(io.BytesIO(
            audio_content), format='raw', frame_rate=24000, channels=1, sample_width=2)
        audio_segment.export(audio_path, format='wav')
        return {'status': True, 'result': True}
    except Exception as message: 
        return {'status': False, 'message': message}

def gcp_text_to_speech(url='', chapter_name='', chapter_data='', event=None):
    if event.is_set():
        print(f'Stopping, name={chapter_name}')
        return
    #  
    try:
        # 
        chapter_contents = chapter_data + base_logo
        audio_name = chapter_name.removesuffix('.txt') + '.wav'
        audio_path = os.path.join(outputAudio, audio_name)
        list_audio_data = []
        # 
        logging.info(f'Split data from {chapter_name} ')
        chapter_lists = textwrap.wrap(chapter_contents, width=3000)
        total_list = len(chapter_lists) - 1
        logging.info(f'Request data from {chapter_name} to server....')
        # split chapter contents to segments
        for current_count, current_content in enumerate(chapter_lists):
            gcp_payload = format_payload(current_content)
            gcp_request_data = handle_request(url=gcp_url, headers=gcp_headers, payload=gcp_payload)
            if gcp_request_data['status'] == True:
                list_audio_data.append(gcp_request_data['result'])
                sys.stdout.write(f"\r Downloading file: {round(current_count/total_list *100)}%")
                
                
            elif gcp_request_data['status'] == False and gcp_request_data['status_code'] !=400:
                logging.error(gcp_request_data['message'])
                event.set()
                return False
            
            else:
                logging.warning(f'First. false to request {chapter_name} text to server. Split payload and try again...')
                child_contents = textwrap.wrap(current_content, width=500)
                child_list = len(child_contents)
                for child_count, child_content in enumerate(child_contents):
                    child_gcp_payload = format_payload(child_content)
                    gcp_request_data = handle_request(url=gcp_url, headers=gcp_headers, payload=child_gcp_payload)
                    if gcp_request_data['status'] == True:
                        list_audio_data.append(gcp_request_data['result'])
                        time.sleep(1)
                        sys.stdout.write(f"\r Downloading child: {round((child_count/child_list)*100)}%")
                    else:
                        logging.error(gcp_request_data['message'])
                        event.set()
                        return False
        print('\n')        
        if not list_audio_data:
            logging.error('Audio list is emtry')
            return False
        else:
            combine_audio(audio_path=audio_path, audio_name=audio_name, audio_data=list_audio_data)
            logging.info(f"Success save audio {audio_name}")
    except Exception as message:
        logging.error(message)
        return False


# multiple
def multiple_speech_synthesis():
    list_process = []
    event = Event()
    with ThreadPoolExecutor(3) as executor:
        for chapter_name in sorted_alphanumeric(os.listdir(inputFolders)):
            chapter_path = os.path.join(inputFolders, chapter_name)
            with open(chapter_path, 'r', encoding='utf-8') as f:
                chapter_data = f.read()
            process = executor.submit(gcp_text_to_speech, *
                                        [gcp_url,chapter_name, chapter_data, event])
            list_process.append(process)
        return [process.result() for process in list_process]
def handle_process():
    process = Process(target=multiple_speech_synthesis)
    process.start()
    time.sleep(100)
    process.terminate()
if __name__ == '__main__':
    handle_process()