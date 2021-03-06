import speech_recognition as sr
from requests import get
from bs4 import BeautifulSoup
from gtts import gTTS
import os

##### FLAG PARA CONTROLE #####
executar_acao = False

hotword = ''

##### CONFIGURAÇÕES DA CHAVE DO GOOGLE #####
with open('veronicaassistente-863fe9e3268f.json', 'r') as credenciais_google:
    credenciais_google = credenciais_google.read()
    
def monitorar_audio():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        print("Aguardando o Comando: ")
        microfone.adjust_for_ambient_noise(source)
        audio = microfone.listen(source)
    try:
        trigger = microfone.recognize_google_cloud(
            audio, credentials_json=credenciais_google, language='pt-BR')
        trigger = trigger.lower()
        if hotword in trigger and not get_status_trigger():
            print('Comando reconhecido!')
            respoder('feedback')
            set_status_trigger(True)
        elif get_status_trigger():
            set_status_trigger(False)
            return trigger
    except sr.UnknownValueError:
        print("Google not understand audio")
    except sr.RequestError as e:
        print(
            "Could not request results from Google Cloud Speech service; {0}".format(e))

    return None
    
def analisar_acao(comando):
    if comando == hotNoticias:
        sit = get('https://news.google.com/new/rss?')
        noticias = BeautifulSoup(site.text, 'parser.html')

        for item in noticias.findAll('item')[:5]:
            noticia = item.title.text
            criar_audio(noticia, 'noticia')
            responder('noticia')
        
        responder('tchau')
  
def criar_audio(texto, nome_arquivo):
    tts = gTTS(texto, lang='pt-br')
    path = 'audios/' + nome_arquivo + '.mp3'
    with open(path, 'wb') as file:
        tts.write_to_fp(file)


def respoder(nome_arquivo):
    path = 'audios/' + nome_arquivo + '.mp3'
    os.system('mpg321 ' + path)


def set_status_trigger(status):
    global executar_acao
    executar_acao = status


def get_status_trigger():
    return executar_acao


def __main__():
    while True:
        comando = monitorar_audio()
        if comando is not None:
            analisar_acao(comando)


__main__()