# pyauto��ܽ���

�ƶ���Android UI�Զ������

## ��ܹ���

* ��������ʧ���ز�
* ���������ظ�ִ��
* �����������ִ��
* ��־ģ��: ��ӡִ����ÿ������
* ����֪ͨ: ���Խ�����֪ͨ����������
* excel����ռ�����ʧ������
* allure����չʾ, ��ʾ������Ϣ���������裬ʧ�ܽ�ͼ�����ܼ�ؽ�ͼ��ʧ�ܹ�����Ϣ
* weditor����Ԫ����Ϣ����
* ���Զ������ܼ��, memory,logcat,fps,cpu,thread_num
* ����minicap��sdk30,31,32��֧�֣��ӿ��ͼ�ٶ�
* ocr����ʶ��

## Ŀ¼�ṹ

    ������ conf                         // �������Ŀ¼
    ������ libs                         // �����⣬��Ҫ���ػ�����ά���޸�
    ������ report                       // ����ִ������������ݴ�ű���,���Զ����ɣ�������ɾ��
    ������ repos                        // �ű��ֿ⣬��Ÿ������Խű���ֻ�ܷ������Ŀ¼��
    ������ server                       // �������
    ������ uiauto                       // ui�Զ�����ط�װ
    ������ utils                        // ���߿�
    ������ run.py                       // �������  

## ��װ�̳�

* ���ȣ�ִ�б����֮ǰ����Ҫ��� python��python�汾:3.9.6
* ����libs/uiautomator2Ŀ¼�£����install.bat����װuiautomator2�������������uiautomator2,��Ҫʹ��pip install
  uiautomator2��
* ����libsĿ¼��ִ�� install.bat�� ��װ����������
* ���������� run.py

## ִ�з���

* �༭��ִ��,ͨ��pycharm�༭����run.py �Ҽ�������ִ�У����Զ�ִ��reposĿ¼�����в�������
* ������ִ��,��ǰĿ¼��CMD������ִ��python run.py�Զ�ִ������reposĿ¼�����в�������
* ��������ѡ��1, conf/config.yaml��pytestѡ�������Ҫ���Ե�·��
* ��������ѡ��2,python run.py --case ·��������·����������pytest������ python run.py --case D:
  \pyauto\repos\lxl\test_xxx.py::test_xxx,���ڶ��ִ��·����";"�ֿ�
* ����ִ�з�ʽ: ȥconf/config.yaml��ѡ����Ҫ�����Ĺ��ܺ���д����·��,ȥ��Ŀ¼��˫��run.batִ��

## �������Ҫ��

* ����uiautomator2����api
* ����pytest������÷�
* ����allure��ǲ���ȷ���
* ��עconf/config.yaml������ѡ�����

## ���⴦��

* �������⣬����atx_uninstall.py��Ȼ������ִ��

## api

```
�豸�����ʼ��
from uiauto.android.device import connect, AndroidDevice

conn = connect()
device = AndroidDevice(conn)
print(device.d.info)
```

```
adb����

device.adb_fp.adb.run_adb_cmd("shell am start -a com.gm.teenmode.app.LAUNCH")
device.adb_fp.adb.push()
device.adb_fp.adb.pull
```

```
ocr����ʶ��

device.ocr.image_to_text("xxx")
```

```
app

device.app(package=None, activity=None).get_info() ��ȡӦ����Ϣ
device.app(package=None, activity=None).start() Ӧ������
device.app(package=None, activity=None).stop() Ӧ��ֹͣ
device.app(package=None, activity=None).install() Ӧ������
device.app(package=None, activity=None).uninstall() Ӧ��ж��
device.app.current() ��ȡ��ǰӦ����Ϣ
device.app.list_running() �г����������е� app
```

```
page

device.page.source  ��ȡpagesource
device.page.find_element(x,y) ������ȡλ�� (x, y) �����Ԫ��
```

```
rotation

device.rotation.left ������ת����Ϊ��
device.rotation.right ������ת����Ϊ��
device.rotation.back ������ת����
```

```
swipe

device.swipe.down() ���»���
device.swipe.up() ���ϻ���
device.swipe.left() ���󻬶�
device.swipe.right() ���һ���
device.swipe.down().until_exists(text=xxx) ���»�����xxxԪ�س���
```

```
screenshot

device.screenshot.save('xxx.png')  ȫ����ͼ
device.screenshot.save_grid('xxx.png') ȫ����ͼЯ�����Ʊ��
device(text="xxx").screenshot("xxx.png") Ԫ�ؽ�ͼ
```

```
��Ļ�ߴ�

device.window_size 
device.is_multi_window_mode �Ƿ��ڷ���״̬
```

```
click

device.click(text=xxx)  Ԫ�ص��
device.click(resourceId=xxx) Ԫ�ص��
device.click(xpath=xxx) Ԫ�ص��
device.click(x,y) ������
```

