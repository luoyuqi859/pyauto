: pip install --upgrade setuptools wheel
: pip install --upgrade twine
del /Q /S build
del /Q /S  dist
del /Q /S  hmd_uiautomator2.egg-info

python setup.py sdist bdist_wheel
: python setup.py bdist_eggY
: python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
: pip uninstall hmd_uiautomator2
: pip install --upgrade hmd_uiautomator2
: gentliu
: 51Dadong02