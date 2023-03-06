#! /usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: faker
@Created: 2023/2/22 16:46
"""
import base64
import urllib.parse
from random import randint

from faker import Faker

fk = Faker(locale='zh_CN')


def random_mobile():
    """随机生成手机号"""
    return fk.phone_number()


def random_msisdn():
    return fk.msisdn()


def random_name():
    """随机生成中文名字"""
    return fk.name()


def random_ssn():
    """随机生成一个身份证号"""
    return fk.ssn()


def random_addr():
    """随机生成一个地址"""
    return fk.address()


def random_city():
    """随机生成一个城市名"""
    return fk.city()


def random_company():
    """随机生成一个公司名"""
    return fk.company()


def random_postcode():
    """随机生成一个邮编"""
    return fk.postcode()


def random_email():
    """随机生成一个邮箱号"""
    return fk.email()


def random_date():
    """随机生成一个日期"""
    return fk.date()


def radom_date_time():
    """随机生成一个时间"""
    return fk.date_time()


def random_ipv4():
    """随机生成一个ipv4的地址"""
    return fk.ipv4()


def random_job():
    """随机生成一个职业"""
    return fk.job()


def generate_random_num_str(length=20):
    """
    生成随机字母与数字混合字符串
    :param length:
    :return:
    """
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z']
    random_list = []
    for _ in range(length):
        random_list.append(randint(0, len(letters)) - 1)

    for i, v in enumerate(random_list):
        if i % 2 == 0:
            v %= 10
            random_list[i] = str(v)
            continue
        random_list[i] = letters[v]
    return ''.join(random_list)


def base64_encode(data: str):
    """base64编码"""
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')


def md5_encrypt(data: str):
    """md5加密"""
    from hashlib import md5
    new_md5 = md5()
    new_md5.update(data.encode('utf-8'))
    return new_md5.hexdigest()


def rsa_encrypt(msg, server_pub):
    """
    rsa加密
    :param msg: 待加密文本
    :param server_pub: 密钥
    :return:
    """
    import rsa

    msg = msg.encode('utf-8')
    pub_key = server_pub.encode("utf-8")
    public_key_obj = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key)
    cryto_msg = rsa.encrypt(msg, public_key_obj)  # 生成加密文本
    cipher_base64 = base64.b64encode(cryto_msg)  # 将加密文本转化为 base64 编码
    return cipher_base64.decode()


def get_url(url, type=True):
    """
    url转码
    type=True: %E6%88%91%E8%A6%81%E5%8F%8D%E9%A6%88 =》我要反馈
    type=False: 我要反馈 =》%E6%88%91%E8%A6%81%E5%8F%8D%E9%A6%88
    """
    if type:
        return urllib.parse.unquote(url)
    else:
        return urllib.parse.quote(url)
