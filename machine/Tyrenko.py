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
    morph = pymorphy2.MorphAnalyzer()
    
    text = text.replace(',', ' ').replace('_', ' ').replace('\n', ' ').lower()
    text = re.sub(PATTERN, "", text)
    if with_mophy:
        string = ''
        for item in text.split(' '):
            string += morph.parse(item)[0].normal_form + ' '
        return string.strip("\t\n ")
    return text.strip("\t\n ")

def get_links_and_lenEmptyChars(text):
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
    
    cleaned_text = re.sub(REGEX, '', text)
    regex = r"[^a-zA-Zа-яА-Я\s\w\.:\!\?\s]"
    ratio_empty_chars = len(re.sub(regex, "", cleaned_text))


    return (links, ratio_empty_chars)

def get_ratio(links, text, len_empty = 0):
    try:
        count_links = len(links)
        count_words = len(text.split())
        return count_links + ( len_empty // 100 ) / count_words
    
    except Exception as e:
        print(e)
        return 0.0

def determined_text_to_title(title, text):
    
    if title.strip("\t\n ") == '' or text.strip("\t\n ") == '':
        return 'Error: Оба поля должны быть заполненый!'

    model = tf.keras.models.load_model('model.h5')

    with open('tokenizer_hack_dict.json', 'r') as f:
        word_index = json.load(f)
    tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=10000, oov_token="<OOV>")
    tokenizer.word_index = word_index

    title = formate_text(title)
    links, part_empty_chars = get_links_and_lenEmptyChars(text)
    text = formate_text(text)
    ratio_links = get_ratio(links, text, part_empty_chars)

    title = tokenizer.texts_to_sequences([title])
    text = tokenizer.texts_to_sequences([text])

    titles_pad = tf.keras.preprocessing.sequence.pad_sequences(title, maxlen=15)
    articles_pad = tf.keras.preprocessing.sequence.pad_sequences(text, maxlen=1500)

    predition = model([titles_pad, articles_pad])
    pred_class= int(tf.round(predition)[0][0].numpy())

    label_dict = {
        0: 'Статья не полностью раскрывает суть темы или нет её определения!',
        1: 'Статья полностью раскрывает суть темы и присутствует её определение!'
    }

    if ratio_links > 0.2:
        result = "что превышает норму"
    else:
        result = "что яляется допустимым"

    res_ratio_links = ratio_links * 100 if ratio_links * 100 < 100 else ratio_links * 10
    
    return label_dict[pred_class] + f' Уровень бесполезной информации: {res_ratio_links:.3f}%, {result}!'