# PaaSPure Generator

The generator is built into paaspure and allows users to quickly generate scaffolding code and tests.

### Usage

```bash
usage: paaspure generate TEMPLATE

Options:
  -h, --help          show this help message and exit

Templates:
  {module,component}
    module            Generate template for a new module.
    component         Generate template for a new component.
```


### Module
Modules provide a layer of abstraction for running all the different components and represent things such as logging, CI or monitoring.


```bash
usage: paaspure generate module NAME

Arguments:
  NAME                The name of the new module.

Options:
  -h, --help          show this help message and exit
```


### Component
A module may have many components, components are usually orchestrator specific composed of things such as Dockerfiles, stackfiles and component specific tests.


```bash
usage: paaspure generate component PARENT_MODULE NAME

Arguments:
  PARENT_MODULE       The parent module name.
  NAME                The name of the new component.

Options:
  -h, --help          show this help message and exit
```
