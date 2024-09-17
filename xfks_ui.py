# 日志、UI、浏览器、登录页
import logging
import sys
import threading
import os
import webbrowser
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from xfks_element import Element_Process
from xfks_func import Base_Func

def log_message():
    current_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    log_file_path = os.path.join(current_dir, "record.log")
    logging.basicConfig(filename=log_file_path, level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger(__name__)
    return logger

class AutomationUI:
    def __init__(self):
        self.logger = log_message()
        self.main_window = tk.Tk()
        self.main_window.title("学法考试自动化脚本——By Mustrad")
        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()
        window_width = 650
        window_height = 400
        x_position = screen_width - window_width
        y_position = (screen_height - window_height) // 2
        self.main_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.main_window.resizable(0, 0)
        self.main_window.attributes("-topmost", True)
        self.firefox_path_var = tk.StringVar()
        self.firefox_path_var.set("例如：D:/Software/Mozilla Firefox/firefox.exe")
        self.mode_var = tk.IntVar()
        self.mode_var.set(0)

        l1 = tk.Label(self.main_window, text="1、安装Firefox浏览器，点我进行下载，里面有卸载软件，完成学习后可以卸载。",
                      font=("宋体", 12), fg="blue", cursor="hand2")
        l1.place(x=33, y=10)
        l1.bind("<Button-1>", self.open_link_download)
        l2 = tk.Label(self.main_window, text="2、安装后打开浏览器，点击右上角-设置-常规-更新-由您决定，然后关闭浏览器。",
                      font=("宋体", 12))
        l2.place(x=35, y=35)
        l3 = tk.Label(self.main_window, text="3、选择刚才安装的浏览器启动路径(exe文件路径)，并点击“启动浏览器”。",
                      font=("宋体", 12))
        l3.place(x=35, y=60)
        l4 = tk.Label(self.main_window, textvariable=self.firefox_path_var, font=("宋体", 12), background="white")
        l4.place(x=140, y=105)
        l5 = tk.Label(self.main_window, text="4、输入账号密码并登陆，成功进入首页后，选择合适的模式，再点击“启动脚本”。", font=("宋体", 12))
        l5.place(x=35, y=150)
        l6 = tk.Label(self.main_window, text="5、启动成功后，尽量不要操作浏览器，并留意弹窗提示和下方的日志信息!", font=("宋体", 12))
        l6.place(x=35, y=210)
        l7 = tk.Label(self.main_window, text="日志信息：", font=("宋体", 10))
        l7.place(x=35, y=250)
        l8 = tk.Label(self.main_window, text="脚本仅供交流学习，禁止用于商业用途，后续功能看情况更新，有BUG请联系我!",
                      font=("宋体", 10), cursor="hand2")
        l8.place(x=98, y=380)
        l8.bind("<Button-1>", self.open_link_developer_info)
        l8.bind("<Enter>", self.show_developer_info)
        l8.bind("<Leave>", self.hide_developer_info)
        # 个人主页
        self.l9 = tk.Label(self.main_window, font=("宋体", 12), fg="blue")
        self.l9.place(x=63, y=360)

        self.ui_func()
        self.mode_select()

    def ui_func(self):
        b1 = tk.Button(self.main_window, text="选择浏览器", font=("宋体", 11), command=self.select_friefox_browser_path)
        b1.place(x=35, y=90)
        b2 = tk.Button(self.main_window, text="启动浏览器", font=("宋体", 11), command=self.start_friefox_browser_thread)
        b2.place(x=35, y=120)
        b3 = tk.Button(self.main_window, text="启动脚本", font=("宋体", 11), command=self.start_script_thread)
        b3.place(x=35, y=180)
        b4 = tk.Button(self.main_window, text="停止脚本", font=("宋体", 11), command=self.stop_script)
        b4.place(x=150, y=180)
        self.log_area = tk.Text(self.main_window, height=7, width=68, background="white", font=("宋体", 10), fg="green")
        self.log_area.place(x=115, y=250)
        self.show_log_area("动态显示日志信息。")

        # 模式
        self.normal_mode_radio = tk.Radiobutton(self.main_window, text="正常模式", variable=self.mode_var, value=0,command=self.mode_select, activebackground="yellow")
        self.normal_mode_radio.place(x=250, y=180)
        self.fast_mode_radio = tk.Radiobutton(self.main_window, text="快速模式:建议没时间再用！", variable=self.mode_var, value=1,command=self.mode_select, activebackground="yellow")
        self.fast_mode_radio.place(x=330, y=180)


    def open_link_download(self, event):
        webbrowser.open_new("https://www.123pan.com/s/ydsAjv-5Ge03")
    def open_link_developer_info(self, event):
        webbrowser.open_new("https://github.com/Mustrud")
    def show_developer_info(self, event):
        self.l9.config(text="有BUG请把生成的record.log文件发给我，谢谢！邮箱：akali233@outlook.com")
    def hide_developer_info(self, event):
        self.l9.config(text="")

    # ui按钮功能
    def select_friefox_browser_path(self):
        self.current_friefox_browser_path = filedialog.askopenfilename()
        if self.current_friefox_browser_path:
            self.firefox_path_var.set(self.current_friefox_browser_path)
    # 多线程
    def start_friefox_browser_thread(self):
        threading.Thread(target=self.start_friefox_browser).start()
    def start_friefox_browser(self):
        try:
            self.firefox_browser = Firefox_Browser(self.firefox_path_var.get(), self.logger, self, self.main_window)
            self.firefox_browser.open_firefox_browser()
        except Exception as e:
            self.show_log_area("调用浏览器失败！")
            self.logger.error(f"调用浏览器失败！错误信息：{e}")
            msgBox = tk.messagebox.showerror("错误", '初始化失败，请先检查路径！若路径正确但浏览器没出现登录页，关闭浏览器后再点击"启动浏览器"按钮（可能要多次尝试！）。建议重启本软件！')
    # 脚本
    def start_script_thread(self):
        threading.Thread(target=self.start_script).start()
    def start_script(self):
        if not hasattr(self, 'firefox_browser') or not self.firefox_browser.web:
            self.show_log_area("未启动浏览器！")
            self.logger.error("未启动浏览器！")
            msgBox = tk.messagebox.showerror("错误", "请先启动浏览器！")
        elif self.firefox_browser.web.current_url == "http://xfks-study.gdsf.gov.cn/study/index":
            base_func_instance = Base_Func(self.firefox_browser.web, self.logger, self, self.main_window, self.mode_var.get())
            base_func_instance.frist_enter_index_page()
        else:
            self.show_log_area("未进入首页！")
            self.logger.error("未进入首页！")
            msgBox = tk.messagebox.showerror("错误", "请进首页后再启动脚本！")
    def stop_script(self):
        if hasattr(self, 'firefox_browser') and self.firefox_browser.web:
            self.firefox_browser.web.quit()
            self.show_log_area("脚本已停止！")
            self.logger.info("脚本已停止！")
            msgBox = messagebox.showinfo("提示", "脚本已停止！")
        self.main_window.destroy()
        sys.exit()

    def mode_select(self):
        if self.mode_var.get() == 0:
            self.show_log_area("选择正常模式。")
            self.logger.info("选择正常模式。")
        else:
            self.show_log_area("选择快速模式。")
            self.logger.warning("选择快速模式。")
            msgBox = messagebox.showwarning("警告", "快速模式下，直接向服务器发送请求，能瞬间完成一篇，但服务器会有时间记录，所以建议实在没时间再用！")
            self.mode_var.set(1)

    # 动态监控日志信息
    def show_log_area(self, message):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{current_time} {message}\n"
        self.log_area.insert(tk.END, log_message)
        self.log_area.see(tk.END)
        log_count = int(self.log_area.index(tk.END).split('.')[0])
        # 只显示5条
        if log_count > 7:
            self.log_area.delete(1.0, 2.0)

class Firefox_Browser:
    def __init__(self,browser_path, loggger,log_area,main_window):
        self.browser_path = browser_path
        self.logger = loggger
        self.log_area = log_area
        self.main_window = main_window
        self.element_process = None
        self.web = None

    def open_firefox_browser(self):
        try:
            options = Options()
            options.binary_location = self.browser_path
            current_dir = os.path.dirname(os.path.realpath(__file__))
            driver_path = os.path.join(current_dir, "geckodriver.exe")
            service = Service(executable_path=driver_path)
            self.web = webdriver.Firefox(service=service, options=options)
        except Exception as e:
            self.log_area.show_log_area("浏览器初始化失败!")
            self.logger.error(f"浏览器初始化失败！错误信息：{e}")
            if self.web:
                self.web.quit()
                return
        self.check_login_page()

    def check_login_page(self):
        self.web.get("http://xfks-study.gdsf.gov.cn/")
        self.element_process = Element_Process(self.web, self.logger, self.log_area,self.main_window)
        self.element_process.check_page_element(By.CSS_SELECTOR, ".button", "login", EC.element_to_be_clickable)


if __name__ == '__main__':
    window = AutomationUI()
    window.main_window.mainloop()

