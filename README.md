# Jsonipy - CLI tool to convert various file formats to JSON

## Install

Use [pipx](https://github.com/pypa/pipx).

```bash
pipx install jsonipy
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