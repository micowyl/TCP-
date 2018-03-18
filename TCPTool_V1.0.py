#!/usr/bin/env python
# -*-coding:utf-8-*-

"""
TCPTool v1.0   2018-03-18
功能：
    1、侦听TCP端口，显示接收数据，下发文本指令
    2、每次只处理一个终端的连接
待实现功能：

待解决问题：

"""

__author__ = 'wyl'

import socket
import threading
import time
import logging
import function_lib
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

box_output_gb = None
scrollbar_y = None
boxInputId = None
labelInputId = None


class ProxyUi(object):
    boxLocalPort = None
    boxOutPutParse = None
    boxInputTxt = None
    menu_box_OutPut = None
    buttonStart = None
    buttonStop = None
    scrollbar_y = None
    labelStatus = None

    saveVar = None
    saveLogPath = './TCPTool_log.txt'  # 日志保存路径

    def create_gui(self):
        def win_close():
            print('主线程GUI关闭')
            self.stop_server()
            root.destroy()

        root = Tk()
        root.title('TCP测试工具 v1.0')
        root.geometry('850x750')

        # ----------------------菜单项部分开始...------------------------ #
        # 创建右键鼠标菜单项
        self.menu_box_OutPut = Menu(root, tearoff=0)
        self.menu_box_OutPut.add_command(label='清空', command=self.clear_boxOutPutParse)

        # 创建顶部菜单页
        menu_bar = Menu(root)
        root.config(menu=menu_bar)

        # 增加文件菜单项
        file_menu = Menu(menu_bar, tearoff=0)  # tearoff虚线分离菜单项
        file_menu.add_command(label='保存日志')
        menu_bar.add_cascade(label='文件', menu=file_menu)

        # 增加导出功能菜单项
        export_menu = Menu(menu_bar, tearoff=0)
        export_menu.add_command(label='HIS', command='')
        export_menu.add_separator()
        export_menu.add_command(label='ARM', command='')
        menu_bar.add_cascade(label='导出', menu=export_menu)

        # 增加保存类菜单项
        save_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='日志', menu=save_menu)
        self.saveVar = IntVar()
        save_menu.add_checkbutton(label='保存日志', variable=self.saveVar, command=self.set_log_save)

        frm1 = Frame(root)
        frm2 = Frame(root)
        frm1.pack(fill='x')
        frm2.pack(fill='both', expand=True)  # 保证树表能够充满整个frm

        # ----------------------服务器参数配置部分开始。。。------------------------ #
        # 创建容器
        container1 = ttk.LabelFrame(frm1, text='服务器配置')
        container1.pack(fill='both', expand=True)

        # 服务器配置
        Label(container1, text='本地监听端口：').grid(row=0, column=0)
        self.boxLocalPort = Entry(container1, width=5, borderwidth=1)
        self.boxLocalPort.grid(row=0, column=1)
        self.boxLocalPort.insert(0, '8509')
        self.buttonStart = ttk.Button(container1, text='启动', width=5, command=self.start_server)
        self.buttonStart.grid(row=0, column=2, padx=10)
        self.buttonStop = ttk.Button(container1, text='停止', width=5, command=self.stop_server, state='disabled')
        self.buttonStop.grid(row=0, column=3, padx=5)

        # 创建标签页控制
        self.tab_control = ttk.Notebook(frm2)
        self.tab_control.pack(fill='both', expand=True)

        tab1 = ttk.Frame(self.tab_control)
        self.tab_control.add(tab1, text='数据解析')
        tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(tab2, text='部标功能')

        # ----------------------标签页tab1布局部分开始。。。------------------------ #
        # *************数据解析显示部分
        # 创建容器
        container2 = ttk.LabelFrame(tab1, text='指令下发')
        container2.pack()
        container3 = ttk.LabelFrame(tab1, text='终端数据')
        container3.pack(fill='both', expand=True)

        # 指令窗口
        self.boxInputTxt = Entry(container2, width=1000, borderwidth=1)
        self.boxInputTxt.pack(fill='x', expand=True, side='left')
        self.boxInputTxt.insert(0, '/dvr/bin/pyctl disk')
        self.boxInputTxt.bind('<Key-Return>', self.send_input_data)

        # 底部状态栏部分
        self.labelStatus = Label(container3, text='状态栏', borderwidth=3, bg='Gainsboro')
        self.labelStatus.pack(fill='x', side='bottom')

        # 终端数据窗口
        self.scrollbar_y = Scrollbar(container3)
        scrollbar_x = Scrollbar(container3, orient='horizontal')
        self.boxOutPutParse = Text(container3, borderwidth=3, width=300, height=300, bg='black', fg='Green',
                                 yscrollcommand=self.scrollbar_y.set,
                                 xscrollcommand=scrollbar_x.set, wrap='none')  # 设置不换行wrap='none'
        self.scrollbar_y.config(command=self.boxOutPutParse.yview)
        self.scrollbar_y.pack(fill='y', expand=True, side='right')
        scrollbar_x.config(command=self.boxOutPutParse.xview)
        scrollbar_x.pack(fill='x', side='bottom')
        self.boxOutPutParse.pack(fill='both', expand=True, side='right')
        self.boxOutPutParse.bind('<Button-3>', self.right_key_parse)



        root.protocol('WM_DELETE_WINDOW', win_close)
        root.mainloop()

    def box_insert(self, data):
        self.boxOutPutParse.insert(END, data)
        if self.scrollbar_y.get()[1] > 0.9:  # 当滚动条在底部附近则自动保持最底部
            self.boxOutPutParse.see(END)

    def start_server(self):
        local_port = re.sub('\s', '', proxy_ui.boxLocalPort.get())
        if args_detection.port_args(local_port):
            messagebox.showerror(title='非法参数', message='服务器启动失败，请输入正确的监听端口！')
            print('启动服务器失败！,监听端口参数（{}）非法'.format(local_port))
            return
        else:
            socket_handle.localPort = int(local_port)
        # 如果bind端口失败，则弹出错误框
        result = socket_handle.create_server_socket()
        if result:
            messagebox.showerror(title='启动失败', message='【{}】-->{}'.format(local_port, result))
            return

        # 按钮状态赋值
        self.buttonStart['state'] = 'disabled'  # 启动按钮置为不可用状态
        self.buttonStop['state'] = 'normal'

        create_dispose_dev_conns_event.set()  # 解除线程 create_client_socket阻塞状态
        socket_handle.serverIsStart = True

    def stop_server(self):  # 需考虑是不是要close所有因终端接入产生的子线程？？？
        self.buttonStop['state'] = 'disabled'
        self.buttonStart['state'] = 'normal'  # 启动按钮置为可用状态

        # 关闭服务器端
        if socket_handle.socketServer is not None:
            socket_handle.socketServer.close()
        if socket_handle.socketDev is not None:
            socket_handle.socketDev.close()
        debug_data = '\n{:-^110}\n关闭服务器socket: {}\n关闭终端socket: {}\n'\
            .format('关闭服务器', socket_handle.socketServer, socket_handle.socketDev)
        proxy_ui.box_insert(debug_data)

        create_dispose_dev_conns_event.clear()
        socket_handle.serverIsStart = False

    def send_input_data(self, event):
        if socket_handle.socketDev is None:
            messagebox.showerror(title='错误', message='终端未连接！指令发送失败！{}'.format(socket_handle.socketDev))
            return
        user_data = self.boxInputTxt.get().strip() + '\n'
        print('发送指令！', user_data)
        proxy_ui.box_insert('发送指令：{}'.format(user_data))
        socket_handle.socketDev.send(user_data.encode('utf-8'))

    def clear_boxOutPutParse(self):
        self.boxOutPutParse.delete('0.0', 'end')

    def right_key_parse(self, event):
        self.menu_box_OutPut.post(event.x_root, event.y_root)

    def set_log_save(self):
        if self.saveVar.get():
            self.labelStatus.config(text='日志保存中：' + self.saveLogPath, fg='blue')
        else:
            self.labelStatus.config(text='')

    def save_log(self, data):
        if self.saveVar.get():
            with open(self.saveLogPath, 'a') as f:
                f.write(data)


