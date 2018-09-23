# PaaSPure VM Builder

Abstraction module for components used to build cloud images.

### Usage

```bash
usage: paaspure vm_builder COMMAND

Options:
  -h, --help     show this help message and exit

Commands:
  {run,destroy}
    run          Run the VmBuilder module.
    destroy      Destroy VmBuilder resources.
```

### Sample PureFile

```yaml
vm_builder:
  repo:
  commit:
  components:
    packer_aws:
      template: docker_ubuntu.json
      region: eu-west-1
      var-files:
        - variables.json
```
