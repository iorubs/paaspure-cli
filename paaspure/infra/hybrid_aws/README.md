# PaaSPure Extend Swarm

PaaSPure component for extending existing swarm. Provisioning AWS resources using terraform and configuration using Ansible.

## Networking
Open protocols and ports between the hosts
The following ports must be available. On some systems, these ports are open by default.

#### Required
TCP port 2377 for cluster management communications
TCP and UDP port 7946 for communication among nodes
UDP port 4789 for overlay network traffic

#### Optional
TCP port 22 for ssh

## Usage

```yaml
hybrid_aws:
  aws_region: "eu-west-1"
  aws_key_name: "paaspure"
  ssh_user: "docker"
  manager_instance_type: "t2.micro"
  manager_count: 1
  worker_instance_type: "t2.micro"
  worker_count: 1
  orchestrator_params:
    name: 'orchestrator'
    component: 'swarm_azure'
    resource_group_name: paaspureswarm
    swarmName: "dockerswarm"
```


Validate template by adding '--syntax-check' to the execute command
E.g ['--syntax-check', '-i', 'swarm-inventory', 'swarm-leave.yml']
