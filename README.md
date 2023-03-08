# pyauto框架介绍

移动端Android UI自动化框架

## 框架功能

* 测试用例失败重测
* 测试用例重复执行
* 测试用例随机执行
* 日志模块: 打印执行中每个步骤
* 飞书通知: 测试结束后通知测试完成情况
* excel表格收集测试失败用例
* allure报告展示, 显示用例信息，用例步骤，失败截图，性能监控截图，失败过程信息
* weditor辅助元素信息查找
* 测试对象性能监控, memory,logcat,fps,cpu,thread_num
* 增加minicap对sdk30,31,32的支持，加快截图速度
* ocr文字识别

## 目录结构

    ├── conf                         // 配置相关目录
    ├── libs                         // 依赖库，需要本地化后续维护修改
    ├── report                       // 测试执行完毕所有数据存放报告,会自动生成，可随意删除
    ├── repos                        // 脚本仓库，存放各个测试脚本，只能放在这个目录下
    ├── server                       // 服务相关
    ├── uiauto                       // ui自动化相关封装
    ├── utils                        // 工具库
    ├── run.py                       // 运行入口  

## 安装教程

* 首先，执行本框架之前，需要搭建好 python、python版本:3.9.6
* 进入libs/uiautomator2目录下，点击install.bat，安装uiautomator2相关依赖（本地uiautomator2,不要使用pip install
  uiautomator2）
* 进入libs目录下执行 install.bat， 安装框架相关依赖
* 框架运行入口 run.py

## 执行方法

* 编辑器执行,通过pycharm编辑器在run.py 右键绿三角执行，会自动执行repos目录下所有测试用例
* 命令行执行,当前目录下CMD命令行执行python run.py自动执行所有repos目录下所有测试用例
* 测试区域选择1, conf/config.yaml中pytest选项添加想要测试的路径
* 测试区域选择2,python run.py --case 路径用例，路径用例依据pytest规则，如 python run.py --case D:
  \pyauto\repos\lxl\test_xxx.py::test_xxx,存在多个执行路径用";"分开
* 建议执行方式: 去conf/config.yaml中选择想要开启的功能和填写测试路径,去根目录下双击run.bat执行

## 框架掌握要点

* 掌握uiautomator2常用api
* 掌握pytest等相关用法
* 掌握allure标记步骤等方法
* 关注conf/config.yaml中配置选项参数

## 问题处理

* 出现问题，运行atx_uninstall.py，然后重新执行

## api

```
设备对象初始化
from uiauto.android.device import connect, AndroidDevice

conn = connect()
device = AndroidDevice(conn)
print(device.d.info)
```

```
adb命令

device.adb_fp.adb.run_adb_cmd("shell am start -a com.gm.teenmode.app.LAUNCH")
device.adb_fp.adb.push()
device.adb_fp.adb.pull
```

```
ocr文字识别

device.ocr.image_to_text("xxx")
```

```
app

device.app(package=None, activity=None).get_info() 获取应用信息
device.app(package=None, activity=None).start() 应用启动
device.app(package=None, activity=None).stop() 应用停止
device.app(package=None, activity=None).install() 应用下载
device.app(package=None, activity=None).uninstall() 应用卸载
device.app.current() 获取当前应用信息
device.app.list_running() 列出所有运行中的 app
```

```
page

device.page.source  获取pagesource
device.page.find_element(x,y) 解析获取位于 (x, y) 坐标的元素
```

```
rotation

device.rotation.left 设置旋转方向为左
device.rotation.right 设置旋转方向为右
device.rotation.back 返回旋转方向
```

```
swipe

device.swipe.down() 向下滑动
device.swipe.up() 向上滑动
device.swipe.left() 向左滑动
device.swipe.right() 向右滑动
device.swipe.down().until_exists(text=xxx) 向下滑动到xxx元素出现
```

```
screenshot

device.screenshot.save('xxx.png')  全屏截图
device.screenshot.save_grid('xxx.png') 全屏截图携带绘制表格
device(text="xxx").screenshot("xxx.png") 元素截图
```

```
屏幕尺寸

device.window_size 
device.is_multi_window_mode 是否处于分屏状态
```

```
click

device.click(text=xxx)  元素点击
device.click(resourceId=xxx) 元素点击
device.click(xpath=xxx) 元素点击
device.click(x,y) 坐标点击
```

```
press

device.press("home") 按键HOME
device.press("back") 按键返回
```

