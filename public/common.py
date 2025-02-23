# -*- coding: utf-8 -*-
# @File: common.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/2/1  16:11

import os, sys
import re
from typing import List
import time
import shutil

import requests
from hashlib import md5

from config.setting import IS_CLEAN_REPORT
from public.yaml_data import GetCaseYmal
from config.ptahconf import PRPORE_ALLURE_DIR, PRPORE_JSON_DIR, PRPORE_SCREEN_DIR
from public.logs import logger


def get_run_func_name():
    """
    获取运行函数名称
    :return:
    """
    try:
        raise Exception
    except:
        exc_info = sys.exc_info()
        traceObj = exc_info[2]
        frameObj = traceObj.tb_frame
        Upframe = frameObj.f_back
        return Upframe.f_code.co_name


def sleep(s: float):
    """
    休眠秒数
    :param s:
    :return:
    """
    time.sleep(s)
    logger.info('强制休眠{}'.format(s))


def str_re_int(string: str) -> list:
    """
    提取字符中的整数
    :param string: 字符串
    :return: list
    """
    findlist = re.findall(r'[1-9]+\.?[0-9]*', string)
    return findlist

def png_path(imgname):
    """
    返回img测试图片路径
    :param imgname: imgname 图片名称 默认png格式
    :return:
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    IMG_FILE = os.path.join(BASE_DIR, "database", "file", "img", f"{imgname}.png")
    return IMG_FILE


def clean_report(filepath: str) -> None:
    """
    清除测试报告文件
    :param filepath:  str  清除路径
    :return:
    """
    del_list = os.listdir(filepath)
    if del_list:
        for f in del_list:
            file_path = os.path.join(filepath, f)

            # 判断是不是文件
            if os.path.isfile(file_path):
                if not file_path.endswith('.xml'):  # 不删除.xml文件
                    os.remove(file_path)
            else:
                os.path.isdir(file_path)
                shutil.rmtree(file_path)

def del_clean_report():
    """
    执行删除测试报告记录
    :return:
    """
    if IS_CLEAN_REPORT == True:  # 如果为 True 清除 PRPORE_ALLURE_DIR、 PRPORE_JSON_DIR 、PRPORE_SCREEN_DIR 路径下报告

        dir_list = [PRPORE_ALLURE_DIR, PRPORE_JSON_DIR, PRPORE_SCREEN_DIR]

        for dir in dir_list:
            clean_report(dir)

class ErrorExcep(Exception):
    """
    自定义异常类
    """

    def __init__(self, message):
        super().__init__(message)


class Get:
    """
    获取测试数据
    """

    @staticmethod
    def test_data(yamlname: str, casename: str) -> List:
        testdata = GetCaseYmal(yamlname, casename).test_data_values()
        return testdata



def imgContent(img_path, img_type=1902):
    """
    云打码验证码
    :param img_path: 图片路径
    :param img_type:  图片类型 默认 1902
    :return: str
    """
    '''
    https://www.chaojiying.com/price.html
    1902	常见4~6位英文数字(急速)	
    1101	1位英文数字	
    1004	1~4位英文数字	
    1005	1~5位英文数字	
    1006	1~6位英文数字	
    1007	1~7位英文数字	
    1008	1~8位英文数字	
    1009	1~9位英文数字	
    1010	1~10位英文数字	
    1012	1~12位英文数字	
    1020	1~20位英文数字	
    '''
    IMG_INFO = {'username': 'redaflifht', 'password': 'qar2000!', 'code_id': 909536,
                'api_url': 'http://upload.chaojiying.net/Upload/Processing.php'}

    rep = CjyClient(IMG_INFO.get('username'), IMG_INFO.get('password'), IMG_INFO.get('code_id'),
                    IMG_INFO.get('api_url'))

    with open(img_path, 'rb') as f:
        im = f.read()
        img_text = rep.postPic(im, img_type)

    return img_text.get('pic_str')


class CjyClient:

    def __init__(self, username, password, soft_id, apiurl):
        self.username = username
        password = password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.apiurl = apiurl
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id, }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def postPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post(self.apiurl, data=params, files=files,
                          headers=self.headers)
        return r.json()

# if __name__ == '__main__':
#     x=value_division(['all',1,1,'demo'])
#     print(x)