import json
import sys
from io import StringIO
from jsonipy.main import main


def test_simple_json5_conversion(simple_json5, monkeypatch, capsys):
    """Test conversion of simple JSON5 to JSON."""
    monkeypatch.setattr('sys.stdin', StringIO(simple_json5))
    monkeypatch.setattr('sys.argv', ['jsonipy', 'json5'])

    try:
        main()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    result = json.loads(captured.out)

    assert result['title'] == "Simple JSON5 Example"
    assert result['count'] == 42
    assert result['enabled'] is True
    assert result['pi'] == 3.14
    assert result['database']['host'] == "localhost"
    assert result['database']['port'] == 5432


def test_complex_json5_conversion(complex_json5, monkeypatch, capsys):
    """Test conversion of complex JSON5 with nested structures and arrays."""
    monkeypatch.setattr('sys.stdin', StringIO(complex_json5))
    monkeypatch.setattr('sys.argv', ['jsonipy', 'json5'])

    try:
        main()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    result = json.loads(captured.out)

    assert result['title'] == "Complex JSON5 Example"
    assert result['tags'] == ["config", "test", "example"]
    assert result['server']['enabled'] is True
    assert result['server']['ports'] == [8080, 8081, 8082]
    assert result['server']['auth']['username'] == "admin"
    assert result['server']['auth']['timeout'] == 30
    assert len(result['services']) == 2
    assert result['services'][0]['name'] == "web"
    assert result['services'][1]['name'] == "api"


def test_json5_with_comments_and_trailing_commas(monkeypatch, capsys):
    """Test JSON5 features like comments and trailing commas."""
    json5_content = """{
  // Single line comment
  /* Multi-line
     comment */
  key1: "value1",
  key2: 42,
  array: [1, 2, 3,], // trailing comma in array
  nested: {
    prop: "test",
  }, // trailing comma in object
}"""

    monkeypatch.setattr('sys.stdin', StringIO(json5_content))
    monkeypatch.setattr('sys.argv', ['jsonipy', 'json5'])

    try:
        main()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    result = json.loads(captured.out)

    assert result['key1'] == "value1"
    assert result['key2'] == 42
    assert result['array'] == [1, 2, 3]
    assert result['nested']['prop'] == "test"


def test_json5_unquoted_keys(monkeypatch, capsys):
    """Test JSON5 with unquoted keys."""
    json5_content = """{
  unquotedKey: "value",
  'singleQuoted': "value2",
  "doubleQuoted": "value3"
}"""

    monkeypatch.setattr('sys.stdin', StringIO(json5_content))
    monkeypatch.setattr('sys.argv', ['jsonipy', 'json5'])

    try:
        main()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    result = json.loads(captured.out)

    assert result['unquotedKey'] == "value"
    assert result['singleQuoted'] == "value2"
    assert result['doubleQuoted'] == "value3"


def test_json5_numbers(monkeypatch, capsys):
    """Test JSON5 number formats."""
    json5_content = """{
  hexadecimal: 0xFF,
  leadingDecimal: .5,
  trailingDecimal: 5.,
  positiveSign: +42,
  infinity: Infinity,
  negativeInfinity: -Infinity
}"""

    monkeypatch.setattr('sys.stdin', StringIO(json5_content))
    monkeypatch.setattr('sys.argv', ['jsonipy', 'json5'])

    try:
        main()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    result = json.loads(captured.out)

    assert result['hexadecimal'] == 255
    assert result['leadingDecimal'] == 0.5
    assert result['trailingDecimal'] == 5.0
    assert result['positiveSign'] == 42
    # Note: Infinity values may be handled differently by JSON serialization