```
element

device.get_element(text=xxx) 获取元素
device.get_element(xpath=xxx) 获取元素
device(text=xxx).info 获取元素info
device(text=xxx).text  获取元素text
device(text=xxx).resource_id  获取元素resource_id
device(text=xxx).bounds  获取元素bounds
device(text=xxx).position  获取元素position
device(text=xxx).class_name  获取元素class_name
device(text=xxx).selectable  获取元素selectable
device(text=xxx).selected  获取元素selected
device(text=xxx).checked  获取元素checked
device(text=xxx).checkable  获取元素checkable
device(text=xxx).focused  获取元素focused
device(text=xxx).focusable  获取元素focusable
device(text=xxx).clickable  获取元素clickable
device(text=xxx).long_clickable  获取元素long_clickable
device(text=xxx).enabled  获取元素enabled
device(text=xxx).count  获取元素count
device(text=xxx).click()  元素点击
```

```
assert

device.assert_exist(text=xxx) 断言元素存在
device.assert_exist(xpath=xxx) 断言元素存在
device.assert_not_exist(text=xxx) 断言元素不存在
device(text=xxx).assert_image(xxx.png, similarity=0.8) 断言图片相似度
assert device(text=xxx).enabled == True, "element enabled asser failed"
```

## 性能数据名词解析

cpu

```shell
top
```

* device_cpu_rate：整机CPU使用率
* user%：用户态CPU使用率
* system%：内核态CPU使用率
* idle%：空闲CPU
* pid_cpu%：测试对象进程的CPU
*

FPS（流畅度)

```shell
dumpsys SurfaceFlinger 或 dumpsys gfxinfo
```

* fps：帧数
* jank：丢帧数，掉帧（丢10帧算一次严重丢帧）
*

MEM（内存)

```shell
adb shell dumpsys meminfo [pkg]
```

* total_ram：设备总内存
* free_ram：可用内存
* pid_pss：测试对象进程的内存
*

Power（能耗）（不准确）

```shell
dumpsys batteryproperties

dumpsys battery
```

* voltage：电压
* tempreture：温度
* current：电流（0表示没获取到）
*

PSS

```shell
adb shell dumpsys meminfo [pkg] 可以用来查看指定进程包名的内存使用情况
```

* pss：实际使用的物理内存
* java_heap：java的堆内存
* native_heap：其他的堆内存
* system
* android程序内存被分为2部分：native和dalvik，dalvik就是java堆，普通java对象是在java堆分配，而bitmap是直接在native上分配，对于内存的限制是
  native+dalvik 不能超过最大限制
*

Thread Num（线程数)

*

Traffic（网络流量)

```shell
读取/proc/net/xt_qtaguid/stats
```

* device_total：设备总流量
* device_receive：设备接收
* device_transport：设备传输
* pid_rx：上行流量
* pid_tx：下行流量
* pid_total：总流量

  root
  └── pytest_cmdline_main
  ├── pytest_plugin_registered
  ├── pytest_configure
  │ └── pytest_plugin_registered
  ├── pytest_sessionstart
  │ ├── pytest_plugin_registered
  │ └── pytest_report_header
  ├── pytest_collection
  │ ├── pytest_collectstart
  │ ├── pytest_make_collect_report
  │ │ ├── pytest_collect_file
  │ │ │ └── pytest_pycollect_makemodule
  │ │ └── pytest_pycollect_makeitem
  │ │ └── pytest_generate_tests
  │ │ └── pytest_make_parametrize_id
  │ ├── pytest_collectreport
  │ ├── pytest_itemcollected
  │ ├── pytest_collection_modifyitems
  │ └── pytest_collection_finish
  │ └── pytest_report_collectionfinish
  ├── pytest_runtestloop
  │ └── pytest_runtest_protocol
  │ ├── pytest_runtest_logstart
  │ ├── pytest_runtest_setup
  │ │ └── pytest_fixture_setup
  │ ├── pytest_runtest_makereport
  │ ├── pytest_runtest_logreport
  │ │ └── pytest_report_teststatus
  │ ├── pytest_runtest_call
  │ │ └── pytest_pyfunc_call
  │ ├── pytest_runtest_teardown
  │ │ └── pytest_fixture_post_finalizer
  │ └── pytest_runtest_logfinish
  ├── pytest_sessionfinish
  │ └── pytest_terminal_summary
  └── pytest_unconfigure

