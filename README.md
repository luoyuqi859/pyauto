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

## Ŀ¼�ṹ
    ������ conf                         // �������Ŀ¼
    ������ libs                         // �����⣬��Ҫ���ػ�����ά���޸�
    ������ repos                        // �ű��ֿ⣬��Ÿ������Խű�
    ������ uiauto                       // ui�Զ�����ط�װ
    ������ utils                        // ���߿�
    ������ run.py                       // �������  

## ��װ�̳�

* ���ȣ�ִ�б����֮ǰ����Ҫ��� python��python�汾:3.9.6
* ����libs/uiautomator2Ŀ¼�£����install.bat����װuiautomator2�������
* ����libsĿ¼��ִ�� install.bat�� ��װ����������
* ���������� run.py 

## ����
* �������⣬ȥatx_uninstall.py ж�أ���������

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