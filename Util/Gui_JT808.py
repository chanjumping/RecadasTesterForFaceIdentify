from tkinter import *
from tkinter import filedialog, messagebox
from ParseModel.ParseUpgrade import *
from Util import GlobalVar
from Util.GetTestData import GetTestData


class JTFuncWindow():
    def __init__(self,para,msg,tts,photo,upgrade,reboot, parameter, mainwindow):
        self.frame_jt_para = para
        self.frame_jt_msg = msg
        self.frame_jt_upgrade = upgrade
        self.frame_jt_tts = tts
        self.frame_jt_photo = photo
        self.frame_jt_reboot = reboot
        self.frame_parameter = parameter
        self.mainwindow = mainwindow
        self.jt_FuncWindow()
        self.upgrade_file = None

    def jt_FuncWindow(self):
        self.frame_msg = StringVar()
        self.frame_flag = StringVar()
        self.frame_voice = StringVar()
        self.frame_photo = StringVar()
        # 终端信息
        self.frame_jt_para_querypara = Button(self.frame_jt_para,text="查询终端参数",command=self.query_para,bd=5,width=10)
        self.frame_jt_para_querypara.grid(row=0,column=0,ipadx=20,ipady=5,padx=20,pady=10,sticky=W)
        self.frame_jt_para_setpara = Button(self.frame_jt_para,text="【点击】设置参数",command=self.window_para,bd=5,width=10)
        self.frame_jt_para_setpara.grid(row=0,column=1,ipadx=20,ipady=5,pady=10,padx=20,sticky=W)
        self.frame_jt_attr_queryattr = Button(self.frame_jt_para,text="查询终端属性",command=self.query_attr,bd=5,width=10)
        self.frame_jt_attr_queryattr.grid(row=1,column=0,ipadx=20,ipady=5,pady=10,padx=20,sticky=W)
        # 构造报文
        self.frame_jt_msg_title = Label(self.frame_jt_msg,text="构造报文：")
        self.frame_jt_msg_title.grid(row=0,column=0,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_jt_msg_value = Entry(self.frame_jt_msg,textvariable=self.frame_msg,width=18,bd=5)
        self.frame_jt_msg_value.grid(row=0,column=1,ipadx=20,ipady=5,padx=20,pady=5,sticky=W)
        self.frame_jt_msg_example = Label(self.frame_jt_msg,text="例如：7E 08 05 *** 0D 7E",fg="red")
        self.frame_jt_msg_example.grid(row=1,column=1,ipadx=20, sticky=W)
        self.frame_jt_msg_exe = Button(self.frame_jt_msg,text="发    送",command=self.send_msg,bd=5)
        self.frame_jt_msg_exe.grid(row=2,column=1,ipadx=20,ipady=5,padx=20,pady=5,sticky=W)
        # 语音播报
        self.frame_jt_tts_flag = Label(self.frame_jt_tts,text="TTS标识：")
        self.frame_jt_tts_flag.grid(row=0,column=0,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_jt_tts_flagvalue = Entry(self.frame_jt_tts,textvariable=self.frame_flag,width=18,bd=5)
        self.frame_jt_tts_flagvalue.grid(row=0,column=1,ipadx=20,ipady=5,padx=20,pady=5,sticky=W)
        self.frame_jt_tts_voice = Label(self.frame_jt_tts,text="语音内容：")
        self.frame_jt_tts_voice.grid(row=1,column=0,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_jt_tts_voicevalue = Entry(self.frame_jt_tts,textvariable=self.frame_voice,width=18,bd=5)
        self.frame_jt_tts_voicevalue.grid(row=1,column=1,ipadx=20,ipady=5,padx=20,pady=5,sticky=W)
        self.frame_jt_tts_exe = Button(self.frame_jt_tts,text="播    报",command=self.send_tts,bd=5)
        self.frame_jt_tts_exe.grid(row=2,column=1,ipadx=20,ipady=5,padx=20,pady=5,sticky=W)
        # 立即拍照
        self.frame_jt_photo_type = Label(self.frame_jt_photo,text="类  型：")
        self.frame_jt_photo_type.grid(row=0,column=0,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        girls1 = [("DSM", 1), ('ADAS', 2)]
        self.photo_channel = IntVar()
        self.photo_channel.set(1)
        for girl, num in girls1:
            Radiobutton(self.frame_jt_photo, text=girl, variable=self.photo_channel, value=num).grid(row=0, column=num,
                                                                                ipadx=7, ipady=5, pady=6, sticky=W)
        self.frame_jt_photo_exe = Button(self.frame_jt_photo,text="拍    照",command=self.take_photo,bd=5)
        self.frame_jt_photo_exe.grid(row=1,column=1,columnspan=2,ipadx=20,ipady=5,padx=30,pady=5,sticky=W)
        # 升级操作
        self.frame_jt_upgrade_para = Button(self.frame_jt_upgrade,text="【点击】升级窗口",command=self.window_upgrade,width=17,bd=5)
        self.frame_jt_upgrade_para.grid(row=0,column=0,ipadx=10, ipady=5,padx=90, pady=30, sticky=W)
        # 重启操作
        self.frame_jt_reboot_exe = Button(self.frame_jt_reboot,text="设备重启",command=self.reboot,width=17,bd=5)
        self.frame_jt_reboot_exe.grid(row=0,column=0,ipadx=10, ipady=5,padx=90, pady=30, sticky=W)

        # 参数操作
        self.frame_su_para_case = Label(self.frame_parameter, text="用例：")
        self.frame_su_para_case.grid(row=0, column=0, pady=15, sticky=W)
        self.frame_su_para_select = Button(self.frame_parameter, text="选择用例", command=self.select_case_file, bd=5,
                                           width=15)
        self.frame_su_para_select.grid(row=1, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_su_para_exe = Button(self.frame_parameter, text="执行用例", command=self.case_exe, bd=5, width=15)
        self.frame_su_para_exe.grid(row=1, column=1, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)

    # 选择用例文件
    def select_case_file(self):
        self.casefile = filedialog.askopenfilename()
        self.casefilename = os.path.split(self.casefile)[-1]
        if self.casefilename:
            self.frame_su_para_case.config(text="用例：" + self.casefilename)
        else:
            self.frame_su_para_case.config(text="未选择任何用例")

    # 执行用例文件
    def case_exe(self):
        case = GetTestData(self.casefile)
        case.open()
        test_point, data = case.get_excel_data()
        logger.debug('—————— ' + test_point + ' ——————')
        send_queue.put(data)

    # 参数设置窗口
    def window_para(self):
        self.window_setpara = Toplevel(self.mainwindow)
        self.ww = self.window_setpara.winfo_screenwidth()
        self.wh = self.window_setpara.winfo_screenheight()
        self.mw = (self.ww - 400) / 2
        self.mh = (self.wh - 400) / 2
        self.window_setpara.geometry("%dx%d+%d+%d" % (400, 400, self.mw, self.mh))
        self.window_setpara.title("设置参数")

        self.frame_ip = StringVar()
        self.frame_port = StringVar()
        self.frame_limitspeed = StringVar()
        self.frame_adasspeed = StringVar()
        self.frame_volum = StringVar()
        self.frame_volum.set('06')
        # self.frame_mode = StringVar()

        self.frame_jt_para_ip = Label(self.window_setpara, text="IP地址：", width=10)
        self.frame_jt_para_ip.grid(row=0, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_jt_para_ipvalue = Entry(self.window_setpara, textvariable=self.frame_ip, width=17, bd=5)
        self.frame_jt_para_ipvalue.grid(row=0, column=1,columnspan=2, ipadx=20, ipady=5, pady=5, padx=20, sticky=W)
        self.frame_jt_para_port = Label(self.window_setpara, text="端口号：", width=10)
        self.frame_jt_para_port.grid(row=1, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_jt_para_portvalue = Entry(self.window_setpara, textvariable=self.frame_port, width=17, bd=5)
        self.frame_jt_para_portvalue.grid(row=1, column=1,columnspan=2, ipadx=20, ipady=5, pady=5, padx=20, sticky=W)
        self.frame_jt_para_limitspeed = Label(self.window_setpara, text="最高速度：", width=10)
        self.frame_jt_para_limitspeed.grid(row=2, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_jt_para_limitspeedvalue = Entry(self.window_setpara, textvariable=self.frame_limitspeed, width=17,bd=5)
        self.frame_jt_para_limitspeedvalue.grid(row=2, column=1,columnspan=2, ipadx=20, ipady=5, pady=5, padx=20, sticky=W)
        self.frame_jt_para_adasspeed = Label(self.window_setpara, text="ADAS告警速度：", width=10)
        self.frame_jt_para_adasspeed.grid(row=3, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_jt_para_adasspeedvalue = Entry(self.window_setpara, textvariable=self.frame_adasspeed, width=17,bd=5)
        self.frame_jt_para_adasspeedvalue.grid(row=3, column=1,columnspan=2, ipadx=20, ipady=5, pady=5, padx=20, sticky=W)
        self.frame_jt_para_volum = Label(self.window_setpara, text="音量：", width=10)
        self.frame_jt_para_volum.grid(row=4, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_jt_para_volumnvalue = Scale(self.window_setpara,from_=0,to=8,orient=HORIZONTAL,variable=self.frame_volum,tickinterval=1,length=130)
        self.frame_jt_para_volumnvalue.grid(row=4,column=1,columnspan=2,ipadx=20, ipady=5, pady=5, padx=20,sticky=W)
        self.frame_jt_para_mode = Label(self.window_setpara, text="模式：", width=10)
        self.frame_jt_para_mode.grid(row=5, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        girls1 = [("行车", 1), ('测试', 2)]
        self.mode_value = IntVar()
        self.mode_value.set(1)
        for girl, num in girls1:
            Radiobutton(self.window_setpara, text=girl, variable=self.mode_value, value=num).grid(row=5, column=num,
                                                                                ipadx=7, ipady=5, pady=6, sticky=W)
        self.frame_jt_para_exe = Button(self.window_setpara, text="设    置", command=self.set_para, bd=5)
        self.frame_jt_para_exe.grid(row=6, column=1,columnspan=2, ipadx=20, ipady=5, pady=5, padx=20, sticky=W)

    # 升级窗口
    def window_upgrade(self):
        self.window_upgrade = Toplevel(self.mainwindow)
        self.ww = self.window_upgrade.winfo_screenwidth()
        self.wh = self.window_upgrade.winfo_screenheight()
        self.mw = (self.ww - 400) / 2
        self.mh = (self.wh - 450) / 2
        self.window_upgrade.geometry("%dx%d+%d+%d" % (400, 450, self.mw, self.mh))
        self.window_upgrade.title("升级操作")
        # self.window_upgrade.attributes("-toolwindow", 1)
        self.window_upgrade.wm_attributes("-topmost", 2)

        self.frame_upgradeflag = StringVar()
        self.frame_upgradetype = StringVar()
        self.frame_upgradeurl = StringVar()
        self.frame_hardware = StringVar()
        self.frame_fireware = StringVar()
        self.frame_software = StringVar()

        self.frame_jt_upgrade_flag = Label(self.window_upgrade, text="升级标志：", width=10)
        self.frame_jt_upgrade_flag.grid(row=0, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        girls1 = [("升级", 1), ('不升级', 2)]
        self.upgrade_flag = IntVar()
        self.upgrade_flag.set(1)
        for girl, num in girls1:
            Radiobutton(self.window_upgrade, text=girl, variable=self.upgrade_flag, value=num).grid(row=0, column=num,
                                                                                ipadx=7, ipady=5, pady=6, sticky=W)
        self.frame_jt_upgrade_type = Label(self.window_upgrade, text="升级类型：", width=10)
        self.frame_jt_upgrade_type.grid(row=1, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        girls2 = [("应用升级", 1), ('固件升级', 2)]
        self.upgrade_type = IntVar()
        self.upgrade_type.set(1)
        for girl, num in girls2:
            Radiobutton(self.window_upgrade, text=girl, variable=self.upgrade_type, value=num).grid(row=1, column=num,
                                                                                                    ipadx=7, ipady=5,
                                                                                                    pady=6, sticky=W)
        self.frame_jt_upgrade_url = Label(self.window_upgrade, text="升级包下载地址：", width=10)
        self.frame_jt_upgrade_url.grid(row=2, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_jt_upgrade_urlvalue = Entry(self.window_upgrade, textvariable=self.frame_upgradeurl, width=17,bd=5)
        self.frame_jt_upgrade_urlvalue.grid(row=2, column=1,columnspan=2, ipadx=20, ipady=5, pady=5, padx=20, sticky=W)
        self.frame_jt_upgrade_example = Label(self.window_upgrade,text="例如：http://jumping512.imwork.net:28388/Package.zip",fg="red")
        self.frame_jt_upgrade_example.grid(row=3, column=0,columnspan=3, padx=15, sticky=W)
        self.frame_jt_upgrade_hardware = Label(self.window_upgrade, text="硬件版本号：", width=10)
        self.frame_jt_upgrade_hardware.grid(row=4, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_jt_upgrade_hardwarevalue = Entry(self.window_upgrade, textvariable=self.frame_hardware, width=17,bd=5)
        self.frame_jt_upgrade_hardwarevalue.grid(row=4, column=1,columnspan=2, ipadx=20, ipady=5, pady=5, padx=20, sticky=W)
        self.frame_jt_upgrade_fireware = Label(self.window_upgrade, text="固件版本号：", width=10)
        self.frame_jt_upgrade_fireware.grid(row=5, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_jt_upgrade_firewarevalue = Entry(self.window_upgrade, textvariable=self.frame_fireware, width=17,bd=5)
        self.frame_jt_upgrade_firewarevalue.grid(row=5, column=1, columnspan=2, ipadx=20, ipady=5, pady=5, padx=20,sticky=W)
        self.frame_jt_upgrade_software = Label(self.window_upgrade, text="软件版本号：", width=10)
        self.frame_jt_upgrade_software.grid(row=6, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_jt_upgrade_softwarevalue = Entry(self.window_upgrade, textvariable=self.frame_software, width=17,bd=5)
        self.frame_jt_upgrade_softwarevalue.grid(row=6, column=1, columnspan=2, ipadx=20, ipady=5, pady=5, padx=20,sticky=W)
        self.frame_jt_upgrade_package = Label(self.window_upgrade,text="升级包：")
        self.frame_jt_upgrade_package.grid(row=7,column=0,columnspan=3, padx=20,ipadx=5,ipady=5, pady=5,sticky=W)
        self.frame_jt_upgrade_select = Button(self.window_upgrade,text="选择升级包",command=self.select_package,bd=5)
        self.frame_jt_upgrade_select.grid(row=8,column=0,ipadx=15, ipady=5, pady=5, padx=20,sticky=W)
        self.frame_jt_upgrade_exe = Button(self.window_upgrade, text="升    级", command=self.start_upgrade, bd=5)
        self.frame_jt_upgrade_exe.grid(row=8, column=1,columnspan=2, ipadx=20, ipady=5, pady=5, padx=20, sticky=W)

    def set_para(self):
        txt = '修改参数 : '
        list_num = 0
        self.ip = self.frame_ip.get()
        self.port = self.frame_port.get()
        self.limitspeed = self.frame_limitspeed.get()
        self.adasspeed = self.frame_adasspeed.get()
        self.volum = self.frame_volum.get()
        self.mode = self.mode_value.get()
        if self.mode == 1:
            self.mode = '01'
        elif self.mode == 2:
            self.mode = '02'
        msg_body = ''
        if self.ip:
            list_num += 1
            ip_len = len(self.ip)
            msg_body += '00000013' + num2big(ip_len, 1) + str2hex(self.ip, ip_len)
            txt += '服务器 {} '.format(self.ip)
        if self.port:
            list_num += 1
            msg_body += '00000018' + '04' + num2big(int(self.port), 4)
            txt += '端口号 {} '.format(self.port)
        if self.limitspeed:
            list_num += 1
            msg_body += '00000055' + '04' + num2big(int(self.limitspeed), 4)
            txt += '最高速度 {} '.format(self.limitspeed)
        if self.adasspeed:
            list_num += 1
            msg_body += '0000F091' + '01' + num2big(int(self.adasspeed), 1)
            txt += 'ADAS激活速度 {} '.format(self.adasspeed)
        if self.volum:
            list_num += 1
            msg_body += '0000F092' + '01' + num2big(int(self.volum), 1)
            txt += '告警音量 {} '.format(self.volum)
        if self.mode:
            list_num += 1
            msg_body += '0000F094' + '01' + num2big(int(self.mode), 1)
            txt += '工作模式 {} '.format(self.mode)
        if list_num:
            msg_body = num2big(list_num, 1) + msg_body
            body = '8103' + num2big(int(len(msg_body) / 2), 2) + GlobalVar.DEVICEID + \
                   num2big(GlobalVar.get_serial_no()) + msg_body
            data = '7E' + body + calc_check_code(body) + '7E'
            logger.debug('—————— 设置终端参数 ——————')
            logger.debug('—————— ' + txt + ' ——————')
            send_queue.put(data)
        # self.window_setpara.destroy()

    # 查询参数
    def query_para(self):
        logger.debug('—————— 查询终端参数 ——————')
        body = '8104' + '0000' + GlobalVar.DEVICEID + num2big(GlobalVar.get_serial_no())
        data = '7E' + body + calc_check_code(body) + '7E'
        send_queue.put(data)

    # 查询属性
    def query_attr(self):
        logger.debug('—————— 查询终端属性 ——————')
        body = '8107' + '0000' + GlobalVar.DEVICEID + num2big(GlobalVar.get_serial_no())
        data = '7E' + body + calc_check_code(body) + '7E'
        send_queue.put(data)

    # 构造报文
    def send_msg(self):
        self.msg = self.frame_msg.get()
        send_queue.put(self.msg)

    # 语音播报
    def send_tts(self):
        self.flag = self.frame_flag.get()
        self.voice = self.frame_voice.get()
        if self.voice:
            if self.flag:
                tts_flag_ = num2big(int(self.flag), 1)
            else:
                tts_flag_ = '08'
            msg_body = tts_flag_ + byte2str(self.voice.encode('gbk'))
            body = '8300' + num2big(int(len(msg_body) / 2)) + GlobalVar.DEVICEID + \
                   num2big(GlobalVar.get_serial_no()) + msg_body
            data = '7E' + body + calc_check_code(body) + '7E'
            send_queue.put(data)

    # 立即拍照
    def take_photo(self):
        self.photo = self.photo_channel.get()
        if self.photo == 1:
            self.photo = '00'
        elif self.photo == 2:
            self.photo ='01'
        if self.photo:
            msg_body = num2big(int(self.photo), 1) + '00' * 11
            body = '8801' + '000C' + GlobalVar.DEVICEID + num2big(GlobalVar.get_serial_no()) + msg_body
            data = '7E' + body + calc_check_code(body) + '7E'
            send_queue.put(data)

    # 设备重启
    def reboot(self):
        body = '8F01' + '0000' + GlobalVar.DEVICEID + num2big(GlobalVar.get_serial_no())
        data = '7E' + body + calc_check_code(body) + '7E'
        send_queue.put(data)

    # 选择升级包
    def select_package(self):
        self.upgrade_file = filedialog.askopenfilename()
        file_name = os.path.split(self.upgrade_file)[-1]
        if file_name:
            self.frame_jt_upgrade_package.configure(text="升级包：" + file_name)
        else:
            self.frame_jt_upgrade_package.configure(text="未选择任何升级包。")

    # 执行升级
    def start_upgrade(self):
        upgrade_flag = self.upgrade_flag.get()
        upgrade_type = self.upgrade_type.get()
        upgrade_url = self.frame_upgradeurl.get()
        up_hardware = self.frame_hardware.get()
        up_firmware = self.frame_fireware.get()
        up_software = self.frame_software.get()
        active_upgrade_ = True
        if upgrade_flag and upgrade_type and upgrade_url and self.upgrade_file:
            upgrade_jt808(self.upgrade_file, upgrade_flag, upgrade_type, up_hardware, up_firmware, up_software,
                          upgrade_url, active_upgrade_)
        # else:
        #     messagebox.showerror(title="error", message="Parameter Error")
        # self.window_upgrade.destroy()
