# Contributing


Install [uv](https://docs.astral.sh/uv/getting-started/installation/)

1. and...


        git clone https://github.com/pytest-dev/pytest-echo
        cd pytest-echo
        uv venv .venv --python 3.12
        source .venv/bin/activate
        uv sync --all-groups
        pre-commit install --hook-type pre-commit --hook-type pre-push
