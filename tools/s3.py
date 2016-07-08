import boto3, os, json, helpers

DEFAULT_TEMP_FILENAME = "temp.json"
S3_BUCKETS = {'troll': 'uw-bot-troll-classification', 'score': 'uw-bot-score-prediction'}
S3_FILENAMES = {'comments': 'comments/data.json', 'threads': 'threads/data.json'}

def login():
    return boto3.resource('s3')

def file_trans(key):
    return S3_FILENAMES[key]

def bucket_trans(key):
    return S3_BUCKETS[key]

def fetch_file_from_bucket(bucket, remote_name, local_name):
    s3 = login()
    s3_bucket = s3.Bucket(bucket)
    s3_bucket.download_file(remote_name, local_name)

def upload_file_to_bucket(bucket, local_name, remote_name):
    s3 = login()
    s3_bucket = s3.Bucket(bucket)
    s3_bucket.upload_file(local_name, remote_name)
    os.remove(local_name)

def overwrite_file(bucket, key, raw_data):
    fetch_file_from_bucket(bucket, key, DEFAULT_TEMP_FILENAME)
    helpers.write_to_data_file(DEFAULT_TEMP_FILENAME, raw_data)
    upload_file_to_bucket(bucket, DEFAULT_TEMP_FILENAME, key)

def update_json(bucket, key, new_data):
    remote_filename = file_trans(key)
    remote_bucket = bucket_trans(bucket)
    fetch_file_from_bucket(remote_bucket, remote_filename, DEFAULT_TEMP_FILENAME)
    old_data = helpers.load_json_into_array(DEFAULT_TEMP_FILENAME)[key]
    old_data += new_data
    helpers.write_to_data_file(DEFAULT_TEMP_FILENAME, json.dumps({key: old_data}))
    upload_file_to_bucket(remote_bucket, DEFAULT_TEMP_FILENAME, remote_filename)

def get_data(bucket, key):
    remote_bucket = bucket_trans(bucket)
    remote_filename = file_trans(key)
    fetch_file_from_bucket(remote_bucket, remote_filename, DEFAULT_TEMP_FILENAME)
    data = helpers.load_json_into_array(DEFAULT_TEMP_FILENAME)[key]
    upload_file_to_bucket(remote_bucket, DEFAULT_TEMP_FILENAME, remote_filename)
    return data

