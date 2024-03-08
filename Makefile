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
	python3.11 run.py

setup: requirements.txt
	pip install -r requirements.txt

lint:
	pylint *.py