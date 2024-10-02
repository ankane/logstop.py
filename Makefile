lint:
	pycodestyle . --ignore=E501

publish: clean
	python3 -m build
	ls dist
	twine upload dist/*
	make clean

clean:
	rm -rf .pytest_cache build dist src/logstop.egg-info
