import sys
import requests

from paaspure import settings


def __request(url=f'{settings.HUB}/api'):
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        print(f'Could not connect to hub: {settings.HUB}')
        sys.exit(1)

    if response.status_code != 200:
        print(f'Invalid response from hub: {settings.HUB}')
        print(f'\t{response}')
        sys.exit(1)

    return response.json()


def request_objects():
    return __request(url=f'{settings.HUB}/api/hub')


def request_versions(id=None):
    versions = __request(url=f'{settings.HUB}/api/version/{id}')
    return [{'tag': 'latest', 'date': 'now', 'commit': 'master'}] + versions


def get_object(name='', type='module', version='latest'):
    hub_objects = request_objects()

    filtered_hub_objects = [obj for obj in hub_objects
                            if obj['type'] == type and name == obj['name']]

    if len(filtered_hub_objects) == 1:
        return filtered_hub_objects[0]

    hub_objects = [obj for obj in hub_objects
                   if obj['type'] == type and name in obj['name']]

    if len(hub_objects) == 0:
        print(f'Pull failed: {type} {name} does not exist.')
        sys.exit(1)
    if len(hub_objects) >= 1:
        print(f'Could not find a name match for {type}: {name}')
        print(f'Other {type}s with a similar name:')
        for item in hub_objects:
            print('  {:40s} {:s}'.format(
                item['name'],
                item['description']
            ))
        sys.exit(1)


def get_version(hub_object, version):
    versions = request_versions(hub_object['_id'])
    filtered_versions = [vrs for vrs in versions if version == str(vrs['tag'])]

    if len(filtered_versions) == 1:
        return filtered_versions[0]

    filtered_versions = [vrs for vrs in versions if version in str(vrs['tag'])]

    if len(filtered_versions) == 0:
        print(f'Could not find {hub_object["name"]} version {version}.')
        print('Versions available:')
        __print_versions(versions)
        sys.exit(1)
    if len(filtered_versions) >= 1:
        print(f'Could not match {hub_object["name"]} version {version}.')
        print(f'Other similar tags:')
        __print_versions(filtered_versions)
        sys.exit(1)


def __print_versions(versions):
    print('  {:20s} {:20s} {:s}'.format('tag', 'date', 'hash'))
    for item in versions:
        print('  {:20s} {:20s} {:s}'.format(
            str(item['tag']), item['date'], item['commit'])
        )
