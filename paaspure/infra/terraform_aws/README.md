# PaaSPure Terraform AWS

PaaSPure component for provisioning AWS resources using terraform.

### Usage
Tested with the infra module: https://github.com/iorubs/paaspure_infra.git

```bash
Usage:
    run          Provisioning resources.
    destroy      Destroy resources.
```


# Sample pure.yml

```yaml
version: 1

credentials:
  aws_access_key: ACCESS_KEY
  aws_secret_key: SECRET_KEY

modules:
  infra:
    components:
      docker_for_aws:
        stack_name: "PaasPureDocker"
        region: "eu-west-1"
        parameters:
          KeyName: "paaspure"
          ManagerSize: 1
          ManagerInstanceType: "t2.micro"
          ClusterSize: 1
          InstanceType: "t2.micro"
```
