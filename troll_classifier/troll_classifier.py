import json
from helpers import load_json_into_array
from pandas import DataFrame
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import KFold
from sklearn.metrics import confusion_matrix, f1_score

def build_data_frame(rows):
    indexes = []
    for index, item in enumerate(rows):
        indexes.append(index)

    data_frame = DataFrame(rows, index=indexes)
    return data_frame

def combine_full_data():
    rows = load_json_into_array("troll_training_data.json")['comments']
    data_frame = build_data_frame(rows)
    return data_frame.reindex(np.random.permutation(data_frame.index))

def build_classifier(data_frame, counts):
    classifier = MultinomialNB()
    targets = data_frame['class'].values
    return classifier.fit(counts, targets)

def use_pipeline(data, examples):
    pipeline = Pipeline([
        ('vectorizer', CountVectorizer()),
        ('classifier', MultinomialNB())])
    pipeline.fit(data['text'].values, data['class'].values)
    return pipeline.predict(examples)

def custom_pipeline(data, examples):
    count_vectorizer = CountVectorizer()
    vectorized_counts = count_vectorizer.fit_transform(data['text'].values)

    classifier = build_classifier(data, vectorized_counts)

    example_counts = count_vectorizer.transform(examples)
    return classifier.predict(example_counts)

def cross_validate(data):
    k_fold = KFold(n=len(data), n_folds=12)
    scores = []
    confusion = np.array([[0, 0], [0, 0]])

    for train_indices, test_indices in k_fold:
        train_text = data.iloc[train_indices]['text'].values
        train_y = data.iloc[train_indices]['class'].values

        test_text = data.iloc[test_indices]['text'].values
        test_y = data.iloc[test_indices]['class'].values

        pipeline = Pipeline([
            ('vectorizer', CountVectorizer()),
            ('classifier', MultinomialNB())])
        pipeline.fit(train_text, train_y)
        predictions = pipeline.predict(test_text)

        confusion += confusion_matrix(test_y, predictions)
        score = f1_score(test_y, predictions, pos_label=1)
        scores.append(score)

    return {"scores": scores, "confusion": confusion}

def main():
    examples = ['DISRUPTIVE', "You're a fgt", "I'm gay", "It's all fun and games until someone is"]
    randomly_permuted_frame = combine_full_data()

    print use_pipeline(randomly_permuted_frame, examples)
    testing = cross_validate(randomly_permuted_frame)

    print testing['scores']
    print sum(testing['scores'])/len(testing['scores'])
    print testing['confusion']

if __name__ == "__main__":
    main()