import json
import sys
from io import StringIO
from jsonipy.main import main


def test_simple_toml_conversion(simple_toml, monkeypatch, capsys):
    """Test conversion of simple TOML to JSON."""
    # Mock stdin with TOML content
    monkeypatch.setattr('sys.stdin', StringIO(simple_toml))
    monkeypatch.setattr('sys.argv', ['jsonipy', 'toml'])

    # Run the converter
    try:
        main()
    except SystemExit as e:
        assert e.code == 0

    # Capture and parse output
    captured = capsys.readouterr()
    result = json.loads(captured.out)

    # Verify expected structure
    assert result['title'] == "Simple TOML Example"
    assert result['count'] == 42
    assert result['enabled'] is True
    assert result['pi'] == 3.14
    assert result['database']['host'] == "localhost"
    assert result['database']['port'] == 5432


def test_complex_toml_conversion(complex_toml, monkeypatch, capsys):
    """Test conversion of complex TOML with nested structures and arrays."""
    monkeypatch.setattr('sys.stdin', StringIO(complex_toml))
    monkeypatch.setattr('sys.argv', ['jsonipy', 'toml'])

    try:
        main()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    result = json.loads(captured.out)

    # Verify complex structure
    assert result['title'] == "Complex TOML Example"
    assert result['tags'] == ["config", "test", "example"]
    assert result['server']['enabled'] is True
    assert result['server']['ports'] == [8080, 8081, 8082]
    assert result['server']['auth']['username'] == "admin"
    assert result['server']['auth']['timeout'] == 30
    assert len(result['services']) == 2
    assert result['services'][0]['name'] == "web"
    assert result['services'][1]['name'] == "api"


def test_toml_with_various_data_types(monkeypatch, capsys):
    """Test TOML conversion with various data types."""
    toml_content = """
string_value = "hello"
int_value = 42
float_value = 3.14159
bool_true = true
bool_false = false
array_mixed = [1, 2, 3]

[nested]
key = "value"
"""

    monkeypatch.setattr('sys.stdin', StringIO(toml_content))
    monkeypatch.setattr('sys.argv', ['jsonipy', 'toml'])

    try:
        main()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    result = json.loads(captured.out)

    assert result['string_value'] == "hello"
    assert result['int_value'] == 42
    assert result['float_value'] == 3.14159
    assert result['bool_true'] is True
    assert result['bool_false'] is False
    assert result['array_mixed'] == [1, 2, 3]
    assert result['nested']['key'] == "value"


def test_empty_toml(monkeypatch, capsys):
    """Test conversion of empty TOML input."""
    monkeypatch.setattr('sys.stdin', StringIO(""))
    monkeypatch.setattr('sys.argv', ['jsonipy', 'toml'])

    try:
        main()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    result = json.loads(captured.out)

    # Empty TOML should produce empty object
    assert result == {}
