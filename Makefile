package=ros_node_utils

include pypackage.mk



bump-upload:
	bumpversion patch
	git push --tags
	git push --all
	rm -f dist/*
	rm -rf src/*.egg-info
	python setup.py sdist
	twine upload dist/*
