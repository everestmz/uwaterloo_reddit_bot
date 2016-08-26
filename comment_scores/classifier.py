from tools.classifier_helpers import combine_full_data, use_pipeline

def determine_comment_score(data, comment_text):
    frame = combine_full_data(data)
    prediction = use_pipeline(frame, 'bernoulli', [comment_text])[0]
    return prediction