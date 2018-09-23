# PaaSPure Puller

Module for pulling other modules and components.

## Usage

```bash
usage: paaspure pull TYPE

Options:
  -h, --help          show this help message and exit
  --git-url GIT_URL   Repo url to pull from.

Commands:
  {module,component}
    module            Pull module
    component         Pull component
```

### Pull Module
```bash
usage: paaspure pull module NAME

Arguments:
  NAME                The module name

Options:
  -h, --help          show this help message and exit
```

### Pull Component

```bash
usage: paaspure pull component PARENT_MODULE NAME

Arguments:
  PARENT_MODULE       The parent module name
  NAME                The component name

Options:
  -h, --help          show this help message and exit
```
