import numpy as np
from sklearn.cross_validation import KFold
from sklearn.metrics import confusion_matrix, f1_score
from tools.pipelines import gen_pipeline, TYPES as pipeline_types
from tools.helpers import build_data_frame

def combine_full_data(rows):
    data_frame = build_data_frame(rows)
    data_frame.reindex(np.random.permutation(data_frame.index))
    return data_frame

def use_pipeline_prob(data, type, examples):
    pipeline = gen_pipeline(data, type)
    return pipeline.predict_proba(examples)

def use_pipeline(data, type, examples):
    pipeline = gen_pipeline(data, type)
    return pipeline.predict(examples)

def cross_validate(data, type):
    k_fold = KFold(n=len(data), n_folds=6)
    scores = []
    confusion = np.array([[0, 0], [0, 0]])

    for train_indices, test_indices in k_fold:
        train_text = data.iloc[train_indices]['text'].values
        train_y = data.iloc[train_indices]['class'].values

        test_text = data.iloc[test_indices]['text'].values
        test_y = data.iloc[test_indices]['class'].values

        pipeline = gen_pipeline(data, type)
        pipeline.fit(train_text, train_y)
        predictions = pipeline.predict(test_text)

        confusion += confusion_matrix(test_y, predictions)
        score = f1_score(test_y, predictions, pos_label=1)
        scores.append(score)

    return {"scores": scores, "confusion": confusion}

def print_metrics(data, pipelines=pipeline_types):
    frame = combine_full_data(data)

    for type in pipelines:
        print type

        testing = cross_validate(frame, type)

        print sum(testing['scores']) / len(testing['scores'])
        print testing['confusion']
        print "---------------------------"