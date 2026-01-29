# Publishing `ccp-sdk` to PyPI

This repo contains a reference Python package (`ccp-sdk`).

## 1) Build

From the repo root:

```bash
python -m pip install -U build twine
python -m build
```

Artifacts will be created in `dist/`.

## 2) Publish to TestPyPI (recommended first)

```bash
python -m twine upload --repository testpypi dist/*
```

Test install:

```bash
python -m pip install -i https://test.pypi.org/simple/ ccp-sdk
```

## 3) Publish to PyPI

```bash
python -m twine upload dist/*
```

## Notes
- Consider replacing the placeholder URLs in `pyproject.toml`.
- Pick a unique package name if `ccp-sdk` is taken on PyPI.
- If you change schemas/spec, bump the package version.
