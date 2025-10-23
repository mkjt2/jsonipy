import json
import sys
from io import StringIO
from jsonipy.main import main


def test_simple_yaml_conversion(simple_yaml, monkeypatch, capsys):
    """Test conversion of simple YAML to JSON."""
    monkeypatch.setattr('sys.stdin', StringIO(simple_yaml))
    monkeypatch.setattr('sys.argv', ['jsonipy', 'yaml'])

    try:
        main()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    result = json.loads(captured.out)

    assert result['title'] == "Simple YAML Example"
    assert result['count'] == 42
    assert result['enabled'] is True
    assert result['pi'] == 3.14
    assert result['database']['host'] == "localhost"
    assert result['database']['port'] == 5432


def test_complex_yaml_conversion(complex_yaml, monkeypatch, capsys):
    """Test conversion of complex YAML with nested structures and arrays."""
    monkeypatch.setattr('sys.stdin', StringIO(complex_yaml))
    monkeypatch.setattr('sys.argv', ['jsonipy', 'yaml'])

    try:
        main()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    result = json.loads(captured.out)

    assert result['title'] == "Complex YAML Example"
    assert result['tags'] == ["config", "test", "example"]
    assert result['server']['enabled'] is True
    assert result['server']['ports'] == [8080, 8081, 8082]
    assert result['server']['auth']['username'] == "admin"
    assert result['server']['auth']['timeout'] == 30
    assert len(result['services']) == 2
    assert result['services'][0]['name'] == "web"
    assert result['services'][1]['name'] == "api"


def test_yaml_multiline_strings(monkeypatch, capsys):
    """Test YAML conversion with multiline strings."""
    yaml_content = """
description: |
  This is a multiline
  string that should be
  preserved properly
folded: >
  This is a folded
  string that will become
  a single line
"""

    monkeypatch.setattr('sys.stdin', StringIO(yaml_content))
    monkeypatch.setattr('sys.argv', ['jsonipy', 'yaml'])

    try:
        main()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    result = json.loads(captured.out)

    assert "This is a multiline" in result['description']
    assert "This is a folded" in result['folded']


def test_yaml_with_null_values(monkeypatch, capsys):
    """Test YAML conversion with null/None values."""
    yaml_content = """
key1: value1
key2: null
key3: ~
key4:
"""

    monkeypatch.setattr('sys.stdin', StringIO(yaml_content))
    monkeypatch.setattr('sys.argv', ['jsonipy', 'yaml'])

    try:
        main()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    result = json.loads(captured.out)

    assert result['key1'] == "value1"
    assert result['key2'] is None
    assert result['key3'] is None
    assert result['key4'] is None


def test_empty_yaml(monkeypatch, capsys):
    """Test conversion of empty YAML input."""
    monkeypatch.setattr('sys.stdin', StringIO(""))
    monkeypatch.setattr('sys.argv', ['jsonipy', 'yaml'])

    try:
        main()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    result = json.loads(captured.out)

    # Empty YAML should produce null/None
    assert result is None
