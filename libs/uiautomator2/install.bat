del /Q /S build
del /Q /S  dist
del /Q /S  own_uiautomator2.egg-info
python setup.py install
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
pause