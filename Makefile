test:
	pytest tests

clean:
	rm -fr dist build pytest_echo.egg-info .coverage ./~build

fullclean: clean
	rm -fr .tox .cache .pytest_cache
	find . -name '*.pyc' -exec rm -f {} +
