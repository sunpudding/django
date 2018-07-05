# -*- coding：utf-8 -*-
from selenium import webdriver
import unittest
import requests


class MOutTest(unittest.TestCase):
    """测试注销功能"""
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.login_url = r"http://127.0.0.1:8000/login"
        self.logout_url = r"http://127.0.0.1:8000/logout/"
        self.driver.get(self.login_url)
        self.driver.implicitly_wait(30)

    def test_logout(self):
        """测试退出接口"""
        r1 = requests.get(self.logout_url)
        code = r1.status_code
        self.assertEqual(code,200)


    def test_01(self):
        """在登录页，点击注销，可注销"""
        self.driver.find_element_by_xpath(".//*[@value='注销']").click()
        text = self.driver.find_element_by_xpath(".//*[@id='logout']").text
        self.assertEqual(text,"已注销！")

    def test_02(self):
        """登录后，点击注销，可注销"""
        self.driver.find_element_by_id("id_username").send_keys("12")
        self.driver.find_element_by_id("id_password").send_keys("12")
        self.driver.find_element_by_xpath("/html/body/form/input[2]").click()
        self.driver.find_element_by_xpath(".//*[@value='注销']").click()
        text = self.driver.find_element_by_xpath(".//*[@id='logout']").text
        self.assertEqual(text,"已注销！")




    def tearDown(self):
            self.driver.quit()

if __name__ == "__main__":
        unittest.main()