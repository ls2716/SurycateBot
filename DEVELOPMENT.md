# Development of the package

## Installation

To install the package in edit mode, you can use the following command:

```bash
pip install -e .
```

This will install the package in editable mode, so you can modify the code and
see the changes immediately.

Then, install the required packages:

```bash
pip install -r requirements.txt
```

Lastly, install the required nltk data within the python interpreter:

```python
import nltk
nltk.download('punkt_eng')
nltk.download('averaged_perceptron_tagger_eng')
```


## Testing

To run the tests, you can use the following command:

```bash
python -m pytest # [optional path to test file]
```

## Documentation

The documentation is based on file comments and on README.md file.

## Platform

The package requires pexpect, which is not available on Windows. The package
is not tested on Windows, and it is not guaranteed to work on Windows.
