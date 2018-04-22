build:
	python setup.py sdist bdist_wheel

clean:
	rm -fr dist build pytest_echo.egg-info .coverage ./~build

fullclean: clean
	rm -fr .tox .cache .pytest_cache
	find . -name '*.pyc' -exec rm -f {} +

release: build
	twine upload dist/*
	$(MAKE) fullclean
