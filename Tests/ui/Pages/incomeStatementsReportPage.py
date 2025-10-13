from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import *


class IncomeStatementsReportPage:
    def __init__(self, driver, delay):
        self.driver = driver
        self.delay = delay

        self.power_bi_button = "//a[@role='tab' and text()='Power BI']"
        self.revenue_report_header = "//div[contains(@title, 'REVENUE')][1]"


        self.total_revenue_link = "//a[contains(text(), 'Total revenue')]"
        self.balance_sheets_tab = "//a[@aria-label='Balance Sheets']"


    def open_power_bi_report(self):
        try:
            power_bi_report_button = WDW(self.driver, self.delay).until(EC.element_to_be_clickable((By.XPATH,
                                                                                                    self.power_bi_button)))
            power_bi_report_button.click()
            return True
        except AssertionError:
            return False

    def switch_to_report_frame(self):
        iframe = self.driver.find_element(By.ID, "mschart")
        self.driver.switch_to.frame(iframe)

    def get_revenue_report_title(self):
        report_header = WDW(self.driver, self.delay).until(EC.element_to_be_clickable((By.XPATH,
                                                                                       self.revenue_report_header)))
        return report_header.get_attribute("title")

    def check_total_revenue_field_exists_and_clickable(self):

        total_revenue_element = WDW(self.driver, self.delay).until(
            EC.element_to_be_clickable((By.XPATH, self.total_revenue_link))
        )
        return total_revenue_element.is_displayed()

    def click_total_revenue_field(self):

        total_revenue_element = WDW(self.driver, self.delay).until(
            EC.element_to_be_clickable((By.XPATH, self.total_revenue_link))
        )
        total_revenue_element.click()

    def check_balance_sheets_button_exists(self):

        balance_sheets_element = WDW(self.driver, self.delay).until(
            EC.element_to_be_clickable((By.XPATH, self.balance_sheets_tab))
        )
        return balance_sheets_element.is_displayed()


    def click_balance_sheets_button(self):

        balance_sheets_element = WDW(self.driver, self.delay).until(
            EC.element_to_be_clickable((By.XPATH, self.balance_sheets_tab))
        )
        balance_sheets_element.click()

