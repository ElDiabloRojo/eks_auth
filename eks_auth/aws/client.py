import boto3

class AWSCLient:
    def __init__(self, service, access_key, secret_key, region, session_token=None):
        self.service = service
        self.access_key = access_key
        self.secret_access_key = secret_key
        self.session_token = session_token
        self.region = region

    def primary_client(self):
        client = boto3.client(
            self.service,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_access_key
        )

        return client

    def session_token_client(self, region):
        client = boto3.client(
            self.service,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_access_key,
            aws_session_token=self.session_token,
            region_name=region
        )

        return client

    def get_session_token(self, user_name, account_number):
        mfa_code = input('Enter the MFA code: ')
        client = boto3.client(
            self.service,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_access_key
        )
        response = client.get_session_token(
            DurationSeconds=3600,
            SerialNumber='arn:aws:iam::' + account_number + ':mfa/' + user_name,
            TokenCode=mfa_code
        )

        return response


    def show_object(self):
        print(self.__dict__)