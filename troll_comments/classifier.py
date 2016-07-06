from pandas import DataFrame
from helpers import flip
import numpy as np
from sklearn.cross_validation import KFold
from sklearn.metrics import confusion_matrix, f1_score
from pipelines import gen_pipeline, TYPES as pipeline_types
import pipelines

def build_data_frame(rows):
    indexes = []
    for index, item in enumerate(rows):
        indexes.append(index)

    data_frame = DataFrame(rows, index=indexes)
    return data_frame

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
    k_fold = KFold(n=len(data), n_folds=3)
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

def classify_cmdline(data):
    comment_classifications = []

    while True:
        randomly_permuted_frame = combine_full_data(data)

        print "Type your phrase"
        phrase = raw_input("> ")

        result = use_pipeline(randomly_permuted_frame, 'bernoulli', [phrase])

        if result[0] == 1:
            print "Troll"
        else:
            print "Not Troll"

        print "Correct?"
        add = raw_input("[y/n/exit] > ")

        if add == "y":
            comment_classifications.append({"text": phrase, "class": int(result[0])})
        elif add == "exit":
            break
        else:
            comment_classifications.append({"text": phrase, "class": flip(int(result[0]))})

    return {"threads": [], "data": comment_classifications}

def print_metrics(data):
    frame = combine_full_data(data)

    for type in pipeline_types:
        print type

        testing = cross_validate(frame, type)

        print sum(testing['scores']) / len(testing['scores'])
        print testing['confusion']
        print "---------------------------"

def main():
    examples = [
        'DISRUPTIVE', 
        "You're a fgt", 
        "I'm gay", 
        "It's all fun and games until someone is", 
        "dank memes br0", 
        "It's just a frantic karma grab after the first panino variation was posted.",
        "HERE COME DAT BOI O SHIT WADDUP",
        "im sorry",
        "Hey I'm gonna go do some homework"
    ]
    randomly_permuted_frame = combine_full_data()

    print use_pipeline(randomly_permuted_frame, 'multinomial', examples)

if __name__ == "__main__":
    main()