set shell := ["powershell.exe", "-c"]
@a_default:
	just --list

@dev:
	uv run ./main.py

@lint:
	uv run ruff check --fix

@format:
	uv run ruff format