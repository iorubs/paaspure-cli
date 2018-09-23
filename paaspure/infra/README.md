# PaaSPure Infra Builder

Abstraction module for components used to build the infrastructure.
Run cloud VMs and setup cluster.

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
infra:
  components:
    $COMPONENT_NAME:
      $COMPONENT_ARG1: $VAL1
      ...
```
