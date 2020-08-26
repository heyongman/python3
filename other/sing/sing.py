import pyttsx3
import time
from aip import AipSpeech
from playsound import playsound


def pyttsx():
    text = 'hello'
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    rate = engine.getProperty("rate")
    volume = engine.getProperty("volume")

    engine.say(text)
    engine.runAndWait()


def baidu():
    APP_ID = '18346646'
    API_KEY = 'zItMFTRvVouTEl3EO5NTdbLm'
    SECRET_KEY = 'Z4UgmREnIGDB91P9ifVaGg5WAz5E6MqL'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    result = client.synthesis('a', 'zh', 1, {
        'vol': 5,
    })

    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('auido.mp3', 'wb') as f:
            f.write(result)


def play():
    playsound("auido.mp3")


if __name__ == '__main__':
    pyttsx()
