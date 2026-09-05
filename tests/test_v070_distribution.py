from pathlib import Path
import tomllib


def test_distribution_metadata_is_ready():
    root = Path(__file__).resolve().parents[1]
    data = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    project = data["project"]

    assert project["name"] == "docflow-portfolio"
    assert project["requires-python"] == ">=3.11"
    assert project["license"]["text"] == "MIT"
    assert project["scripts"]["docflow"] == "docflow.cli:main"
    assert project["urls"]["Repository"] == "https://github.com/LSANTOSSS/docflow"
    assert "Environment :: Console" in project["classifiers"]
    assert "markdown" in project["keywords"]


def test_distribution_tooling_is_declared():
    root = Path(__file__).resolve().parents[1]
    data = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    dev = data["project"]["optional-dependencies"]["dev"]

    assert any(item.startswith("build") for item in dev)
    assert any(item.startswith("twine") for item in dev)


def test_ci_builds_checks_and_installs_wheel():
    root = Path(__file__).resolve().parents[1]
    workflow = (root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert "python -m build" in workflow
    assert "python -m twine check dist/*" in workflow
    assert "python -m venv /tmp/docflow-wheel-venv" in workflow
    assert "pip install dist/*.whl" in workflow
    assert "docflow --help" in workflow
