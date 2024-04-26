# Run unit tests
test:
    pytest

# Run tests with coverage
coverage:
    coverage run --source pvmetatools -m pytest
    coverage html
