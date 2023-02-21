# Introduction 
Because uiautomator2 will automatically disconnect after being used in Android 12 for a long time, the test terminal will be disconnected. The root cause is that the old version of uiautomator apks is not compatible with Android 12. Therefore, I wrote uiautomator apks from, and using custom apks needs to modify uiautomator2, so I have this version

#Usage
###1. Remove previously installed older versions
```
pip uninstall uiautomator2
```

###2.Install new version
```
pip install -U hmd-uiautomator2
```