```
press

device.press("home") ����HOME
device.press("back") ��������
```

```
element

device.get_element(text=xxx) ��ȡԪ��
device.get_element(xpath=xxx) ��ȡԪ��
device(text=xxx).info ��ȡԪ��info
device(text=xxx).text  ��ȡԪ��text
device(text=xxx).resource_id  ��ȡԪ��resource_id
device(text=xxx).bounds  ��ȡԪ��bounds
device(text=xxx).position  ��ȡԪ��position
device(text=xxx).class_name  ��ȡԪ��class_name
device(text=xxx).selectable  ��ȡԪ��selectable
device(text=xxx).selected  ��ȡԪ��selected
device(text=xxx).checked  ��ȡԪ��checked
device(text=xxx).checkable  ��ȡԪ��checkable
device(text=xxx).focused  ��ȡԪ��focused
device(text=xxx).focusable  ��ȡԪ��focusable
device(text=xxx).clickable  ��ȡԪ��clickable
device(text=xxx).long_clickable  ��ȡԪ��long_clickable
device(text=xxx).enabled  ��ȡԪ��enabled
device(text=xxx).count  ��ȡԪ��count
device(text=xxx).click()  Ԫ�ص��
```

```
assert

device.assert_exist(text=xxx) ����Ԫ�ش���
device.assert_exist(xpath=xxx) ����Ԫ�ش���
device.assert_not_exist(text=xxx) ����Ԫ�ز�����
device(text=xxx).assert_image(xxx.png, similarity=0.8) ����ͼƬ���ƶ�
assert device(text=xxx).enabled == True, "element enabled asser failed"
```

## �����������ʽ���

cpu

```shell
top
```

* device_cpu_rate������CPUʹ����
* user%���û�̬CPUʹ����
* system%���ں�̬CPUʹ����
* idle%������CPU
* pid_cpu%�����Զ�����̵�CPU
*

FPS��������)

```shell
dumpsys SurfaceFlinger �� dumpsys gfxinfo
```

* fps��֡��
* jank����֡������֡����10֡��һ�����ض�֡��
*

MEM���ڴ�)

```shell
adb shell dumpsys meminfo [pkg]
```

* total_ram���豸���ڴ�
* free_ram�������ڴ�
* pid_pss�����Զ�����̵��ڴ�
*

Power���ܺģ�����׼ȷ��

```shell
dumpsys batteryproperties

dumpsys battery
```

* voltage����ѹ
* tempreture���¶�
* current��������0��ʾû��ȡ����
*

PSS

```shell
adb shell dumpsys meminfo [pkg] ���������鿴ָ�����̰������ڴ�ʹ�����
```

* pss��ʵ��ʹ�õ������ڴ�
* java_heap��java�Ķ��ڴ�
* native_heap�������Ķ��ڴ�
* system
* android�����ڴ汻��Ϊ2���֣�native��dalvik��dalvik����java�ѣ���ͨjava��������java�ѷ��䣬��bitmap��ֱ����native�Ϸ��䣬�����ڴ��������
  native+dalvik ���ܳ����������
*

Thread Num���߳���)

*

Traffic����������)

```shell
��ȡ/proc/net/xt_qtaguid/stats
```

* device_total���豸������
* device_receive���豸����
* device_transport���豸����
* pid_rx����������
* pid_tx����������
* pid_total��������

  root
  ������ pytest_cmdline_main
  ������ pytest_plugin_registered
  ������ pytest_configure
  �� ������ pytest_plugin_registered
  ������ pytest_sessionstart
  �� ������ pytest_plugin_registered
  �� ������ pytest_report_header
  ������ pytest_collection
  �� ������ pytest_collectstart
  �� ������ pytest_make_collect_report
  �� �� ������ pytest_collect_file
  �� �� �� ������ pytest_pycollect_makemodule
  �� �� ������ pytest_pycollect_makeitem
  �� �� ������ pytest_generate_tests
  �� �� ������ pytest_make_parametrize_id
  �� ������ pytest_collectreport
  �� ������ pytest_itemcollected
  �� ������ pytest_collection_modifyitems
  �� ������ pytest_collection_finish
  �� ������ pytest_report_collectionfinish
  ������ pytest_runtestloop
  �� ������ pytest_runtest_protocol
  �� ������ pytest_runtest_logstart
  �� ������ pytest_runtest_setup
  �� �� ������ pytest_fixture_setup
  �� ������ pytest_runtest_makereport
  �� ������ pytest_runtest_logreport
  �� �� ������ pytest_report_teststatus
  �� ������ pytest_runtest_call
  �� �� ������ pytest_pyfunc_call
  �� ������ pytest_runtest_teardown
  �� �� ������ pytest_fixture_post_finalizer
  �� ������ pytest_runtest_logfinish
  ������ pytest_sessionfinish
  �� ������ pytest_terminal_summary
  ������ pytest_unconfigure

