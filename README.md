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
* 测试对象性能监控, memory,logcat,fps,cpu,thread_num
* 增加minicap对sdk30,31,32的支持，加快截图速度

## 目录结构

    ├── conf                         // 配置相关目录
    ├── libs                         // 依赖库，需要本地化后续维护修改
    ├── plugins                      // 框架相关插件
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
* 执行方式1,通过pycharm编辑器在run.py 右键绿三角执行，会自动执行repos目录下所有测试用例
* 执行方式2,当前目录下CMD命令行执行python run.py自动执行所有repos目录下所有测试用例, 指定目录,python run.py --case
  路径用例，路径用例依据pytest规则，如 python run.py --case D:\pyauto\repos\lxl\test_xxx.py::test_xxx,存在多个执行路径用";"分开

## 框架掌握要点
* 掌握uiautomator2常用api
* 掌握pytest
* 掌握allure标记步骤等方法
* 关注conf/config.yaml中配置选项参数
* 执行用例前关注根目录下pytest.ini文件，conftest.py文件，了解用例执行位置，标记，和相关前置后置条件

## 问题
* 出现问题，运行atx_uninstall.py，然后重新执行


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
    │   └── pytest_plugin_registered
    ├── pytest_sessionstart
    │   ├── pytest_plugin_registered
    │   └── pytest_report_header
    ├── pytest_collection
    │   ├── pytest_collectstart
    │   ├── pytest_make_collect_report
    │   │   ├── pytest_collect_file
    │   │   │   └── pytest_pycollect_makemodule
    │   │   └── pytest_pycollect_makeitem
    │   │       └── pytest_generate_tests
    │   │           └── pytest_make_parametrize_id
    │   ├── pytest_collectreport
    │   ├── pytest_itemcollected
    │   ├── pytest_collection_modifyitems
    │   └── pytest_collection_finish
    │       └── pytest_report_collectionfinish
    ├── pytest_runtestloop
    │   └── pytest_runtest_protocol
    │       ├── pytest_runtest_logstart
    │       ├── pytest_runtest_setup
    │       │   └── pytest_fixture_setup
    │       ├── pytest_runtest_makereport
    │       ├── pytest_runtest_logreport
    │       │   └── pytest_report_teststatus
    │       ├── pytest_runtest_call
    │       │   └── pytest_pyfunc_call
    │       ├── pytest_runtest_teardown
    │       │   └── pytest_fixture_post_finalizer
    │       └── pytest_runtest_logfinish
    ├── pytest_sessionfinish
    │   └── pytest_terminal_summary
    └── pytest_unconfigure