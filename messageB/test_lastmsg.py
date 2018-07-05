# -*- coding：utf-8 -*-
from selenium import webdriver
import unittest
import requests
import random
import string
x =''.join(random.sample(string.ascii_letters+string.digits, 15))
y = ''.join(random.sample(string.digits,5))
data = [{"registname": x, "registpsw":y}]
testdata = [{"title": "demo title", "content": "demo content"},
            ]


class MLATest(unittest.TestCase):
    """最近十分钟留言模块"""
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.login_url = r"http://127.0.0.1:8000/login/"
        self.lastmsg_url = r"http://127.0.0.1:8000/latest_msg/"
        self.register_url = r"http://127.0.0.1:8000/regist/"
        self.driver.get(self.login_url)
        self.driver.implicitly_wait(30)


    def newAccount(self,title,content):
        """新注册一个账户，修改用户密码"""
        self.driver.get(self.register_url)
        self.driver.find_element_by_xpath("//*[@name='username']").send_keys(data[0]['registname'])
        self.driver.find_element_by_xpath("//*[@name='password']").send_keys(data[0]['registpsw'])
        self.driver.find_element_by_xpath("//*[@value='Regist']").click()
        self.driver.find_element_by_xpath("/html/body/a").click()
        self.driver.find_element_by_id("id_username").send_keys(data[0]['registname'])
        self.driver.find_element_by_id("id_password").send_keys(data[0]['registpsw'])
        self.driver.find_element_by_xpath("//*[@value='登录']").click()
        self.driver.find_element_by_xpath("//*[@value='去留言']").click()
        self.driver.find_element_by_xpath(
            "//*[@name='title']").send_keys(title)
        self.driver.find_element_by_xpath(
            "//*[@name='content']").send_keys(content)
        self.driver.find_element_by_xpath("//*[@value='留言']").click()

    def newMes(self):
        self.driver.get(self.login_url)
        title, content = testdata[0]['title'], testdata[0]['content']
        self.driver.find_element_by_id("id_username").send_keys(data[0]['registname'])
        self.driver.find_element_by_id("id_password").send_keys(data[0]['registpsw'])
        self.driver.find_element_by_xpath("//*[@value='登录']").click()
        self.driver.find_element_by_xpath("//*[@value='去留言']").click()
        self.driver.find_element_by_xpath(
            "//*[@name='title']").send_keys(title)
        self.driver.find_element_by_xpath(
            "//*[@name='content']").send_keys(content)
        self.driver.find_element_by_xpath("//*[@value='留言']").click()

    def test_01(self):
        """新创建一条留言，与最近十分钟的页面的发布时间进行比对"""
        d = self.driver
        title, content = testdata[0]['title'], testdata[0]['content']
        self.newAccount(title, content)
        self.driver.find_element_by_xpath("//*[@value='查看我的留言']").click()
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
        newMesTime = self.driver.find_element_by_xpath("/html/body/div/table/tbody/tr/td[1]").text
        self.driver.get(self.lastmsg_url)
        self.driver.find_element_by_xpath("//*[@id='table_last']/a").click()
        tds = d.find_elements_by_xpath("//table/tbody/tr/td")
        self.assertEqual(len(tds) % 4, 0)
        # check if new comment on current page
        foundRecord = False
        for i in range(len(tds) // 4):
            i_ctime, i_creator, i_title, i_content = tds[4 * i:4 * i + 4]
            # todo: check data
            if i_ctime.text != newMesTime:
                foundRecord = True
        self.assertTrue(foundRecord)

    def test_02(self):
        """新创建一条留言，与最近十分钟的页面的发布者进行比对"""
        self.newMes()
        d = self.driver
        self.driver.get(self.lastmsg_url)
        self.driver.find_element_by_xpath("//*[@id='table_last']/a").click()
        tds = d.find_elements_by_xpath("//table/tbody/tr/td")
        self.assertEqual(len(tds) % 4, 0)
        # check if new comment on current page
        foundRecord = False
        for i in range(len(tds) // 4):
            i_creator,i_title, i_content,i_ctime= tds[4 * i:4 * i + 4]
            # todo: check data
            if i_creator.text == data[0]["registname"]:
                foundRecord = True
        self.assertTrue(foundRecord)

    def test_03(self):
        """新创建一条留言，与最近十分钟的页面的标题进行比对"""
        self.newMes()
        d = self.driver
        self.driver.get(self.lastmsg_url)
        self.driver.find_element_by_xpath("//*[@id='table_last']/a").click()
        tds = d.find_elements_by_xpath("//table/tbody/tr/td")
        self.assertEqual(len(tds) % 4, 0)
        # check if new comment on current page
        foundRecord = False
        for i in range(len(tds) // 4):
            i_creator,i_title, i_content,i_ctime= tds[4 * i:4 * i + 4]
            # todo: check data
            if i_title.text ==testdata[0]['title'] :
                foundRecord = True
        self.assertTrue(foundRecord)


    def test_04(self):
        """新创建一条留言，与最近十分钟的页面的内容进行比对"""
        self.newMes()
        d = self.driver
        self.driver.get(self.lastmsg_url)
        self.driver.find_element_by_xpath("//*[@id='table_last']/a").click()
        tds = d.find_elements_by_xpath("//table/tbody/tr/td")
        self.assertEqual(len(tds) % 4, 0)
        # check if new comment on current page
        foundRecord = False
        for i in range(len(tds) // 4):
            i_creator,i_title, i_content,i_ctime= tds[4 * i:4 * i + 4]
            # todo: check data
            if i_content.text ==testdata[0]['content'] :
                foundRecord = True
        self.assertTrue(foundRecord)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
        unittest.main()