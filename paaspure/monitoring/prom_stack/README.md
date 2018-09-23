# Prom Stack
Monitoring stack with Prometheus and Grafana

### Usage

```yaml
monitoring:
  orchestrator: orchestrator
  components:
    prom_stack:
```
More coming soon...

### Grafana usage
Default username admin
Default password admin

1. Login and create a new Prometheus data point.
2. Import dashboards using their IDs

### Useful dashboards
1442 - node exporter (host stats)
2603 - cadvisor (docker stats)
2240 - traefik reverse proxy stats
3662 - prometheus scraping stats

### Todo
1. Update Instructions
2. Add AlertManager
