#!/usr/bin/env python
# -*-coding:utf-8-*-

"""
RmLine v1.0   2018-03-18
功能：
    1、删除文件数据中包含指定字符串的行，并保存为新的文件
待实现功能：
pass
待解决问题：
pass
"""

__author__ = 'wyl'

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

class ProxyUi(object):
    boxInputPath = None
    boxInputStr = None
    file_Path = None

    def create_gui(self):
        def win_close():
            print('主线程GUI关闭')
            root.destroy()

        root = Tk()
        root.title('文本处理 v1.0')

        # ----------------------菜单项部分开始...------------------------ #
        # 创建顶部菜单页
        menu_bar = Menu(root)
        root.config(menu=menu_bar)

        # 增加文件菜单项
        file_menu = Menu(menu_bar, tearoff=0)  # tearoff虚线分离菜单项
        file_menu.add_command(label='保存日志')
        menu_bar.add_cascade(label='文件', menu=file_menu)

        frm1 = Frame(root)

        # ----------------------服务器参数配置部分开始。。。------------------------ #
        # 创建容器
        container1 = ttk.LabelFrame(frm1, text='路径')
        container1.pack(fill='x')
        container2= ttk.LabelFrame(frm1, text='字符串内容（删除包含以下各行中字符的行）')
        container2.pack(fill='both', expand=True)

        # 选择文件
        Label(container1, text='文件路径：').pack(side='left')
        self.boxInputPath = Entry(container1, borderwidth=1)
        self.boxInputPath.pack(fill='x', expand=True, side='left')
        self.boxInputPath.insert(0, 'C:/Users/admin/Desktop/')
        self.boxInputPath.configure(state='disabled')
        ttk.Button(container1, text='浏览', width=5, command=self.get_path).pack(side='left')

        # 匹配字符串
        self.boxInputStr = Text(container2, borderwidth=1, height=2)
        self.boxInputStr.pack(fill='both', expand=True, side='bottom')
        self.boxInputStr.insert(END, 'sn=0 addr=(nil)')
        ttk.Button(frm2, text='开始', width=10, command=self.dispose_file).pack(side='bottom')

        root.protocol('WM_DELETE_WINDOW', win_close)
        root.mainloop()

    def get_path(self):
        self.file_Path = filedialog.askopenfilename()
        if self.file_Path == '':  # 用于检测用户点击取消保存按钮或文件名为空
            return
        self.boxInputPath.configure(state='normal')
        self.boxInputPath.delete(0, 'end')
        self.boxInputPath.insert(0, self.file_Path)
        self.boxInputPath.configure(state='disabled')

    def dispose_file(self):
        def not_empty(s):
            return s

        line_num = 0
        is_match = False

        # 将用户输入字符串按换行符分割
        list_match_str = self.boxInputStr.get('0.0', 'end').split('\n')
        list_match_str = list(filter(not_empty, list_match_str))
        print('list_match_str：', list_match_str)

        des_file = open(self.file_Path + '.RmLine', 'w')
        with open(self.file_Path, 'r', errors='ignore') as raw_file:
            for line in raw_file.readlines():
                if line == '\n':  # 去掉空行
                    continue
                for match_str in list_match_str:
                    if match_str in  line:
                        line_num += 1
                        is_match = True
                        break
                    else:
                        is_match = False
                if is_match:
                    continue
                des_file.write(line)
        des_file.close()
        messagebox.showinfo('处理完成', '已经删除 {} 行包含 {} 字符的行！\n新文件路径{}'
                            .format(line_num, list_match_str, self.file_Path + '.RmLine'))

if __name__ == '__main__':
    # 创建类实例
    proxy_ui = ProxyUi()

    # 弹出UI主界面
    proxy_ui.create_gui()






