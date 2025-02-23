# -*- coding: utf-8 -*-
# @File: test_api.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/6/23  14:42

import os
import allure
import pytest

from public.logs import logger
from public.api_base import apiexe
from public.yaml_data import reda_data
from public.api_base import ApiBase
from config.setting import API_URL, HEADERS

yamlfile = os.path.basename(__file__).replace('py', 'yaml')  # 获取当前目运行文件



class TestApiDemo:
    """
    API  用例只需要 caseYAML文件
    """

    @allure.feature("接口demo")  # 测试用例特性（主要功能模块）
    @allure.story("接口测试")  # 模块说明
    @allure.title("get接口")  # 用例标题
    @allure.description('测试接口get方法')  # 用例描述
    @pytest.mark.parametrize('data', reda_data(yamlfile, 'test_api'))  # 测试数据传递
    @pytest.mark.test_api
    def test_api(self, data):
        with allure.step('登录接口'):
            ret = apiexe(yamlfile, 'test_api')
            assertion=data.get('assertion')
            assert assertion ==200



