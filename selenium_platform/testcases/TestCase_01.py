import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from TestCasesClass import Step
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


class TestCase(unittest.TestCase):

    def setUp(self):
        """Start web driver"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            options=chrome_options
        )
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.driver.get('https://www.w3schools.com')
        self.screenshot_root_dir = r'screenshots/'

    def tearDown(self):
        """Stop web driver"""
        self.driver.quit()


    def test_case_1(self):
        """Check search"""
        screenshot_dir = self.screenshot_root_dir + 'test_case_1/'
        step_delay = 0
        try:
            step1 = Step('1. Click accept choices', self.driver, 'accept-choices', By.ID, delay=step_delay, action='click',
                         showHint=True, screenshotPath=screenshot_dir)
            print(step1.returnStepName())
            step1.returnElement()

            step2 = Step('2. Click tutorials', self.driver, '//*[@id="navbtn_tutorials"]', By.XPATH, delay=step_delay,
                         action='click', showHint=True, screenshotPath=screenshot_dir)
            print(step2.returnStepName())
            step2.returnElement()

            step3 = Step('3. Click Learn HTML', self.driver, '//*[@id="nav_tutorials"]/div/div/div[2]/a[1]', By.XPATH,
                         delay=step_delay, action='click',
                         showHint=True, screenshotPath=screenshot_dir)
            print(step3.returnStepName())
            step3.returnElement()

            step4 = Step('4. Click Next', self.driver, 'Next ❯', By.LINK_TEXT, delay=step_delay, action='click',
                         showHint=True, screenshotPath=screenshot_dir)
            print(step4.returnStepName())
            step4.returnElement()

            step5 = Step('5. Click Search', self.driver, '//*[@id="topnav"]/div/div[1]/a[23]', By.XPATH, delay=step_delay,
                         action='click',
                         showHint=True, screenshotPath=screenshot_dir)
            print(step5.returnStepName())
            step5.returnElement()

            step6 = Step('6. Type python', self.driver, '//*[@id="gsc-i-id1"]', By.XPATH, delay=step_delay, action='send_keys',
                         actionValue='python',
                         showHint=True, screenshotPath=screenshot_dir)
            print(step6.returnStepName())
            step6.returnElement()

            step7 = Step('7. Click Search', self.driver,
                         '//*[@id="___gcse_0"]/div/div/form/table/tbody/tr/td[2]/button',
                         By.XPATH, delay=step_delay, action='click', showHint=True, screenshotPath=screenshot_dir)
            print(step7.returnStepName())
            step7.returnElement()
            step8 = Step('8. Click 1st Element', self.driver,
                         '//*[@id="___gcse_0"]/div/div/div[1]/div[6]/div[2]/div/div/div[1]/div[1]/div[1]/div[1]/div/a',
                         By.XPATH, delay=step_delay, action='click', showHint=True, screenshotPath=screenshot_dir)
            print(step8.returnStepName())
            step8.returnElement()

        except NoSuchElementException as ex:
            self.fail(ex.msg)

    def test_case_2(self):
        """Buy 3 cert C# exams"""
        screenshot_dir = self.screenshot_root_dir + 'test_case_2/'
        step_delay = 0
        try:
            step1 = Step('1. Click accept choices', self.driver, 'accept-choices', By.ID, delay=step_delay, action='click',
                         showHint=True, screenshotPath=screenshot_dir)
            print(step1.returnStepName())
            step1.returnElement()

            step2 = Step('2. Type c#', self.driver, 'search2', By.ID, delay=step_delay, action='send_keys', actionValue='c#',
                         showHint=True, screenshotPath=screenshot_dir)
            print(step2.returnStepName())
            step2.returnElement()

            step3 = Step('3. Press down arrow', self.driver, 'search2', By.ID, delay=step_delay, action='send_keys',
                         actionValue=Keys.DOWN, showHint=True, screenshotPath=screenshot_dir)
            print(step3.returnStepName())
            step3.returnElement()

            step4 = Step('4. Press enter', self.driver, 'learntocode_searchbtn', By.ID, delay=step_delay,
                         action='send_keys', actionValue=Keys.ENTER, showHint=True, screenshotPath=screenshot_dir)
            print(step4.returnStepName())
            step4.returnElement()

            step5 = Step('5. Select option 3 from quantity', self.driver, 'product-quantity-select', By.ID, delay=step_delay,
                         action='select_by_visible_text', actionValue='3',
                         showHint=True, screenshotPath=screenshot_dir)
            print(step5.returnStepName())
            step5.returnElement()

            step6 = Step('6. Click add to cart', self.driver, '//*[@id="product_form_6807031644217"]/div[1]/button', By.XPATH, delay=step_delay,
                         action='click', showHint=True, screenshotPath=screenshot_dir)
            print(step6.returnStepName())
            step6.returnElement()

            step7 = Step('7. Click check out', self.driver, '//*[@id="shopify-section-template--15415043850297__main"]/form/header/div[2]/button', By.XPATH, delay=step_delay,
                         action='click', showHint=True, screenshotPath=screenshot_dir)
            print(step7.returnStepName())
            step7.returnElement()

        except NoSuchElementException as ex:
            self.fail(ex.msg)

