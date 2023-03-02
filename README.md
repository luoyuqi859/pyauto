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
* 出现问题，去atx_uninstall.py 卸载，重新运行

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