class SocketHandle(object):
    maxConnNum = 1  # 服务器支持最大连接数
    localPort = 8506  # 本地监听端口
    socketServer = None  # 服务器端socket
    socketDev = None  # 设备端socket
    serverIsStart = False  # 服务器启动状态

    def create_server_socket(self):
        # 创建服务器端socket
        self.socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socketServer.bind(('0.0.0.0', self.localPort))
        except Exception as e:
            return e
        self.socketServer.listen(self.maxConnNum)
        debug_data = '{:-^110}\n监听端口：{}，最大连接数：{}\n{}\n' \
            .format('启动服务器', self.localPort, self.maxConnNum, self.socketServer)
        proxy_ui.box_insert(debug_data)
        return 0

    def dispose_dev_conns(self):
        while True:
                print('dispose_dev_conns线程阻塞中...')
                create_dispose_dev_conns_event.wait()  # 用于限制只处理一个TCP连接
                print('dispose_dev_conns已解除阻塞状态！')

                # 主线程循环等待新的连接, 如果超时set default timeout(120)都没连接，则重新等待
                try:
                    self.socketDev, addr = self.socketServer.accept()
                except Exception as e:
                    time.sleep(1)
                    if not self.serverIsStart:  # 如果服务器已经停止，退出子线程
                        function_lib.print_colorfont('服务器已经关闭，进入阻塞循环！')
                        create_dispose_dev_conns_event.clear()
                        continue
                    function_lib.print_colorfont('There is no new connection for 2 min, continue wait...')
                    continue

                # 每接收到一个新的连接则创建一个recv_device_data子线程来处理
                thread_recv_device_data = threading.Thread(target=self.recv_device_data, args=(self.socketDev, addr))
                thread_recv_device_data.setDaemon(True)
                thread_recv_device_data.start()

                # 已经存在一个连接的情况下，阻塞接收新的连接
                create_dispose_dev_conns_event.clear()

                debug_data = '\n\n{}\n接收到新连接-->IP：{}，Port：{}\n创建子线程：{}\n当前线程数：{}\n{}\n' \
                    .format('*' * 50, addr[0], addr[1], thread_recv_device_data, threading.active_count(), '*' * 50)
                proxy_ui.box_insert(debug_data)

    def recv_device_data(self, socket_device, device_ip_port):

        def _exception_handle():
            debug_data = '终端()连接断开! \n' \
                         '关闭socket_device: ==> {} \n' \
                         '退出线程recv_device_data: ==> {}'\
                .format(socket_device, threading.current_thread())
            function_lib.err_print('31m', debug_data)
            proxy_ui.box_insert(debug_data)
            socket_handle.socketDev = None
            socket_device.close()

        while True:
            # time.sleep(1)
            # 捕获终端连接断开后的异常，并close掉socket，退出当前子线程
            try:
                # 已设置超时时间为2分钟，如果2分钟都收不到数据，则抛出异常
                print(function_lib.get_time() + ' 等待终端数据...')
                recvdata = socket_device.recv(10240)
            except Exception as e:
                logging.exception(e)
                _exception_handle()
                create_dispose_dev_conns_event.set()  # 线程退出后，开始接收新的连接
                break

            device_data = recvdata.decode('gbk')
            if not device_data:  # 解决如果设备断开连接，会导致子线程死循环一直读取空信息
                function_lib.err_print('31m', '终端()接收到空数据：None data:({})\n'
                                       .format(device_data))

                _exception_handle()
                create_dispose_dev_conns_event.set()  # 线程退出后，开始接收新的连接
                break  # 退出当前子线程
            else:
                print('-' * 160)
                print('Device_data（）[%s, %s, ThreadNum: %d]:\n%s-->%s'
                      % (
                         threading.current_thread(), device_ip_port,
                         threading.active_count(), function_lib.get_time(), device_data))
                proxy_ui.box_insert(device_data)
                proxy_ui.save_log(device_data)


class ArgsDetection(object):

    def port_args(self, port):
        # 端口参数合法性检测
        if re.search('[^0-9]', port):
            return 1

    def ip_args(self, ip):
        return 0


if __name__ == '__main__':
    # 创建全局变量
    leastThreadNum = 3  # 主线程 + create_client_socket + recv_server_data

    # 创建类实例
    proxy_ui = ProxyUi()
    args_detection = ArgsDetection()
    socket_handle = SocketHandle()

    # 设置socket超时时间为120s，防止产生无法关闭的僵尸线程，一直阻塞在recv处
    # socket.setdefaulttimeout(120)

    # 创建线程阻塞标志
    create_dispose_dev_conns_event = threading.Event()
    create_dispose_dev_conns_event.clear()  # 将事件标志设置为False

    # 创建线程
    thread_create_client_socket = threading.Thread(target=socket_handle.dispose_dev_conns)
    thread_create_client_socket.setDaemon(True)
    thread_create_client_socket.start()

    # 弹出UI主界面
    proxy_ui.create_gui()





