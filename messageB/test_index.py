# -*- coding：utf-8 -*-
from selenium import webdriver
import unittest
import requests


class MITest(unittest.TestCase):
    """博客主页"""
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.index_url = r"http://127.0.0.1:8000/"
        self.driver.get(self.index_url)
        self.driver.implicitly_wait(30)

    def test_Index(self):
        """测试留言板登录"""
        r1 = requests.get(self.index_url)
        code = r1.status_code
        self.assertEqual(code,200)


    def test_01(self):
        """在主页，点击登录，可进入登录页面"""
        self.driver.find_element_by_xpath(".//*[@value='登录']").click()
        text = self.driver.find_element_by_xpath("/html/body/h1").text
        self.assertEqual(text,"登录页面")

    def test_02(self):
        """在主页，点击登录，可进入注册页面"""
        self.driver.find_element_by_xpath(".//*[@value='注册']").click()
        text = self.driver.find_element_by_xpath("/html/body/h1").text
        self.assertEqual(text,"注册页面")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
        unittest.main()