# Run unit tests
test:
    pytest

# Run tests with coverage
coverage:
    coverage run --source pvmetatools -m pytest
    coverage html

docker:
    docker build --target pvmetatools -t pvmetatools .

docker-test:
    docker build --target pvmetatools-tests -t pvmetatools-tests .
    docker run -v $PWD:/src pvmetatools-tests -c pytest
