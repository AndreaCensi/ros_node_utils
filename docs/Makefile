# v. 1.5
github_repo=git@github.com:AndreaCensi/ros_node_utils.git
# also change this in epydoc.cfg
webdir=website
webgit=git --git-dir $(webdir)/.git --work-tree=$(webdir)/ 

all: compile-website 

	
compile-website: website epydoc
	PYTHONPATH=`pwd`:$(PYTHONPATH) sphinx-build -E -n -a -b html source website

compile:
	PYTHONPATH=`pwd`:$(PYTHONPATH) sphinx-build -n -a -b html source website
	
website: distclean
	# Check out the website
	git clone $(github_repo) $@
	$(webgit) checkout origin/gh-pages -b gh-pages
	$(webgit) branch -D master

upload:
	$(webgit) commit -m "updated website" -a 
	$(webgit) push

distclean:
	rm -rf $(webdir)/
	
epydoc:
	epydoc --config epydoc.cfg --introspect-only -v --exclude-introspect=MAIN_PACKAGE.unittests --debug
 