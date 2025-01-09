from setuptools import setup , find_packages

setup(
	name        = "coa",
	version     = "0.1",
	py_modules  = find_packages(where="src"),
	package_dir = {"":"src"},
)
