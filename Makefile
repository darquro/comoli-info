.PHONY: setup run clean check-env test

# Python version
PYTHON := python3

# Check if .env file exists, if not create from example
check-env:
	@if [ ! -f .env ]; then \
		echo "Creating .env file..."; \
		echo "LINE_CHANNEL_ACCESS_TOKEN=" > .env; \
		echo "LINE_CHANNEL_SECRET=" >> .env; \
		echo "Please fill in the LINE credentials in .env file"; \
		exit 1; \
	fi

# Install dependencies
setup: check-env
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install wheel setuptools
	$(PYTHON) -m pip install -r requirements.txt

# Run the scraper
run: check-env
	$(PYTHON) scrape_comoli.py

# Run in test mode (skip content comparison and storage)
test: check-env
	$(PYTHON) scrape_comoli.py --test

# Clean up generated files
clean:
	rm -f previous_content.json
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete 