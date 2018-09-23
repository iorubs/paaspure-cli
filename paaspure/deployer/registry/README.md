# Registry
Image repository and visualizer

### Usage

```yaml
deployer:
  orchestrator: orchestrator
  components:
    registry:
```

add registry.demo as an insecure registry

More coming soon...


### Generate certs
  docker run --rm \
  -v "$(pwd)/certs":/certs \
  -e SSL_IP=172.17.8.101 \
  -e SSL_DNS=registry.demo \
  paulczar/omgwtfssl

docker run --rm \
  -v "$(pwd)/certs":/certs \
  -e SSL_SUBJECT=registry.demo \
  -e SSL_DNS=registry.demo \
  paulczar/omgwtfssl

### Todo
1. Fix portus or find another solution.
2. Update Instructions
