# oc-p4-chess-tournament

![chess_manager](https://cdn.mos.cms.futurecdn.net/5myLF3pZ6LfCZwPe5Drgtd.jpg)
## Install ChessManager

### Clone this repository
```
git clone https://github.com/Lee-RoyMannier/oc-p4-chess-tournament.git
```

### Create and activate python virtualenv
```
python -m venv .venv
source .venv/bin/activate
```

### Install dependencies
```
pip install -r requirements.txt
```

##  Run ChessManager
Launch this command:
```
python3 main.py
```
Then follow the instructions of the program

## Flake8
### View report
The report  is available via  an html file
`flake-report/index.html`

### Generate new flake8 report
```
flake8 --format=html --htmldir=flake-report --ignore=E501
```