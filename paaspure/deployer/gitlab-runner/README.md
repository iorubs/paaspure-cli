# GitLab Runner

### Instructions:

 * For now you have to register a runner manually. Might automate this in the future.
 * How to register a runner: https://docs.gitlab.com/runner/register/
 * You should end-up with a config.toml file similar to config/config.toml.template:


```text
concurrent = 1
check_interval = 0

[[runners]]
  name = "PaaSPure Runner"
  url = "INSERT URL HERE"
  token = "INSERT YOUR TOKEN HERE"
  executor = "shell"
  [runners.cache]

```

 * Put config.toml inside the config folder.

 * Build agent

```bash
docker-compose build
```

 * Start agent

```bash
docker-compose up -d
```

### TODO
* Add component.py and and script for initiating runner.
