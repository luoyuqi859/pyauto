# pyauto框架介绍

本框架主要是基于 Python + pytest + pytest相关插件+ allure + loguru + yaml + uiautomator2 + weditor + 飞书通知 +
实现的UI自动化框架

## 框架功能

* 测试用例失败重测 '--reruns=1', '--reruns-delay=2'
* 测试用例重复执行 "--count=1"
* 测试用例执行完毕收集花费时间最长的10条用例
* 测试用例随机执行
* 日志模块: 打印执行中每个步骤
* 飞书通知
* excel表格收集测试失败用例
* allure报告失败截图
* weditor辅助元素信息查找

## 目录结构
    ├── conf                         // 配置相关目录
    ├── libs                         // 依赖库，需要本地化后续维护修改
    ├── repos                        // 脚本仓库，存放各个测试脚本
    ├── uiauto                       // ui自动化相关封装
    ├── utils                        // 工具库
    ├── run.py                       // 运行入口  

## 安装教程

* 首先，执行本框架之前，需要搭建好 python、python版本:3.9.6
* 进入libs/uiautomator2目录下，点击install.bat，安装uiautomator2相关依赖
* 进入libs目录下执行 install.bat， 安装框架相关依赖
* 框架运行入口 run.py 

## 问题
* 如何对比两个文字的字体大小  333200