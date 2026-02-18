# Publishing `ccp-sdk` to PyPI

This repo contains a reference Python package (`ccp-sdk`).

Current release (PyPI): https://pypi.org/project/ccp-sdk/0.1.0/

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

If you prefer to pass credentials explicitly:

```bash
python -m twine upload --repository testpypi -u __token__ -p <TESTPYPI_TOKEN> dist/*
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

## Troubleshooting

### `HTTPError: 403 Forbidden` on TestPyPI
Common causes:

- Wrong site/token: a token created on **PyPI** (pypi.org) does not work on **TestPyPI** (test.pypi.org). Create an account + token on https://test.pypi.org/.
- Token scope: use an account-wide token for the first upload. Project-scoped tokens only work for projects you already own.
- Package name already owned by someone else on TestPyPI/PyPI. In that case, change `[project].name` in `pyproject.toml` to a unique name and rebuild.

To get a more explicit error message:

```bash
python -m twine upload --repository testpypi --verbose dist/*
```
