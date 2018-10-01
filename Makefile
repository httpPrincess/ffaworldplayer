.PHONY: clean data lint

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = isat
PYTHON_INTERPRETER = python3

#################################################################################
# COMMANDS                                                                      #
#################################################################################

data/raw/votes2018.pdf:
	wget -O $@ https://img.fifa.com/image/upload/ag30shazs0wdowcyettg.pdf?_branch_match_id=459377745713818745

data/raw/votes2017.pdf:
	wget -O $@ https://resources.fifa.com/mm/document/the-best/playeroftheyear-men/02/91/68/49/faward_menplayer2017_neutral.pdf

data/raw/regions.csv:
	wget -O $@ https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv

data/processed/votes2018.txt : data/raw/votes2018.pdf
	pdftotext $< $@

data/processed/votes2017.txt : data/raw/votes2017.pdf
	pdftotext $< $@

data/processed/votes2018.csv: data/processed/votes2018.txt data/raw/regions.csv
	$(PYTHON_INTERPRETER) src/data/processtext.py $< $@

data/processed/votes2017.csv: data/processed/votes2017.txt data/raw/regions.csv
	$(PYTHON_INTERPRETER) src/data/processtext.py $< $@


## Make Dataset
alldata: data/processed/votes2018.csv data/processed/votes2017.csv

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8
lint:
	flake8 src

