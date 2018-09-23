# PaaSPure Generic Parser

### Generic ArgParse
By default the generic parser just parses 3 arguments:

```bash
	-f, --file		Name of the cofig file (Default is 'PATH/pure.yml').
	-v, --version 	Show version number and exit.
	-h, --help		Show help message and exit.
```

At runtime the parser is extended based on the modules defined in the cofig file. This allows the CLI tool to adapt to it's users and provide a sanitized output.


### Extending the default ArgParse
New modules are able to extend the parser features, simply by importing it and adding the new arguments to it.

```python
# -*- coding: utf-8 -*-

from paaspure.argparser import paaSPureParser


class NewModuleParser:
    def __init__(self, module):
        module.parser = paaSPureParser.extend_parser(
            'paaspure new_module COMMAND',
            'new_module',
            'New auto-generated module.'
        )

        sub_parsers = module.parser.add_subparsers(
            title='Commands',
            dest='subcommand'
        )

        module.run_parser = sub_parsers.add_parser(
            'build',
            help='Run the NewModule module.',
            usage='paaspure new_module run'
        )

        module.run_parser._optionals.title = 'Options'
        module.run_parser._positionals.title = 'Commands'
        module.run_parser.set_defaults(parser=True)

        super(NewModuleParser, self).__init__()
```

Running ```paaspure new_module``` would output:

```bash
usage: paaspure new_module COMMAND

Options:
  -h, --help  show this help message and exit

Commands:
  {run}
    run       Run the NewModule module.
```
