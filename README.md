# Django clean architecture

Example REST web service for internet library with:

- clean architecture with interfaces, layers and entities
- Dependency Injection with [dishka](https://github.com/reagento/dishka)
- auto tests with [pytest](https://docs.pytest.org/en/stable/)
- formatting and linting with [ruff](https://github.com/astral-sh/ruff) and [mypy](https://github.com/python/mypy)
- Dockerfile with best practices
- CI/CD with Github Workflows with separated actions
- [pre-commit](https://github.com/pre-commit/pre-commit) features

## Working with repos

### How to install dependencies?

Creating new venv in project folder and install all dependencies with poetry:

```bash
make develop
```

### How to run dev containers for testing?

Start postgres container described in `docker-compose.dev.yaml` from scratch:

```bash
make local
```

### How to run tests?

The tests must be run after the dependencies are installed and when the `make local` process is running separately:

```bash
pytest -vx ./tests
```
