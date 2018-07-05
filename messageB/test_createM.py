# -*- coding：utf-8 -*-
from selenium import webdriver
import unittest
#测试数据
testdata = [{"title": "demo title", "content": "demo content"},
            ]

class MCTest(unittest.TestCase):
    """博客建立留言"""

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.login_url = r"http://127.0.0.1:8000/login/"
        self.driver.get(self.login_url)
        # self.driver.implicitly_wait(30)

    def createM(self, title, content):
        """重新定义留言,标题和内容参数化"""
        self.driver.find_element_by_id("id_username").send_keys("12")
        self.driver.find_element_by_id("id_password").send_keys("12")
        self.driver.find_element_by_xpath("/html/body/form/input[2]").click()
        self.driver.find_element_by_xpath("//*[@value='去留言']").click()
        self.driver.find_element_by_xpath(
            "//*[@name='title']").send_keys(title)
        self.driver.find_element_by_xpath(
            "//*[@name='content']").send_keys(content)
        self.driver.find_element_by_xpath("//*[@value='留言']").click()


    def test_creatM(self):
        from datetime import datetime
        d = self.driver
        # append random content suffix string
        title, content = testdata[0]['title'], testdata[0]['content']
        #格式化输出字符串
        content += ' {}'.format(datetime.now())
        ncreateM = self.createM(title, content)
        mainH = d.window_handles[0]
        self.driver.find_element_by_xpath("//*[@value='查看我的留言']").click()
        for h in d.window_handles:
            if h != mainH:
                d.switch_to.window(h)
        # turn to last page
        pageNumber = d.find_element_by_xpath("//a[contains(text(), '[第')]").text
        import re
        # 匹配到留言页面的最后一页
        y = re.findall(r"(?<=/).*(?=页)", pageNumber)
        lastNumber = " ".join(y)
        lastPage= "http://127.0.0.1:8000/mes/?page" + "=%s" % lastNumber
        self.driver.get(lastPage)
        lastHref = None
        foundRecord = False  # set if new comment found
        # read all comments at current page
        tds = d.find_elements_by_xpath("//table/tbody/tr/td")
        self.assertEqual(len(tds) % 4, 0)
        # check if new comment on current page
        for i in range(len(tds) // 4):
            i_ctime, i_creator, i_title, i_content = tds[4 * i:4 * i + 4]
            # todo: check data
            if i_title.text == title and i_content.text == content:
                foundRecord = True
        self.assertTrue(foundRecord)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()