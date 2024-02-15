# Jsonipy - CLI to convert stuff to JSON

## Install

Use [pipx](https://github.com/pypa/pipx).

```bash
pipx install git+https://github.com/mkjt2/jsonipy.git
```

## Usage

```text
usage: jsonipy [-h] {toml,yaml,json5,hcl2}

Convert something from stdin to JSON

positional arguments:
{toml,yaml,json5,hcl2}
Source format

options:
-h, --help            show this help message and exit
```

### Example

Convert a YAML file to JSON, print the result.

```bash
cat some.yaml | jsonipy yaml
```

## What for?

This might pair well with the powerful [jq](https://jqlang.github.io/jq//). E.g. analyze a TOML file using `jq`
commands.