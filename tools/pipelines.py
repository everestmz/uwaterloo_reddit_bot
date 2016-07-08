from sklearn.naive_bayes import BernoulliNB, GaussianNB, MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from dense_transformer import DenseTransformer
from helpers import load_json_into_array

DEFAULT_BERNOULLI_BINARIZE = 0.1
TYPES = [
    'multinomial',
    'bernoulli',
    'gaussian'
]

def gen_pipeline(data, type, count=DEFAULT_BERNOULLI_BINARIZE):
    if type == 'multinomial':
        return gen_multinomial(data)
    elif type == 'bernoulli':
        return gen_bernoulli(data, count)
    elif type == 'gaussian':
        return gen_gaussian(data)

def gen_multinomial(data):
    pipeline = Pipeline([
        ('vectorizer', CountVectorizer(analyzer='char_wb', ngram_range=(2, 4))),
        ('classifier', MultinomialNB())
    ])
    pipeline.fit(data['text'].values, data['class'].values)
    return pipeline

def gen_bernoulli(data, binarize_num):
    pipeline = Pipeline([
        ('vectorizer', TfidfVectorizer(lowercase=False)),
        ('classifier', BernoulliNB(binarize=binarize_num))
    ])
    pipeline.fit(data['text'].values, data['class'].values)
    return pipeline

def gen_gaussian(data):
    stopwords = load_json_into_array("troll_comments/stopwords.json")['stopwords']

    pipeline = Pipeline([
        ('vectorizer', CountVectorizer(stop_words=stopwords, lowercase=False)),
        ('tfidf_transformer', TfidfTransformer()),
        ('to_dense', DenseTransformer()),
        ('classifier', GaussianNB())
    ])
    pipeline.fit(data['text'].values, data['class'].values)
    return pipeline