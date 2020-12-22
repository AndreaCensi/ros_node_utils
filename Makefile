package=ros_node_utils

include pypackage.mk

upload:
	rm -f dist/*
	rm -rf src/*.egg-info
	python3 setup.py sdist
	devpi use $(TWINE_REPOSITORY_URL)
	devpi login $(TWINE_USERNAME) --password $(TWINE_PASSWORD)
	devpi upload --verbose dist/*
bump:
	bumpversion patch
	git push --tags
	git push --all
