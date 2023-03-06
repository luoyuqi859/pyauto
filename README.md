# pyauto��ܽ���

�������Ҫ�ǻ��� Python + pytest + pytest��ز��+ allure + loguru + yaml + uiautomator2 + weditor + ����֪ͨ +
ʵ�ֵ�UI�Զ������

## ��ܹ���

* ��������ʧ���ز� '--reruns=1', '--reruns-delay=2'
* ���������ظ�ִ�� "--count=1"
* ��������ִ������ռ�����ʱ�����10������
* �����������ִ��
* ��־ģ��: ��ӡִ����ÿ������
* ����֪ͨ
* excel����ռ�����ʧ������
* allure����ʧ�ܽ�ͼ
* weditor����Ԫ����Ϣ����
* ���Զ������ܼ��, memory,logcat,fps,cpu,thread_num
* ����minicap��sdk30,31,32��֧�֣��ӿ��ͼ�ٶ�

## Ŀ¼�ṹ

    ������ conf                         // �������Ŀ¼
    ������ libs                         // �����⣬��Ҫ���ػ�����ά���޸�
    ������ plugins                      // �����ز��
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
* ִ�з�ʽ1,ͨ��pycharm�༭����run.py �Ҽ�������ִ�У����Զ�ִ��reposĿ¼�����в�������
* ִ�з�ʽ2,��ǰĿ¼��CMD������ִ��python run.py�Զ�ִ������reposĿ¼�����в�������, ָ��Ŀ¼,python run.py --case
  ·��������·����������pytest������ python run.py --case D:\pyauto\repos\lxl\test_xxx.py::test_xxx,���ڶ��ִ��·����";"�ֿ�

## �������Ҫ��
* ����uiautomator2����api
* ����pytest
* ����allure��ǲ���ȷ���
* ��עconf/config.yaml������ѡ�����
* ִ������ǰ��ע��Ŀ¼��pytest.ini�ļ���conftest.py�ļ����˽�����ִ��λ�ã���ǣ������ǰ�ú�������

## ����
* �������⣬����atx_uninstall.py��Ȼ������ִ��


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
    ��   ������ pytest_plugin_registered
    ������ pytest_sessionstart
    ��   ������ pytest_plugin_registered
    ��   ������ pytest_report_header
    ������ pytest_collection
    ��   ������ pytest_collectstart
    ��   ������ pytest_make_collect_report
    ��   ��   ������ pytest_collect_file
    ��   ��   ��   ������ pytest_pycollect_makemodule
    ��   ��   ������ pytest_pycollect_makeitem
    ��   ��       ������ pytest_generate_tests
    ��   ��           ������ pytest_make_parametrize_id
    ��   ������ pytest_collectreport
    ��   ������ pytest_itemcollected
    ��   ������ pytest_collection_modifyitems
    ��   ������ pytest_collection_finish
    ��       ������ pytest_report_collectionfinish
    ������ pytest_runtestloop
    ��   ������ pytest_runtest_protocol
    ��       ������ pytest_runtest_logstart
    ��       ������ pytest_runtest_setup
    ��       ��   ������ pytest_fixture_setup
    ��       ������ pytest_runtest_makereport
    ��       ������ pytest_runtest_logreport
    ��       ��   ������ pytest_report_teststatus
    ��       ������ pytest_runtest_call
    ��       ��   ������ pytest_pyfunc_call
    ��       ������ pytest_runtest_teardown
    ��       ��   ������ pytest_fixture_post_finalizer
    ��       ������ pytest_runtest_logfinish
    ������ pytest_sessionfinish
    ��   ������ pytest_terminal_summary
    ������ pytest_unconfigure