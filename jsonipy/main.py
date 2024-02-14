import argparse
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description='Convert something to JSON')
    parser.add_argument('source_format', type=str, help='Source format', choices=['toml', 'yaml', 'json5', 'hcl2'])
    args = parser.parse_args()

    data = None
    if args.source_format == 'toml':
        import tomllib
        data = tomllib.loads(sys.stdin.read())
    elif args.source_format == 'yaml':
        try:
            import yaml
        except ImportError:
            print("You need to install PyYAML to use this feature (e.g. pip install pyyaml)", file=sys.stderr)
            return 1
        data = yaml.safe_load(sys.stdin.read())
    elif args.source_format == 'json5':
        try:
            import pyjson5
        except ImportError:
            print("You need to install json5 to use this feature (e.g. pip install pyjson5)", file=sys.stderr)
            return 1
        data = pyjson5.loads(sys.stdin.read())
    elif args.source_format == 'hcl2':
        try:
            import hcl2
        except ImportError:
            print("You need to install hcl2 to use this feature (e.g. pip install python-hcl2)", file=sys.stderr)
            return 1
        data = hcl2.loads(sys.stdin.read())
    else:
        print(f"Unsupported source format {args.source_format}", file=sys.stderr)
        return 1
    print(json.dumps(data, indent=4))
    return 0


if __name__ == '__main__':
    sys.exit(main())
