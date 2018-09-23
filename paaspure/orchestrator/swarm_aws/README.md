# AWS Swarm
Component for connecting to Swarm cluster running on AWS.

### Usage

```yaml
orchestrator:
  components:
    swarm_aws:
      user: docker
      bind_port: 2374
      region: eu-west-1
      tags:
        key: swarm-node-type
        manager_value: manager
        worker_value: worker
```
More coming soon...

### Todo
1. Update Instructions
