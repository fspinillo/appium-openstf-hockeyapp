import requests
import os
import sys
import argparse
from dotenv import load_dotenv


"""Load environment variables from .env"""
dotenv_path = (os.path.join(sys.path[0], '../.env'))
load_dotenv(dotenv_path)

app_token = os.environ.get("HOCKEY")

"""This referrs to the ID for your RC/Dev builds to be tested"""
android_rc = os.environ.get("ANDROID_RC")

"""This referrs to the ID for the builds in the Play store"""
android_store = os.environ.get("ANDROID_STORE")
base_url = "https://rink.hockeyapp.net/api/2/apps"

"""Define the Android version to download"""
parser = argparse.ArgumentParser(
    description='Determine what to download from HockeyApp')
parser.add_argument("--rc", action="store_true",
                    default=False, help="Download latest Android RC build")
parser.add_argument("--store", action="store_true",
                    default=False, help="Download latest Android Store build")
parser.add_argument("--version", nargs='?',
                    default=None, help="Download version of RC or Store")

args = parser.parse_args()

if args.rc is False and args.store is False:
    raise Exception('You must define an app to download')

if args.rc is True and args.store is True:
    raise Exception('You cannot define two apps')

if (args.rc is False and args.store is False) and args.version is not None:
    raise Exception('You cannot define a version without an app')

header = {'X-HockeyAppToken': app_token}

if args.rc is True and args.version is None:
    versions = requests.get("{BASE}/{APP}/app_versions?page=1&include_build_urls=true".format(
        BASE=base_url, APP=android_rc), headers=header).json()
    download_url = str(versions['app_versions'][0]['build_url'])
    apk = requests.get(download_url, headers=header, stream=True)
    with open('app/app.apk', 'wb') as f:
        f.write(apk.content)
elif args.rc is True and args.version is not None:
    versions = requests.get("{BASE}/{APP}/app_versions?page=1&include_build_urls=true".format(
        BASE=base_url, APP=android_rc), headers=header).json()
    i = 0
    app_found = False
    while app_found is False and i < len(versions['app_versions']):
        for version in versions['app_versions']:
            if args.version == str(version['version']):
                download_url = str(version['build_url'])
                apk = requests.get(download_url, headers=header, stream=True)
                with open('app/app.apk', 'wb') as f:
                    f.write(apk.content)
                app_found = True
                break
            else:
                i += 1
    if app_found is False:
        raise Exception('Unable to find app version')

if args.store is True and args.version is None:
    versions = requests.get("{BASE}/{APP}/app_versions?page=1&include_build_urls=true".format(
        BASE=base_url, APP=android_store), headers=header).json()
    download_url = str(versions['app_versions'][0]['build_url'])
    apk = requests.get(download_url, headers=header, stream=True)
    with open('app/app.apk', 'wb') as f:
        f.write(apk.content)
elif args.store is True and args.version is not None:
    versions = requests.get("{BASE}/{APP}/app_versions?page=1&include_build_urls=true".format(
        BASE=base_url, APP=android_store), headers=header).json()
    i = 0
    app_found = False
    while app_found is False and i < len(versions['app_versions']):
        for version in versions['app_versions']:
            if args.version == str(version['version']):
                download_url = str(version['build_url'])
                apk = requests.get(download_url, headers=header, stream=True)
                with open('app/app.apk', 'wb') as f:
                    f.write(apk.content)
                app_found = True
                break
            else:
                i += 1
    if app_found is False:
        raise Exception('Unable to find app version')
