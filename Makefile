package=ros_node_utils

include pypackage.mk

upload:
	rm -f dist/*
	rm -rf src/*.egg-info
	python3 setup.py sdist
	twine upload dist/*

bump:
	bumpversion patch
	git push --tags
	git push --all
	
