# Australian Federal Election 2022

The AEC produce a data file which lists, for each 2016 SA1, how many votes were cast at each polling place, and how many votes by other methods e.g absentee votes.

This code processes that file to produce an estimate for primary, two-party, and two-candidate results by SA1.

## Getting Started

- Requires a python 3 environment, e.g through WSL on windows, or anaconda, etc.
- Requires pipenv
On ubuntu 22.04 you could start with:
```sh
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python-is-python3
sudo apt-get install pip
pip install pipenv
```
To configure this project, clone the repo, and then:
```sh
pipenv install
``` 
To create the virutal python env with the necessary packages.

## Running
the "get" file will get all the data
the "clean" file will structure it and produce our output
```sh
pipenv run python get.py
pipenv run python clean.py
```

