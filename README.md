# Micro Auth Service

A micro auth-service which could be used in a microservices architecture.

## Installation

```
pyenv install 3.10.8
pyenv virtualenv 3.10.8 auth-service
pyenv local auth-service
pip install -U pip
pip install -r requirements.txt
```

## Unit Tests

```
pytest
```

## Integration Tests

```
docker compose up
pytest integration_tests
```
