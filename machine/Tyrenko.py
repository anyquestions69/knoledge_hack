def pymorphy2_311_hotfix():
    from inspect import getfullargspec
    from pymorphy2.units.base import BaseAnalyzerUnit

    def _get_param_names_311(klass):
        if klass.__init__ is object.__init__:
            return []
        args = getfullargspec(klass.__init__).args
        return sorted(args[1:])

    setattr(BaseAnalyzerUnit, '_get_param_names', _get_param_names_311)




import numpy as np
import tensorflow as tf
import pymorphy2
import re
import json


def formate_text(text, with_mophy = True):
    PATTERN = r'[^а-яА-Я \d\-]'
    pymorphy2_311_hotfix()
    morph = pymorphy2.MorphAnalyzer()
    
    text = text.replace(',', ' ').replace('_', ' ').replace('\n', ' ').lower()
    text = re.sub(PATTERN, "", text)
    if with_mophy:
        string = ''
        for item in text.split(' '):
            string += morph.parse(item)[0].normal_form + ' '
        return string.strip("\t\n ")
    return text.strip("\t\n ")

def get_links(text):
    REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    links = []
    find_links = re.findall(REGEX, text)
    for lk in find_links:
        if isinstance(lk, tuple):
            for item in lk:
                if len(item) > 0:
                    links.append(item)
        elif isinstance(lk, str) and len(lk) > 0:
            links.append(lk)
    return links

def get_ratio_links(links, text):
    try:
        count_links = len(links)
        count_words = len(text.split())
        return count_links / count_words
    
    except Exception as e:
        print(e)
        return 0.0

def determined_text_to_title(title, text):
    
    if title.strip("\t\n ") == '' or text.strip("\t\n ") == '':
        return 'Error: Оба поля должны быть заполненый!'

    model = tf.keras.models.load_model('best_hack_model.h5')

    with open('tokenizer_hack_dict.json', 'r') as f:
        word_index = json.load(f)
    tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=10000, oov_token="<OOV>")
    tokenizer.word_index = word_index

    title = formate_text(title)
    links = get_links(text)
    text = formate_text(text)
    ratio_links = get_ratio_links(links, text)

    title = tokenizer.texts_to_sequences([title])
    text = tokenizer.texts_to_sequences([text])

    titles_pad = tf.keras.preprocessing.sequence.pad_sequences(title, maxlen=20)
    articles_pad = tf.keras.preprocessing.sequence.pad_sequences(text, maxlen=1000)

    predition = model([titles_pad, articles_pad])
    pred_class= int(tf.round(predition)[0][0].numpy())


    label_dict = {
        0: 'Статья не полностью раскрывает суть темы или нет её определения!',
        1: 'Статья полностью раскрывает суть темы и присутствует её определение!'
    }

    if ratio_links > 0.05:
        result = "что превышает норму"
    else:
        result = " что яляется допустимым"
    
    return label_dict[pred_class] + f' уровень бесполезной информации: {ratio_links * 100}%, {result}!'