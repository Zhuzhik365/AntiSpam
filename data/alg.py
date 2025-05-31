import pandas as pd
import numpy as np
import re

# Загрузка датасета
data_path = 'data/SMSSpamCollection'
df = pd.read_csv(data_path, sep='\t', header=None, names=['label', 'message'])

# Функция предобработки текста
def preprocess_text(text):
    text = text.lower()  # Приводим к нижнему регистру
    text = re.sub(r'[^a-z\s]', '', text)  # Удаляем все кроме букв и пробелов
    text = re.sub(r'\s+', ' ', text).strip()  # Удаляем лишние пробелы
    return text


# Применяем предобработку к сообщениям
df['clean_message'] = df['message'].apply(preprocess_text)

# Разделение на спам и не-спам
spam_df = df[df['label'] == 'spam']
ham_df = df[df['label'] == 'ham']


# Создание словарей частот слов
def create_freq_dict(messages):
    freq_dict = {}
    for message in messages:
        for word in message.split():
            freq_dict[word] = freq_dict.get(word, 0) + 1
    return freq_dict


# Создаем частотные словари
spam_freq = create_freq_dict(spam_df['clean_message'])
ham_freq = create_freq_dict(ham_df['clean_message'])

# Расчет спам-индикаторов для слов
word_spam_scores = {}
total_spam = len(spam_df)
total_ham = len(ham_df)

for word in set(spam_freq.keys()).union(ham_freq.keys()):
    spam_count = spam_freq.get(word, 0) + 1  # Добавляем 1 для сглаживания
    ham_count = ham_freq.get(word, 0) + 1

    # Рассчитываем вероятность слова в спаме
    spam_prob = spam_count / total_spam
    ham_prob = ham_count / total_ham

    # Вычисляем спам-индикатор
    word_spam_scores[word] = spam_prob / (spam_prob + ham_prob)

def spam_words(text):
    # Очищаем и разбиваем текст на слова
    clean_text = preprocess_text(text)
    words = clean_text.split()

    if not words:
        return False, 0.0  # Пустые сообщения не спам

    # Собираем индикаторы для слов из сообщения
    scores = []
    triger_wrods = []
    for word in words:
        if word in word_spam_scores:
            scores.append(word_spam_scores[word])
            triger_wrods.append([word,word_spam_scores[word]])

    return triger_wrods


# Функция проверки сообщения на спам
def check_spam(text, threshold=0.6):
    # Очищаем и разбиваем текст на слова
    clean_text = preprocess_text(text)
    words = clean_text.split()

    if not words:
        return False, 0.0  # Пустые сообщения не спам

    # Собираем индикаторы для слов из сообщения
    scores = []
    for word in words:
        if word in word_spam_scores:
            scores.append(word_spam_scores[word])

    # Если нет известных слов, считаем не спамом
    if not scores:
        return False, 0.0

    # Усредняем индикаторы
    spam_score = np.mean(scores)

    return spam_score > threshold, spam_score

spam_words(" spam")