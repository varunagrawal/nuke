# Just run the tests on `make`
main:
	tox

# Submit the package. Make sure your ~/.pypirc file is set correctly
submit:
	nuke -y dist/
	python3 -m build  # package
	twine upload dist/*  # upload
