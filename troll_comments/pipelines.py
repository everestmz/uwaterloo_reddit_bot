from sklearn.naive_bayes import BernoulliNB, GaussianNB, MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer, TfidfVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from dense_transformer import DenseTransformer
from sklearn.neighbors import KNeighborsClassifier

DEFAULT_BERNOULLI_BINARIZE = 0.1
TYPES = [ 'knn', 'multinomial', 'bernoulli', 'gaussian']

def gen_pipeline(data, type, count=DEFAULT_BERNOULLI_BINARIZE):
    if type == 'multinomial':
        return gen_multinomial(data)
    elif type == 'bernoulli':
        return gen_bernoulli(data, count)
    elif type == 'gaussian':
        return gen_gaussian(data)
    elif type == 'knn':
        return gen_knn(data)

def gen_multinomial(data):
    pipeline = Pipeline([
        ('vectorizer', CountVectorizer(ngram_range=(1, 2))),
        #('vectorizer', HashingVectorizer()),
        #('vectorizer', TfidfVectorizer()),
        #('tfidf_transformer', TfidfTransformer()),
        ('classifier', MultinomialNB())
    ])
    pipeline.fit(data['text'].values, data['class'].values)
    return pipeline

def gen_knn(data):
    pipeline = Pipeline([
        ('vectorizer', CountVectorizer(analyzer='char', ngram_range=(1, 7))),
        #('vectorizer', HashingVectorizer()),
        #('vectorizer', TfidfVectorizer()),
        ('tfidf_transformer', TfidfTransformer()),
        ('classifier', KNeighborsClassifier())
    ])
    pipeline.fit(data['text'].values, data['class'].values)
    return pipeline

def gen_bernoulli(data, binarize_num):
    pipeline = Pipeline([
        #('vectorizer', CountVectorizer()),
        #('vectorizer', HashingVectorizer()),
        ('vectorizer', TfidfVectorizer()),
        ('tfidf_transformer', TfidfTransformer()),
        ('classifier', BernoulliNB(binarize=binarize_num))
    ])
    pipeline.fit(data['text'].values, data['class'].values)
    return pipeline

def gen_gaussian(data):
    pipeline = Pipeline([
        ('vectorizer', CountVectorizer(ngram_range=(2, 4))),
        #('vectorizer', TfidfVectorizer()),
        ('tfidf_transformer', TfidfTransformer()),
        ('to_dense', DenseTransformer()),
        ('classifier', GaussianNB())
    ])
    pipeline.fit(data['text'].values, data['class'].values)
    return pipeline