import os
import re
from profile import creator
from tools.inquire import inquire
from tools.userAccept import yes_or_no


def select():
    profiles = collect_profiles()
    profiles.append('create new profile')
    selection = inquire("profile", "select profile or create new", profiles)
    selected = selection['profile']

    return selected


def collect_profiles():
    profiles = [re.findall(r'\[(.*?)\]',line) for line in open(os.path.expanduser('~/.aws/credentials'))]
    profile_list = [item for sublist in profiles for item in sublist]

    return profile_list


def selector():
    selection = select()
    if selection in collect_profiles():
        selected_profile = select_existing(selection)
    else:
        selected_profile = create()

    return selected_profile


def select_existing(profile_name):
    if yes_or_no('selected profile: %s' % profile_name):

        return profile_name
    else:
        selector()


def create():
    if yes_or_no('create new profile?'):
        profile_name = creator.configure()

        return profile_name
    else:
        selector()


def main():
    profile_name = selector()
    return profile_name


if __name__ == '__main__':
    main()
