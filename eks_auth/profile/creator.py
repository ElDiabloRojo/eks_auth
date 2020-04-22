import os
from profile import selector
from tools.userAccept import yes_or_no, request_value


def configure():
    saved = False
    while not saved:
        profile_keys = ['profile name', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']
        profile = {}
        print('please enter the details for your new profile:\n')
        for k in profile_keys:
            profile[k] = request_value(k)
        if yes_or_no('\nare these details correct?:\n{0}'.format(profile)):
            verify_profile_exists(profile)
            saved = True
        else:
            print('\nrestarting profile input:\n')
            saved = False
    profile_name = profile['profile name']
    print(profile_name)

    return profile_name


def save_profile(profile):
    with open(os.path.expanduser('~/.aws/credentials'), 'a') as credentials_file:
        credentials_file.write('\n[%s]\n' % str(profile['profile name']))
        credentials_file.write('aws_access_key_id = %s\n' % str(profile['AWS_ACCESS_KEY_ID']))
        credentials_file.write('aws_secret_access_key = %s\n' % str(profile['AWS_SECRET_ACCESS_KEY']))


def save_session_profile(profile_name, mfa_session):
    with open(os.path.expanduser('~/.aws/credentials'), 'a') as credentials_file:
        credentials_file.write('\n[{0}-mfa]\n'.format(profile_name))
        credentials_file.write('aws_access_key_id = {0}\n'.format(mfa_session['Credentials']['AccessKeyId']))
        credentials_file.write('aws_secret_access_key = {0}\n'.format(mfa_session['Credentials']['SecretAccessKey']))
        credentials_file.write('aws_session_token = {0}\n'.format(mfa_session['Credentials']['SessionToken']))

def verify_profile_exists(profile):
    while profile['profile name'] in selector.collect_profiles():
        print('profile already exists, please change\n')
        profile['profile name'] = request_value('profile name')
    print('saving profile...')
    save_profile(profile)
