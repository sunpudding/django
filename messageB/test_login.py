# -*- coding:utf-8 -*-
from selenium import webdriver
import unittest
import requests
import time
import ddt
#测试数据{ "username":"","psw":""}
testData=[{"username":"12","psw":"12","expect_value":"True"},
          {"username":"12",  "psw":"",    "expect_value":"False"},
          {"username": "",   "psw": "12", "expect_value": "False"},
          {"username": "", "psw": "", "expect_value": "False"},
          ]




@ddt.ddt
class Bolg(unittest.TestCase):
    u'''登录博客'''
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.login_url = r"http://127.0.0.1:8000/login/"
        self.driver.get(self.login_url)
        self.driver.implicitly_wait(30)

    def login(self, username, psw):
        '''重新定义登录,账号和密码参数化'''
        self.driver.find_element_by_id("id_username").send_keys(username)
        self.driver.find_element_by_id("id_password").send_keys(psw)
        self.driver.find_element_by_xpath("/html/body/form/input[2]").click()
        time.sleep(3)
        try:
            text = self.driver.find_element_by_id("users").text
            print(text)
            return "True"
        except:
            return "False"



    def test_Login(self):
        """测试博客登录"""
        r1 = requests.get(self.login_url)
        code = r1.status_code
        self.assertEqual(code,200)

    @ddt.data(*testData)
    def test_login(self, data):
        u'''登录数据测试'''
        print ("当前测试数据%s"%data)
        # 调用登录方法
        result=self.login(data["username"], data["psw"])
        # 判断结果
        self.assertEqual(result,data["expect_value"], msg=result)

    def test_06(self):
        """验证登录成功后，点击注销，可退出应用"""
        self.driver.find_element_by_id("id_username").send_keys("12")
        self.driver.find_element_by_id("id_password").send_keys("12")
        time.sleep(1)
        self.driver.find_element_by_xpath("/html/body/form/input[2]").click()
        self.driver.find_element_by_xpath("/html/body/form/p/a/input").click()
        text = self.driver.find_element_by_id("logout").text
        self.assertEqual(text,"已注销！")

    def test_07(self):
        """验证在登录页面可以注销该应用"""
        self.driver.find_element_by_xpath("//*[@value='注销']").click()
        text = self.driver.find_element_by_id("logout").text
        self.assertEqual(text, "已注销！")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()