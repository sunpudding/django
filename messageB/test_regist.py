# -*- coding:utf-8 -*-
from selenium import webdriver
import unittest
import requests
import ddt
import random
import string
#测试数据
x = "".join(random.sample(string.digits,8))
y = "".join(random.sample(string.ascii_letters,8))
all= "".join(map(chr, range(0x4e00, 0x9fa6)))
z = "".join(random.sample(all,4))
xy = "".join(random.sample(string.ascii_letters + string.digits,8))

test_data = [{"registname": x, "registpsw":x},
             {"registname": y, "registpsw": y},
             {"registname": z, "registpsw": z},
             {"registname": xy, "registpsw": xy},

             ]


@ddt.ddt
class MRTest(unittest.TestCase):
    """博客注册页面"""

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.regist_url = r"http://127.0.0.1:8000/regist/"
        self.driver.get(self.regist_url)
        self.driver.implicitly_wait(30)

    def test_Regist(self):
        """测试博客注册"""
        r1 = requests.get(self.regist_url)
        code = r1.status_code
        self.assertEqual(code, 200)

    @ddt.data(*test_data)
    def test_regist(self,data):
        """正常注册用户"""
        print("当前测试数据%s" % data)
        self.driver.find_element_by_xpath("//*[@name='username']").send_keys(data['registname'])
        self.driver.find_element_by_xpath("//*[@name='password']").send_keys(data['registpsw'])
        self.driver.find_element_by_xpath("//*[@value='Regist']").click()
        self.driver.find_element_by_xpath("/html/body/a").click()
        self.driver.find_element_by_id("id_username").send_keys(data['registname'])
        self.driver.find_element_by_id("id_password").send_keys(data['registpsw'])
        self.driver.find_element_by_xpath("/html/body/form/input[2]").click()
        text = self.driver.find_element_by_xpath("//*[@id='users']").text
        self.assertEqual(text,data['registname'])


    def test_01(self):
        """已注册的用户再次注册"""
        self.driver.find_element_by_xpath("//*[@name='username']").send_keys("12")
        self.driver.find_element_by_xpath("//*[@name='password']").send_keys("12")
        self.driver.find_element_by_xpath("//*[@value='Regist']").click()
        text = self.driver.find_element_by_id("fail").text
        self.assertEqual(text,"注册失败")


    def test_02(self):
        """注册失败的用户，在失败页面，点击注册按钮，可进入注册页面"""
        self.driver.find_element_by_xpath("//*[@name='username']").send_keys("12")
        self.driver.find_element_by_xpath("//*[@name='password']").send_keys("12")
        self.driver.find_element_by_xpath("//*[@value='Regist']").click()
        self.driver.find_element_by_xpath("/html/body/a").click()
        text = self.driver.find_element_by_xpath("/html/body/h1").text
        self.assertEqual(text,"注册页面")





    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

