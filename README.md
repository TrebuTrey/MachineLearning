# MachineLearning
Fundamental concepts of Machine Learning

## Repo Install Instructions

1. Identify a location on the hard drive (i.e. ~/Documents).
2. Clone the repository (creates a folder "MachineLearning" at the location of the clone)
```bash
git clone https://github.com/TrebuTrey/MachineLearning
```
3. Authenticate with GitHub user and password token.

## pyenv Install Instructions

1. Install `pyenv` for [Windows](https://github.com/pyenv/pyenv#windows) or [macOS](https://github.com/pyenv/pyenv#homebrew-in-macos).
2. Using `pyenv` install a version of Python 3.
```bash
pyenv install 3.9.13
```

## Python Virtual Environment Instructions

1. Activate the Python 3 version that was just installed
```bash
pyenv shell 3.9.13
```
2. Confirm the correct version of Python is active
```bash
python --version
```
3. Create the virtual environment
```bash
python -m venv .venv
```
4. Activate the virtual environment
```bash
# Windows
path/to/.venv/Scripts/Activate.ps1

# macOS
source path/to/.venv/bin/activate
```
5. Install dependencies
```bash
pip install -r path/to/requirements.txt
```

Start programming!
