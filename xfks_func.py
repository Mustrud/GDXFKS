# 首次进首页，各页面处理
import time
import sys
import random
from tkinter import messagebox
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from xfks_element import Element_Process

class Base_Func:
    def __init__(self, web, logger, log_area,main_window,start_mode):
        self.web = web
        self.logger = logger
        self.log_area = log_area
        self.main_window = main_window
        self.start_mode = start_mode
        self.element_process = None
        self.total_progress = None

    def frist_enter_index_page(self):
        self.web.refresh()
        self.log_area.show_log_area("进入首页！")
        self.logger.info("进入首页！")
        self.element_process = Element_Process(self.web, self.logger,self.log_area,self.main_window)
        self.element_process.check_page_element(By.CSS_SELECTOR, ".progressbar-text", "index",EC.presence_of_element_located)
        time.sleep(2)
        self.total_progress = self.element_process.get_total_progress()
        self.check_total_progress()

    # 检查总进度
    def check_total_progress(self):
        pages = Pages(self.web, self.logger, self.log_area, self.element_process, self.main_window,self.total_progress, self.start_mode)
        if self.total_progress == "100%":
            pages.index_page()
        else:
            self.log_area.show_log_area("进度不够100%，开始自动学习！")
            self.logger.info("进度不够100%，开始自动学习！")
            pages.index_page()

