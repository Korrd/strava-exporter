# Use the repo venv when it exists, otherwise fall back to PATH python3
PYTHON := $(if $(wildcard venv/bin/python3),venv/bin/python3,python3)
PIP := $(if $(wildcard venv/bin/pip3),venv/bin/pip3,pip3)

build:
	pipreqs --force --mode compat

badge:
	python3 -m pybadges \
    --left-text="Python" \
    --right-text="3.10, 3.11, 3.12" \
    --whole-link="https://www.python.org/" \
    --browser \
    --logo='https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/python.svg'

clean:
	rm -rf __pycache__

run:
	$(PYTHON) run.py

setup: requirements.txt
	$(PIP) install -r requirements.txt

lint:
	pylint *.py