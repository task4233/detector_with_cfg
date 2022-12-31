.PHONY: test
test:
	poetry run pytest .

.PHONY: run
run:
	poetry run python3 main.py
