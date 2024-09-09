# 页面元素
import time
import sys
from tkinter import messagebox
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class Element_Process:
    def __init__(self, web, logger, log_area, main_window):
        self.web = web
        self.logger = logger
        self.log_area = log_area
        self.main_window = main_window

    # 检查页面元素，含刷新
    def check_page_element(self,By, value, page, ec_condition, timeout=10, retries=5):
        current_retries = 0
        while current_retries < retries:
            try:
                check_page_element = WebDriverWait(self.web, timeout).until(ec_condition((By, value)))
                self.log_area.show_log_area(f"{page}页面{value}元素加载成功！")
                self.logger.info(f"{page}页面{value}元素加载成功！")
                return check_page_element
            except TimeoutException as e:
                current_retries += 1
                self.log_area.show_log_area(f"尝试了{current_retries}次，{page}页面{value}元素加载失败！")
                self.logger.warning(f"尝试了{current_retries}次，{page}页面{value}元素加载失败！错误信息：{e}")
                self.web.refresh()
                time.sleep(2)

        self.log_area.show_log_area(f"{page}页面元素{value}加载超时，请重启本软件！")
        self.logger.error(f"{page}页面元素{value}加载超时，请重启本软件！")
        msgBox = messagebox.showerror("网络超时", f"{page}页面元素{value}加载超时，请重启本软件！")
        self.web.quit()
        self.main_window.quit()
        sys.exit()

    def get_total_progress(self):
        total_progress = self.web.find_element(By.CSS_SELECTOR, ".progressbar-text").text
        return total_progress

    def get_current_url(self):
        current_url = self.web.current_url
        self.log_area.show_log_area(f"当前url：{current_url}")
        self.logger.info(f"当前url：{current_url}")
        return current_url

