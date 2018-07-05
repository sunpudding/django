# -*- coding:utf-8 -*-
import unittest
import HTMLTestRunner
def all_case():
# 待执行用例的目录
    case_dir = r"F:\django\test-django\MessageB"
    testcase = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(case_dir,pattern="test*.py",top_level_dir=None)
# discover 方法筛选出来的用例，循环添加到测试套件中
    for test_suite in discover:
        for test_case in test_suite:
        # 添加用例到 testcase
            testcase.addTests(test_case)
    print(testcase)
    return testcase
if __name__ == "__main__":
    # 返回实例
    report_path = r"F:\django\test-django\report\result.html"
    fp = open(report_path, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                           title=u'这是我的自动化测试报告',
                                           description=u'用例执行情况：')
    # run 所有用例
    runner.run(all_case())
    fp.close()