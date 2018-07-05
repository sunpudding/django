# -*- coding：utf-8 -*-
from selenium import webdriver
import unittest
import requests
import random
import string
x =''.join(random.sample(string.ascii_letters+string.digits, 10))
y = ''.join(random.sample(string.digits,5))
data = [{"registname": x, "registpsw":y}]


class MOutTest(unittest.TestCase):
    """博客修改密码主页"""
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.changepwd_url = r"http://127.0.0.1:8000/changepwd/"
        self.register_url = r"http://127.0.0.1:8000/regist/"
        self.login_url = r"http://127.0.0.1:8000/login/"
        self.driver.get(self.changepwd_url)
        self.driver.implicitly_wait(30)

    def newAccount(self):
        """新注册一个账户，修改用户密码"""
        self.driver.get(self.register_url)
        self.driver.find_element_by_xpath("//*[@name='username']").send_keys(data[0]['registname'])
        self.driver.find_element_by_xpath("//*[@name='password']").send_keys(data[0]['registpsw'])
        self.driver.find_element_by_xpath("//*[@value='Regist']").click()
        self.driver.find_element_by_xpath("/html/body/a").click()
        self.driver.get(self.changepwd_url)
        self.driver.find_element_by_xpath("//*[@name='username']").send_keys(data[0]['registname'])
        self.driver.find_element_by_xpath("//*[@name='old_password']").send_keys(data[0]['registpsw'])
        self.driver.find_element_by_xpath("//*[@name='new_password']").send_keys('123456')
        self.driver.find_element_by_xpath("//*[@value='修改密码']").click()


    def test_changepwd(self):
        """测试修改密码首页"""
        r1 = requests.get(self.changepwd_url)
        code = r1.status_code
        self.assertEqual(code,200)

    def test_01(self):
        """用户修改密码提交后，返回密码修改成功页面"""
        self.newAccount()
        pageResult = self.driver.find_element_by_xpath("/html/body").text
        self.assertEqual("密码修改成功!",pageResult)

    def test_02(self):
        """用户使用修改密码后的账户信息进行登录"""
        self.newAccount()
        self.driver.get(self.login_url)
        self.driver.find_element_by_id("id_username").send_keys(data[0]['registname'])
        self.driver.find_element_by_id("id_password").send_keys("123456")
        self.driver.find_element_by_xpath("/html/body/form/input[2]").click()
        text = self.driver.find_element_by_id("users").text
        self.assertEqual(text,data[0]['registname'])



    def tearDown(self):
            self.driver.quit()

if __name__ == "__main__":
        unittest.main()