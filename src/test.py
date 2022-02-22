from google.cloud import storage

# Instantiates a client
client = storage.Client()

# Creates a new bucket and uploads an object
# new_bucket = client.create_bucket('gcp-exploration-test-bucket')
# new_blob = new_bucket.blob('textfiles/storage.txt')
# new_blob.upload_from_filename(filename='test.txt')

# Retrieve an existing bucket
# https://console.cloud.google.com/storage/browser/[bucket-id]/
bucket = client.get_bucket('gcp-exploration-test-bucket')
# Then do other things...
blob = bucket.get_blob('textfiles/storage.txt')
print(blob.download_as_text())
blob.upload_from_string('New contents!')