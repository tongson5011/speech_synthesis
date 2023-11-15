import logging
import os
import base64
import textwrap
import requests
from pydub import AudioSegment
import sys
import io
import re
from concurrent.futures import ThreadPoolExecutor

#config loggin 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s : %(message)s')

# config path
PATH = os.path.dirname(os.path.abspath(__file__))
inputFolders = os.path.join(PATH, 'inputFolders')
outputAudio = os.path.join(PATH, 'outputAudio')
os.makedirs(inputFolders, exist_ok=True)
os.makedirs(outputAudio, exist_ok=True)

# format input msg
class PayloadData():
    # init value
    def __init__(self, text='', pitch=-0.3, speakingRate=1.05):
        self.text = text
        self.pitch = pitch
        self.speakingRate = speakingRate
    # format msg
    def format(self):
        return str({"input": {"text": f"{self.text}"}, "voice": {"languageCode": "vi-VN", "name": "vi-VN-Neural2-A"},
                    "audioConfig": {"audioEncoding": "LINEAR16", "pitch": self.pitch, "speakingRate": self.speakingRate, "effectsProfileId": ["small-bluetooth-speaker-class-device"]}}).encode()


# short files in folder
def sorted_alphanumeric(data):
    def convert(text): return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key): return [convert(c)
                                   for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


# format text input
def formatText(text=''):
    # remove number in text. example name[1] age[2]
    text = re.sub(r"\[\d+\]", " ", text)
    # replce 
    for char in ["'",']','[', '"', '<', '>', '·', '(sửa)']:
        text = text.replace(char, ' ')
    # 
    for char1 in ['?','!',':', '–']:
        text = text.replace(char1, '. ')
    # 
    for char2 in ['. . .', '. .', '————','———','——', '-']:
        text = text.replace(char2, '. ')
    
    text = re.sub(r'\.+', ".", text)
    
    # add dot after chuong 
    result = re.search(r'^Chương\b.\d+:*', text)
    if result:
        text = text.replace(result.group(0), result.group(0) + '. ')
    document = []
    for line in text.split('\n'):
        if line:
            line = ' '.join(line.split())
            line = line.rstrip()
            if not line.endswith('.'):
                line = line + '.'
            document.append(line)
    temp_result = ' '.join(document)
    return ' '.join(temp_result.split())

#handle request data to server 
def gcp_request(url='', payload='', cus_name=''):
    headers = {
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
    response = requests.post(url=url, headers=headers, data=payload)
    if response.status_code == 200 or response.status_code == 201:
        return response.json()['audioContent']
    logging.error(f'{response.text}')
    return False

#request text to speech
def gcp_text_to_speech(url='', chapter_name='', chapter_data=''):
    if len(os.listdir(inputFolders)) == 0:
        logging.error('Input Folder is emtry')
        return False
    base_logo = 'bạn đang nghe truyện audio trên kênh s truyện 2 4 7. nếu thấy hay đừng quên bấm like và sub cribe kênh nhé'
    chapter_contents = formatText(f'''{chapter_data}. {base_logo}''')
    audio_name = chapter_name.removesuffix('.txt') + '.wav'
    audio_path = os.path.join(outputAudio, audio_name)
    audio_data = []
    audio_content = b''
    base_url = f'https://cxl-services.appspot.com/proxy?{url}' if not url.startswith(
        'https://cxl-services.appspot.com/proxy?') else url
    logging.info(f'Split {chapter_name} data')
    chapter_lists = textwrap.wrap(chapter_contents, width=3000)
    total_list = len(chapter_lists)
    # chapter_lists.insert(int(total_list/2),base_logo)
    logging.info(f'Request data from {chapter_name} to server....')
    #split and request text to server
    for current_count, current_chapter_content in enumerate(chapter_lists):
        current_count +=1
        payload_data = PayloadData(text=current_chapter_content).format()
        request_data = gcp_request(base_url, payload_data)
        if not request_data:
            logging.warning(f'First. false to request {chapter_name} text to server. Split payload and try again...')
            new_data_list = textwrap.wrap(current_chapter_content, width=500)
            for new_count, new_chapter_data in enumerate(new_data_list):
                new_payload_data = PayloadData(text=new_chapter_data).format()
                request_data = gcp_request(base_url, new_payload_data)
                if not request_data:
                    logging.error(f'Second. false to request {chapter_name} text to server. Please check error code')
                    return False
                else:
                    sys.stdout.write(f"\r Downloading new file: {new_count}%")
                    audio_data.append(request_data)
        else:
            sys.stdout.write(f"\r Downloading file: {round(current_count/total_list *100)}%")
            audio_data.append(request_data)
    print('\n')
    
    # combine audio
    logging.info(f'Combine audio {audio_name}')
    for audio in audio_data:
        audio_content += base64.b64decode(audio)
    audio_segment = AudioSegment.from_file(io.BytesIO(
        audio_content), format='raw', frame_rate=24000, channels=1, sample_width=2)
    audio_segment.export(audio_path, format='wav')
    logging.info(f"Success save audio {audio_name}")        
            

# multiple
def multiple_speech_synthesis(url):
    if len(os.listdir(inputFolders)) == 0:
        logging.error('Input folder is emtry')
        return False
    list_process = []
    with ThreadPoolExecutor(3) as executor:
        for chapter_name in sorted_alphanumeric(os.listdir(inputFolders)):
            chapter_path = os.path.join(inputFolders, chapter_name)
            with open(chapter_path, 'r', encoding='utf-8') as f:
                chapter_data = f.read()
                process = executor.submit(gcp_text_to_speech, *
                                          [url,chapter_name, chapter_data])
                list_process.append(process)
       
if __name__ == '__main__':
    url = 'url=https://us-central1-texttospeech.googleapis.com/v1beta1/text:synthesize&token=03AFcWeA57g3yuBEG92MY3ypitpfPxfw6Y_u6QTwPP8hn4zJ4DRcSFpb5pMPjahV-dJMVjOx0ESm9usQnF9Y0DuPtEEhjwnr1oiu37QiZttr0o8tZ9GrT6B-wPO33ChWnmY4em7-lUg4kLZB_xfeOgou_XG90TTKjsS2FGAQOYpByh0sayBJN9MkGI7YIval2TlHHQ9XiWwXEvz71mgI3H_EuRaDktSZQ8nFhJa8hSkei7AAAmYCtNOCgfmRli37oXsZdpZqOZeCSVnT73v-w6Y53uk0RkEVzZPq0cf6WrsBgNM-IoOJNcjX6o0CbTCDDig0tai5EKiMuiyUwkB9SkJXlnOPi9J59tnb3qkFpVZFQSwjGQ9wKHCbb4QRJayBQAJYyL3sv9dyR4CE8nTOcrAR4AjYto7OkzdQUHRV7OJtjLMS1FlKp64gxJufKeDjS81qNJVzSGm5A9294OYYc_5KCfCLqtSg_cLx2SZSNxQhSa_x4vvhcF5-QhGgNtxhfrVbE4VYX8SlIZFuuqVVYlik8lfOW99kbsoK084zrtNze7kHaQzZOU1ZPXTboiHWapMePKjbUeeeb7MGbfNzDkdvliOl4rgupCOAQnQM-MrBt3-wnG5EfQEjBwNE4sm-fHPdydm5ENI7OC'
    multiple_speech_synthesis(url)