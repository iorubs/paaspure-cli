# PaaSPure Network

Abstraction module for setting up network components. Things like reverse proxy and ssl certs

### Usage

```bash
usage: paaspure network

Options:
  -h, --help     show this help message and exit
```

### Sample PureFile

```yaml
network:
  orchestrator: $ORCHESTRATOR_NAME
  components:
    $COMPONENT_NAME:
      $COMPONENT_ARG1: $VAL1
      ...
```
