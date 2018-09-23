# PaaSPure Packer AWS

PaaSPure component for building and provisioning AWS cloud images using packer.

### Usage
Tested with the vm_builder module: https://github.com/iorubs/paaspure_vm_builder.git

```bash
Usage:
    run          Build IMAs.
    destroy      Destroy IMAs and Snapshots
```


# Sample pure.yml

```yaml
version: 1

credentials:
  aws_access_key: ACCESS_KEY
  aws_secret_key: SECRET_KEY

modules:
  vm_builder:
    packer_aws:
      template: PACKER_TEMPLATE_FILE
      region: REGION
      var-files:
          - PACKER_VARIABLES_FILE
```
