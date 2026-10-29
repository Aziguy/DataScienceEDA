.PHONY: install lint format test train site serve app docker clean

PORT ?= 8000

install:
	pip install -e ".[dev,app]"
	pre-commit install

lint:
	ruff check .
	ruff format --check .

format:
	ruff check --fix .
	ruff format .

test:
	pytest --cov

train:
	playstore-insights train

site:
	playstore-insights all

serve: site
	python -m http.server $(PORT) -d build/site

app:
	streamlit run app/streamlit_app.py

docker:
	docker build -t playstore-insights .
	docker run --rm -p 8501:8501 playstore-insights

clean:
	rm -rf build artifacts .pytest_cache .ruff_cache .coverage coverage.xml htmlcov
