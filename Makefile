# Just run the tests on `make`
main:
	tox

# Submit the package. Make sure your ~/.pypirc file is set correctly
submit:
	python3 setup.py sdist  # package
	twine upload dist/*  # upload
