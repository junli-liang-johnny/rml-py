# RML Py

This is a Python implementation for RML with additional helpful features

# Build

```
pip install -U pyinstaller
pyinstaller main.py
```

# Run

```
./dist/main --config <path-to-config-file>
```

## This can be installed and used as a python module

```
from rml_py import convert

convert('<path-to-config-file-ttl>')
```
