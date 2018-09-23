# -*- coding: utf-8 -*-

import os
import pytest
import docker

from paaspure.utils import MockContainerRun
from .component import instance


@pytest.fixture(scope="function")
def tfvars():
    """ Cleanup work."""
    vars = {'parameters': {'linuxSSHPublicKey': __file__}}

    tfvars_path = os.path.join(
        os.path.dirname(__file__),
        'terraform.tfvars'
    )

    tfvars = {'vars': vars, 'path': tfvars_path}
    yield tfvars
    os.remove(tfvars['path'])


class TestTerraformAzure:
    def test_mock_run(self, capsys, monkeypatch, tfvars):
        assert not os.path.exists(tfvars['path'])

        mock_container = MockContainerRun(
            log_output=['Some Output'],
            status_code=1
        )

        monkeypatch.setattr(docker, 'from_env', mock_container)

        instance.build(
            tfvars['vars'],
            {'azure_client_id': '', 'azure_client_secret': '',
             'azure_tenant_id': '', 'subscription_id': ''}
        )

        assert os.path.exists(tfvars['path'])
        out, _ = capsys.readouterr()
        assert 'Some Output' in out
        assert 'Container execution failed' in out

    def test_mock_destroy(self, capsys, monkeypatch):
        # assert os.path.exists(tfvars['path'])

        mock_container = MockContainerRun(
            log_output=[],
            status_code=1
        )

        monkeypatch.setattr(docker, 'from_env', mock_container)

        instance.destroy({}, {'azure_client_id': '', 'azure_client_secret': '',
                              'azure_tenant_id': '', 'subscription_id': ''})

        # TODO: Should check for removed files
        # assert not os.path.exists(tfvars['path'])
        out, _ = capsys.readouterr()
        assert 'Container execution failed' in out

    @pytest.mark.skip(reason='Still not sure what tfvars must look like.')
    def test_validate_tfvars(self):
        # TODO: Should pass in some dummy cred and ensure tfvars is valid.
        pass
