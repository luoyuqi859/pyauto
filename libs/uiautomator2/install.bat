del /Q /S build
del /Q /S  dist
del /Q /S  own_uiautomator2.egg-info
python setup.py install
pip install -r requirements.txt
pause