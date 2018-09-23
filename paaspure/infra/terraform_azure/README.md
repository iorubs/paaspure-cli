# PaaSPure Packer Azure

PaaSPure component for building and provisioning Azure cloud images using packer.

# Sample pure.yml

```yaml
version: 1

credentials:
  private_key:
  azure_client_id:
  azure_client_secret:
  azure_tenant_id:
  subscription_id:

modules:
  infra:
    components:
      docker_for_azure:
        stack_name: "PaasPureDocker"
        resource_group_name: paaspureswarm
        resource_group_location: "North Europe"
        parameters:
          enableExtLogs: "no"
          linuxSSHPublicKey: /app/paaspure/paaspure.pub
          managerCount: 1
          managerVMSize: "Standard_D1_v2"
          linuxWorkerCount: 1
          linuxWorkerVMSize: "Standard_D1_v2"
          swarmName: "dockerswarm"
```

# Setup permissions (Warning this must be done manually in advance of the first setup.)

## New App Registration

This is required for running tasks programmatically using Terraform. It will generate the required azure_client_id, azure_client_secret and azure_tenant_id.

1. Run ```docker run -it --rm docker4x/create-sp-azure ${SP-NAME}```
2. Where SP-NAME equals the desired app name. E.g paaspure
3. Login to shown URL with the given authentication code.
4. Go back to terminal and select subscription.
5. Wait a couple minutes and you should see the following:

```bash
Your access credentials ==================================================
AD ServicePrincipal App ID:       azure_client_id
AD ServicePrincipal App Secret:   azure_client_secret
AD ServicePrincipal Tenant ID:    azure_tenant_id
```

## Image Permissions (DOCKER FOR AZURE SPECIFIC: You must accept the cloud images)

Without this you will see: "Marketplace purchase eligibilty check returned errors."

1. Run ```docker run -it --rm microsoft/azure-cli```
2. Run ```az login```
3. Login to shown URL with the given authentication code.
4. Go back to terminal.
5. Run ```az vm image accept-terms --urn docker:docker-ce:docker-ce:1.0.18```

Optional: You can list the available linuxImageVersions

1. Run ```az vm image list --all --publisher docker --offer docker-ce --sku docker-ce```
1. Update linuxImageVersion in Docker.tmpl to the desired version.

### Changes made to default Docker for azure tmpl

#### Required
Changed parameters to allow strings (seems like terraform passes Ints to azure templates as Strings)

#### Optional
Added Standard_B1s to available instance types to make use of free subscription resources.

Lines: [360 to 362], [617 to 628] and [674], where changed to open extra ports for hybrid cloud demo. (In the feature this should be done in a separate component for security reasons)
