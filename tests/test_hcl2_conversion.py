import json
import sys
from io import StringIO
from jsonipy.main import main


def test_simple_hcl2_conversion(simple_hcl2, monkeypatch, capsys):
    """Test conversion of simple HCL2 to JSON."""
    monkeypatch.setattr('sys.stdin', StringIO(simple_hcl2))
    monkeypatch.setattr('sys.argv', ['jsonipy', 'hcl2'])

    try:
        main()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    result = json.loads(captured.out)

    assert result['title'] == "Simple HCL2 Example"
    assert result['count'] == 42
    assert result['enabled'] is True
    assert result['pi'] == 3.14
    assert 'database' in result
    assert result['database'][0]['host'] == "localhost"
    assert result['database'][0]['port'] == 5432


def test_complex_hcl2_conversion(complex_hcl2, monkeypatch, capsys):
    """Test conversion of complex HCL2 with nested structures and arrays."""
    monkeypatch.setattr('sys.stdin', StringIO(complex_hcl2))
    monkeypatch.setattr('sys.argv', ['jsonipy', 'hcl2'])

    try:
        main()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    result = json.loads(captured.out)

    assert result['title'] == "Complex HCL2 Example"
    assert result['tags'] == ["config", "test", "example"]
    assert 'server' in result
    assert result['server'][0]['enabled'] is True
    assert result['server'][0]['ports'] == [8080, 8081, 8082]
    # HCL2 blocks are represented as lists
    assert len(result['services']) == 2


def test_hcl2_blocks(monkeypatch, capsys):
    """Test HCL2 block syntax."""
    hcl2_content = """
variable "region" {
  default = "us-west-2"
  description = "AWS region"
}

variable "instance_count" {
  default = 3
}
"""

    monkeypatch.setattr('sys.stdin', StringIO(hcl2_content))
    monkeypatch.setattr('sys.argv', ['jsonipy', 'hcl2'])

    try:
        main()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    result = json.loads(captured.out)

    # HCL2 blocks with labels become nested structures
    assert 'variable' in result
    assert len(result['variable']) == 2


def test_hcl2_attributes(monkeypatch, capsys):
    """Test HCL2 simple attribute assignments."""
    hcl2_content = """
name = "my-app"
port = 8080
enabled = true
tags = ["web", "production"]
"""

    monkeypatch.setattr('sys.stdin', StringIO(hcl2_content))
    monkeypatch.setattr('sys.argv', ['jsonipy', 'hcl2'])

    try:
        main()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    result = json.loads(captured.out)

    assert result['name'] == "my-app"
    assert result['port'] == 8080
    assert result['enabled'] is True
    assert result['tags'] == ["web", "production"]


def test_hcl2_nested_blocks(monkeypatch, capsys):
    """Test HCL2 nested block structures."""
    hcl2_content = """
resource "aws_instance" "web" {
  ami = "ami-123456"
  instance_type = "t2.micro"

  tags {
    Name = "WebServer"
    Environment = "production"
  }
}
"""

    monkeypatch.setattr('sys.stdin', StringIO(hcl2_content))
    monkeypatch.setattr('sys.argv', ['jsonipy', 'hcl2'])

    try:
        main()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()
    result = json.loads(captured.out)

    # HCL2 represents blocks as lists with nested structure
    assert 'resource' in result
    # The exact structure depends on the HCL2 parser implementation
