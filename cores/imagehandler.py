import uuid

class ImageHandler:
    def __init__(self, client, bucket, region):
        self.client = client
        self.bucket = bucket
        self.region = region

    def upload_file(self, file):
        unique_key = str(uuid.uuid4())

        self.client.put_object(
            Bucket      = self.bucket,
            Key         = unique_key,
            Body        = file.file.read(),
            ContentType = file.content_type
        )

        return '%s.s3.%s.amazonaws.com/%s' % (self.bucket, self.region, unique_key)
