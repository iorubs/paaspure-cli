# PaaSPure Infra Builder

Abstraction module for components used to build the infrastructure.
Run cloud VMs and setup cluster.

### Usage

```bash
usage: paaspure orchestrator

Options:
  -h, --help     show this help message and exit
```

### Sample PureFile

```yaml
orchestrator:
  components:
    $COMPONENT_NAME:
      $COMPONENT_ARG1: $VAL1
      ...
```
