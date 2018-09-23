# PaaSPure Deployer

A general module for deploying stuff.

### Usage

```bash
usage: paaspure deployer

Options:
  -h, --help     show this help message and exit
```

### Sample PureFile

```yaml
deployer:
  orchestrator: $ORCHESTRATOR_NAME
  components:
    $COMPONENT_NAME:
      $COMPONENT_ARG1: $VAL1
      ...
```
