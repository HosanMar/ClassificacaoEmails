import re
import string
from nltk.stem import RSLPStemmer
from nltk.corpus import stopwords

stemmer = RSLPStemmer()
stopwords_pt = set(stopwords.words("portuguese"))

def preprocess_text(text):
    text = text.lower()
    text = text.replace("\n", " ")

    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"\S+@\S+", "", text)
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))

    tokens = text.split()

    tokens = [t for t in tokens if t not in stopwords_pt]

    stems = [stemmer.stem(t) for t in tokens]

    return " ".join(stems)
