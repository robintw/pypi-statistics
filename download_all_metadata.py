import json
import time

from lxml import html
import requests

def get_all_package_names():
    """Gets a list of all packages on PyPI from the PyPI Simple API service"""
    page = requests.get('https://pypi.org/simple/')
    tree = html.fromstring(page.content)
    package_names = tree.xpath('//a/text()')
    return package_names

def get_package_json(package_name):
    """Get the JSON metadata for a package given the package name, using the PyPI JSON API"""
    headers = {'user-agent': 'robin-statistics - robin@rtwilson.com'}
    page = requests.get('https://pypi.org/pypi/%s/json' % package_name, headers=headers)
    json_string = page.text
    
    return json_string

package_names = get_all_package_names()

# Download JSON metadata for all packages
for index, package_name in enumerate(package_names):
    # If the file we're going to download to already exists then skip
    # downloading it again
    if os.path.exists('all_metadata/' + package_name + '.json'):
        continue

    # Get the JSON and write it out to a file
    json_string = get_package_json(package_name)
    with open('all_metadata/' + package_name + '.json', 'w') as f:
        f.write(json_string)
    
    # Sleep for 2 minutes every 500 downloads, to avoid hammering PyPI too much
    if index % 500 == 0:
        print(index)
        time.sleep(2*60)
