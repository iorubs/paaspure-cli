# PaaSPure CLI

>  This is was created as part of my computing masters practicum. The PaaSPure CLI was intended to be used for building/deploying PaaS platforms based on user supplied configs. The cli tool will still work without the HUB as users may still pull directly from a git repo.


#### Build

```bash
docker build -t paaspure .
```

#### Run

```bash
docker run -it --rm \
	-v "$(pwd)":/app \
	-v /var/run/docker.sock:/var/run/docker.sock \
paaspure sh
```

This will mount the current folder as a volume mapped to /app inside the container. So that any changes done on your machine will also be reflected inside the container.

## CI/CD

#### Lint using Flake8
Flak8 is a linting tool, for ensuring compliance with pep8, pyflakes and circular complexity.

```bash
docker run --rm paaspure flake8
```

#### Unit test using PyTest
```bash
docker run --rm paaspure pytest
```

## TODO
* Move pure objects to their own repos.
* Clean up code.
* Remove credentials from config and read from creds file.
