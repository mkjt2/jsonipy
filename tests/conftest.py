import pytest
from pathlib import Path


@pytest.fixture
def fixtures_dir():
    """Return the path to the fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def simple_toml(fixtures_dir):
    """Read simple TOML fixture."""
    return (fixtures_dir / "simple.toml").read_text()


@pytest.fixture
def simple_yaml(fixtures_dir):
    """Read simple YAML fixture."""
    return (fixtures_dir / "simple.yaml").read_text()


@pytest.fixture
def simple_json5(fixtures_dir):
    """Read simple JSON5 fixture."""
    return (fixtures_dir / "simple.json5").read_text()


@pytest.fixture
def simple_hcl2(fixtures_dir):
    """Read simple HCL2 fixture."""
    return (fixtures_dir / "simple.hcl2").read_text()


@pytest.fixture
def complex_toml(fixtures_dir):
    """Read complex TOML fixture."""
    return (fixtures_dir / "complex.toml").read_text()


@pytest.fixture
def complex_yaml(fixtures_dir):
    """Read complex YAML fixture."""
    return (fixtures_dir / "complex.yaml").read_text()


@pytest.fixture
def complex_json5(fixtures_dir):
    """Read complex JSON5 fixture."""
    return (fixtures_dir / "complex.json5").read_text()


@pytest.fixture
def complex_hcl2(fixtures_dir):
    """Read complex HCL2 fixture."""
    return (fixtures_dir / "complex.hcl2").read_text()
