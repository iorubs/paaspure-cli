# -*- coding: utf-8 -*-

import os
import pytest
import docker

# TODO: Remove mock from requirements.txt
# from mock import MagicMock
from paaspure.utils import build_image, write_yaml_file, MockContainerRun
from .component import instance


@pytest.fixture(scope="function")
def resource_file():
    """ New module name and cleanup work."""
    resources = os.path.join(
        os.path.dirname(__file__),
        'resources.yml'
    )
    yield resources
    os.remove(resources)


class TestPackerAWS:
    resource_file = os.path.join(
        os.path.dirname(__file__),
        'resources.yml'
    )

    def test_validate_packer_template(self):
        client = docker.from_env()

        build_image(
            image_tag='paaspure_packer_test',
            path=os.path.dirname(__file__)
        )
        assert client.images.get('paaspure_packer_test') is not None

        container = client.containers.run(
            'paaspure_packer_test',
            command=[
                'validate',
                '-var-file=variables.json',
                'docker_ubuntu.json'
            ],
            detach=True
        )

        output = []

        for log in container.logs(stdout=True, stderr=True, stream=True):
            output.append(log.decode())

        assert 'Template validated successfully.' in ''.join(output)

        client.images.remove('paaspure_packer_test')

        with pytest.raises(docker.errors.ImageNotFound):
            client.images.get('paaspure_packer_test')

    def test_invalid_inputs(self, resource_file):
        assert not os.path.exists(resource_file)

        with pytest.raises(Exception):
            instance.build(
                {'template': '', 'region': '', 'var-files': ['']},
                {'aws_access_key': '', 'aws_secret_key': ''}
            )

        # No file to read from
        instance.destroy(
            {'template': '', 'region': 'eu-west-1', 'var-files': ['']},
            {'aws_access_key': '', 'aws_secret_key': ''}
        )

        # Try to remove non-existent resources
        dummy_resources = {
            'images': ['ami-a046fake'],
            'snapshots': ['snap-a046fake']
        }

        write_yaml_file(dummy_resources, resource_file)

        instance.destroy(
            {'template': '', 'region': 'eu-west-1', 'var-files': ['']},
            {'aws_access_key': '', 'aws_secret_key': ''}
        )

    def test_mock_run(self, monkeypatch, resource_file):
        assert not os.path.exists(resource_file)

        mock_container = MockContainerRun(
            log_output=[
                'AMI: ami-a046ebce',
                'Snapshot: snap-a046eaae'
            ],
            status_code=0
        )

        monkeypatch.setattr(docker, 'from_env', mock_container)

        instance.build(
            {'template': '', 'region': '', 'var-files': ['']},
            {'aws_access_key': '', 'aws_secret_key': ''}
        )

        assert os.path.exists(resource_file)
