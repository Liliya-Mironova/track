import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class PythonOrgSearch (unittest.TestCase):
    def setUp (self):
        self.driver = webdriver.Firefox(executable_path="/home/katze/Downloads/geckodriver")

    # Example:
    # def test_search_in_python_org(self):
    #     driver = self.driver
    #     driver.get("http://www.python.org")
    #     self.assertIn("Python", driver.title)
    #     elem = driver.find_element_by_name("q")
    #     elem.send_keys("pycon")
    #     assert "No results found." not in driver.page_source
    #     elem.send_keys(Keys.RETURN)

    def test_click_search (self):
        driver = self.driver
        driver.get("http://localhost:3000/chat1")
        elem = driver.find_element_by_class_name("MessageForm")
        assert elem is not None
        print (elem)
        elem.click();
        # assert "No results found." not in driver.page_source

    def tearDown (self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()


# python -m unittest tests/selenium_tests.py