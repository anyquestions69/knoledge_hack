import tensorflow as tf
import json
import pymorphy2
import re



from inspect import getfullargspec
from pymorphy2.units.base import BaseAnalyzerUnit

def _get_param_names_311(klass):
    if klass.__init__ is object.__init__:
        return []
    args = getfullargspec(klass.__init__).args
    return sorted(args[1:])
setattr(BaseAnalyzerUnit, '_get_param_names', _get_param_names_311)



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

def determined_text_to_title(title, text):

    model = tf.keras.models.load_model('best_hack_model.h5')

    with open('tokenizer_hack_dict.json', 'r') as f:
        word_index = json.load(f)
    tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=10000, oov_token="<OOV>")
    tokenizer.word_index = word_index

    # links = get_links(text) # НЕ УДАЛЯТЬ!

    title = tokenizer.texts_to_sequences(formate_text(title))
    text = tokenizer.texts_to_sequences(formate_text(text))

    titles_pad = tf.keras.preprocessing.sequence.pad_sequences(title, maxlen=20)
    articles_pad = tf.keras.preprocessing.sequence.pad_sequences(text, maxlen=1000)

    predition = model([titles_pad, articles_pad])
    pred_class= int(tf.round(predition)[0][0].numpy())

    label_dict = {
        0: 'Статья не полностью раскрывает суть темы!',
        1: 'Статья полностью раскрывает суть темы!'
    }
    
    return label_dict[pred_class]