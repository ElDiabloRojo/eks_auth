"""Main module."""
from profile import selector, profile, creator
from aws import client, eks
import configparser


def config():
    config = configparser.ConfigParser()
    config.read('./config.ini')

    return config


def main():
    project_config = config()
    region = project_config.get('general', 'REGION')
    role = project_config.get('cluster', 'ROLE')
    cluster_name = project_config.get('cluster', 'NAME')
    current_profile = profile.Profile(selector.main())
    current_profile.get_aws_keys()

    sts_client = client.AWSCLient(
        service='sts',
        access_key=current_profile.access_key,
        secret_key=current_profile.secret_key,
        region=region
    )

    iam_client = client.AWSCLient(
        service='iam',
        access_key=current_profile.access_key,
        secret_key=current_profile.secret_key,
        region=region
    )

    current_profile.get_account_number(sts_client)
    current_profile.get_user_name(iam_client)
    current_profile.get_role_arn(role)

    mfa_session = sts_client.get_session_token(
        current_profile.user_name,
        current_profile.account_number
    )

    eks_client = client.AWSCLient(
        service='eks',
        access_key=mfa_session['Credentials']['AccessKeyId'],
        secret_key=mfa_session['Credentials']['SecretAccessKey'],
        session_token=mfa_session['Credentials']['SessionToken'],
        region=region
    )

    creator.save_session_profile(current_profile.user_name, mfa_session)

    session_token_eks_client = eks_client.session_token_client(region)

    eks.main(
        session_token_eks_client,
        cluster_name,
        current_profile.account_number,
        current_profile.role_arn,
        region
    )

    print('\nYour kube config is now ready to use, please follow these steps to complete setup:\n\
        \t1. backup current ~/.kube/config\n\
        \t2. copy the newly generated kube.config from "./kube.config" to "~/.kube/config" \n\
        \t3. "export AWS_PROFILE={0}-mfa" to set your current profile to the mfa authenticated session.'.format(current_profile.user_name))

if __name__ == '__main__':
    main()
