# PaaSPure Monitoring

Abstraction module for components used to setup a monitoring solution.

### Usage

```bash
usage: paaspure monitoring

Options:
  -h, --help     show this help message and exit
```

### Sample PureFile

```yaml
monitoring:
  orchestrator: $ORCHESTRATOR_NAME
  components:
    $COMPONENT_NAME:
      $COMPONENT_ARG1: $VAL1
      ...
```