class Pages:
    def __init__(self, web, logger, log_area,element_process,main_window,total_progress, start_mode):
        self.web = web
        self.logger = logger
        self.log_area = log_area
        self.element_process = element_process
        self.main_window = main_window
        self.total_progress = total_progress
        self.start_mode = start_mode
        self.total_retries = 0
        self.max_quit_retries = 3
        self.li_elements = None
        self.score_element = None

    # 首页处理
    def index_page(self):
        self.element_process.get_current_url()
        # JavaScript设置元素显示
        self.web.execute_script("""
                            var elements = document.querySelectorAll("div.film_focus_imgs_wrap li");
                            for (var i = 0; i < elements.length; i++) {
                                if (elements[i].style.display === "none") {
                                    elements[i].style.display = "block";
                                }
                            }
                            """)
        self.logger.info('首页所有"course按钮"元素已设置为可见！')
        self.total_progress = self.element_process.get_total_progress()
        if self.total_progress == "100%":
            msgBox = messagebox.askyesno("提示", "100%进度可以考试了，还要继续学习剩余课程吗？")
            if msgBox:
                self.check_index_exist()
            else:
                self.log_area.show_log_area("脚本已停止！")
                self.logger.info("脚本已停止！")
                self.web.quit()
                self.main_window.quit()
                sys.exit()
        else:
            self.check_index_exist()

    # 判断全课程
    def check_index_exist(self):
        course_button = self.element_process.check_page_element(By.CSS_SELECTOR, ".film_focus_imgs_wrap li .card.current div a.btn", "index", EC.element_to_be_clickable)
        href_value = course_button.get_attribute("href")
        if href_value == "http://xfks-study.gdsf.gov.cn/study/course/12371":
            self.log_area.show_log_area("课程已全部完成，请仔细检查，及时参加考试！")
            self.logger.info("课程已全部完成，请仔细检查，及时参加考试！")
            msgBox = messagebox.showinfo("提示", "课程已全部完成，请仔细检查，及时参加考试！")
            self.web.quit()
            self.main_window.quit()
            sys.exit()
        else:
            self.button_click(course_button, self.course_page, "点击course_button按钮。")
            return

    # 按钮点击
    def button_click(self, button, action, message):
        button.click()
        self.log_area.show_log_area(message)
        self.logger.info(message)
        try:
            self.logger.info(f"{action}方法调用成功！")
            action()
        except Exception as e:
            self.log_area.show_log_area(f"{action}方法调用失败，即将返回首页！")
            self.logger.error(f"{action}方法调用成功，错误信息: {e}")
            self.return_index_page()

    # 返回首页
    def return_index_page(self):
        self.web.get("http://xfks-study.gdsf.gov.cn/study/index")
        self.element_process.check_page_element(By.CSS_SELECTOR, ".progressbar-text", "index", EC.presence_of_element_located)
        time.sleep(2)
        self.index_page()

    # 专题页处理
    def course_page(self):
        self.element_process.get_current_url()
        self.element_process.check_page_element(By.XPATH, "//ul[@class='chapter' and @chapter='0']", "course", EC.presence_of_element_located)
        self.li_elements = self.web.find_elements(By.XPATH, "//ul[@class='chapter' and @chapter='0']//li")
        for li in self.li_elements:
            title_elements = li.find_elements(By.XPATH, ".//td[@class='sub_title']")  # 无分值
            href_elements = li.find_elements(By.XPATH, ".//td[@class='title']//a")  # 有跳转链接
            if title_elements and href_elements and title_elements[0].text.strip() == "" and href_elements[0].get_attribute("href"):
                self.log_area.show_log_area(f'当前符合"无分值"且有"跳转链接"的元素为:{href_elements[0].text}')
                self.logger.info(f'当前符合"无分值"且有"跳转链接"的元素为:{href_elements[0].text}')
                self.button_click(li, self.select_mode_chapter_page, '点击"chapter_button"按钮。')
                return
        else:
            self.log_area.show_log_area("没有符合条件的元素，准备返回首页!")
            self.logger.info("没有符合条件的元素，准备返回首页!")
            self.return_index_page()

    def select_mode_chapter_page(self):
        if self.start_mode == 0:
            self.log_area.show_log_area("当前为普通模式。")
            self.logger.info("当前为普通模式。")
            self.chapter_page()
        else:
            self.log_area.show_log_area("当前为快速模式。")
            self.logger.info("当前为快速模式。")
            self.fast_chapter_page()

    # 章节页处理（正常模式），随机时间模拟点击
    def chapter_page(self):
        self.check_chapter_page_element()
        max_retries = 100
        retries = 0
        while retries < max_retries:
            try:
                self.score_element = self.web.find_element(By.CSS_SELECTOR,".chapter-score-wrap .chapter-score.chapter-score-suc")
                self.logger.info(f"chapter_page页面分数元素寻找了{retries+1}次，最大次数限制100次。")
                break
            except Exception as e:
                retries += 1
                time.sleep(1)
                if retries >= max_retries:
                    self.log_area.show_log_area("服务端可能出现问题，重新进入文章页。")
                    self.logger.error("元素查找超过100次，服务端可能出现问题，重新进入文章页。")
                    self.total_retries += 1
                    # 服务器异常处理，限制3次
                    if self.total_retries >= self.max_quit_retries:
                        self.log_area.show_log_area("服务端异常次数过多，脚本已停止！")
                        self.logger.error("服务端异常次数过多，最大次数限制3次，脚本已停止！")
                        msgBox = messagebox.showerror("错误", "服务端异常次数过多，脚本已停止，建议等待一段时间后再试！")
                        self.web.quit()
                        self.main_window.quit()
                        sys.exit()
                    self.web.refresh()
                    self.chapter_page()

        self.log_area.show_log_area("当前文章学习完成，即将进入下一篇。")
        self.logger.info("当前文章学习完成，即将进入下一篇。")
        try:
            next_chapter_button = self.web.find_element(By.CSS_SELECTOR, ".container a .next_chapter")
            random_second = random.randint(2, 6)
            time.sleep(random_second)
            self.log_area.show_log_area(f"已等待{random_second}秒。")
            self.logger.info(f"已等待{random_second}秒。")
            self.button_click(next_chapter_button, self.chapter_page, '点击"next_chapter_button"按钮。')
        except Exception as e:
            self.log_area.show_log_area("当前为最后一篇，即将返回专题页。")
            self.logger.info(f"当前为最后一篇，即将返回专题页。错误信息：{e}")
            return_course_button = self.web.find_element(By.CSS_SELECTOR, ".container.title.nav button")
            random_second = random.randint(2, 6)
            time.sleep(random_second)
            self.log_area.show_log_area(f"已等待{random_second}秒。")
            self.logger.info(f"已等待{random_second}秒。")
            self.button_click(return_course_button, self.course_page, '点击"return_course_button"按钮。')

    # 章节页处理（快速模式），直接通过JavaScript调用submitLearn()
    def fast_chapter_page(self):
        self.check_chapter_page_element()
        max_retries = 3
        retries = 0
        while retries < max_retries:
            try:
                random_second = random.randint(2, 5)
                time.sleep(random_second)
                self.log_area.show_log_area(f"已等待{random_second}秒。")
                self.logger.info(f"已等待{random_second}秒。")
                self.web.execute_script("submitLearn();")
                self.log_area.show_log_area("调用submitLearn成功，已更新元素。")
                self.logger.info("调用submitLearn成功，已更新元素。")
                self.log_area.show_log_area("当前文章学习完成，即将进入下一篇。")
                self.logger.info("当前文章学习完成，即将进入下一篇。")
                break
            except Exception as e:
                retries += 1
                self.log_area.show_log_area(f"调用submitLearn第{retries}次失败，即将重试。")
                self.logger.info(f"调用submitLearn第{retries}次失败，即将重试。错误信息：{e}")
                if retries >= max_retries:
                    self.total_retries += 1
                    if self.total_retries <= self.max_quit_retries:
                        self.log_area.show_log_area("服务端可能出错，重新进入文章页！")
                        self.logger.info("服务端异常次数过多，重新进入文章页！")
                        self.web.refresh()
                        self.fast_chapter_page()
                    else:
                        self.log_area.show_log_area("服务端异常次数过多，脚本已停止！")
                        self.logger.error("服务端异常次数过多，最大次数限制3次，脚本已停止！")
                        msgBox = messagebox.showerror("错误", "服务端异常次数过多，脚本已停止，建议等待一段时间后再试！")
                        self.web.quit()
                        self.main_window.quit()
                        sys.exit()

        try:
            next_chapter_button = self.web.find_element(By.CSS_SELECTOR, ".container a .next_chapter")
            self.button_click(next_chapter_button, self.fast_chapter_page, '点击"next_chapter_button"按钮。')
        except Exception as e:
            self.log_area.show_log_area("当前为最后一篇，即将返回专题页。")
            self.logger.info(f"当前为最后一篇，即将返回专题页。错误信息：{e}")
            return_course_button = self.web.find_element(By.CSS_SELECTOR, ".container.title.nav button")
            self.button_click(return_course_button, self.course_page, '点击"return_course_button"按钮。')

    def check_chapter_page_element(self):
        self.element_process.get_current_url()
        self.element_process.check_page_element(By.XPATH, "//div[@class='container title nav']", "chapter",
                                                EC.presence_of_element_located)
        current_title = self.web.find_element(By.XPATH, "//div[@class='container title nav']//div[@class='name']").text
        self.log_area.show_log_area(f"当前文章：{current_title}")
        self.logger.info(f"当前文章：{current_title}")

