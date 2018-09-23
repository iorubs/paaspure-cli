# PaaSPure Logging

Abstraction module for components used to setup a logging solution.

### Usage

```bash
usage: paaspure logging

Options:
  -h, --help     show this help message and exit
```

### Sample PureFile

```yaml
log_management:
  orchestrator: $ORCHESTRATOR_NAME
  components:
    $COMPONENT_NAME:
      $COMPONENT_ARG1: $VAL1
      ...
```
