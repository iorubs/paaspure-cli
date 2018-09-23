import os
import git
import shutil

from paaspure.utils import request_input


def clone(repo_url=None, type=None, target_path=[], commit=None):
    target = os.path.join(*target_path)

    if os.path.exists(target):
        print(f'Found existing {type} {target}: ')
        request_input(
            question='\tWould you like to overwrite it? [Y/n] ',
            reject='\tSkipping pull! ¯\_(ツ)_/¯'
        )

        shutil.rmtree(target)

    repo_name = repo_url.replace('.', '/').split('/')[-2]
    git.Git().clone(repo_url)

    if commit is not None:
        git.Git(repo_name).checkout(commit)

    try:
        # TODO: Fix error handler
        shutil.copytree(repo_name, target)
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    except OSError as e:
        print('Directory not copied. Error: %s' % e)

    shutil.rmtree(repo_name)
