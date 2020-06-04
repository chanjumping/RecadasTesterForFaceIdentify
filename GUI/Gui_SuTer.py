from tkinter import *
from tkinter import Radiobutton
from Util.GlobalVar import *
from Util.CommonMethod import *
import Util.GlobalVar as GlobalVar
from tkinter import messagebox, filedialog
import tkinter.filedialog
from Util.GetTestData import GetTestData


class SuTerFuncWindow():
    def __init__(self,upgrade,msg,info,para,tts,photo,file,mainwindow):
        self.frame_dev_upgrade = upgrade
        self.frame_dev_msg = msg
        self.frame_dev_info = info
        self.frame_dev_para = para
        self.frame_dev_tts = tts
        self.frame_dev_photo = photo
        self.frame_dev_file = file
        self.mainwindow = mainwindow
        self.agreement_sign = "7E"
        self.dev_FuncWindow()

    def dev_FuncWindow(self):
        self.frame_upgrade_path = StringVar()
        self.frame_msg = StringVar()
        # self.frame_trans = StringVar()
        # self.frame_devid = StringVar()
        self.frame_ip = StringVar()
        self.frame_port = StringVar()
        self.frame_speed = StringVar()
        self.frame_carnumber = StringVar()
        self.frame_carcolor = StringVar()
        self.frame_overspeed_time = StringVar()
        self.frame_overspeed_chazhi = StringVar()
        self.frame_default_time = StringVar()
        self.frame_tts = StringVar()
        # self.frame_type = StringVar()
        self.frame_num = StringVar()
        self.frame_time = StringVar()
        self.frame_size = StringVar()
        self.frame_name = StringVar()
        self.frame_flag = StringVar()
        #升级操作
        self.frame_dev_upgrade_direct = Label(self.frame_dev_upgrade,text="升级包地址：")
        self.frame_dev_upgrade_direct.grid(row=0,column=0,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_dev_upgrade_path = Entry(self.frame_dev_upgrade,textvariable=self.frame_upgrade_path,bd=5,width=18)
        self.frame_dev_upgrade_path.grid(row=0,column=1,ipadx=20,ipady=5,pady=5,padx=20,sticky=W)
        self.frame_dev_upgrade_example = Label(self.frame_dev_upgrade,text="例如：ftp://test:123@1.1.1.1/Package.zip;;",fg="red")
        self.frame_dev_upgrade_example.grid(row=1,column=0,columnspan=2,ipadx=20,sticky=E)
        self.frame_dev_upgrade_exe = Button(self.frame_dev_upgrade,text="开始升级",command=self.start_upgrade,bd=5)
        self.frame_dev_upgrade_exe.grid(row=2,column=1,ipadx=20,ipady=5,pady=5,padx=20,sticky=W)
        #构造报文
        self.frame_dev_msg_text = Label(self.frame_dev_msg, text="构造的报文：")
        self.frame_dev_msg_text.grid(row=0, column=0, ipadx=20, ipady=5,padx=5, pady=5, sticky=W)
        self.frame_dev_msg_cont = Entry(self.frame_dev_msg, textvariable=self.frame_msg,bd=5,width=17)
        self.frame_dev_msg_cont.grid(row=0, column=1, ipadx=20, ipady=5, pady=5,padx=20, sticky=W)
        self.frame_dev_msg_example = Label(self.frame_dev_msg,text="例如：7E 89 00 **** 4D 7E",fg="red")
        self.frame_dev_msg_example.grid(row=1,column=1,ipadx=20,padx=5,sticky=W)
        self.frame_dev_msg_exe = Button(self.frame_dev_msg, text="发   送", command=self.send_msg, bd=5)
        self.frame_dev_msg_exe.grid(row=2, column=1, ipadx=20, ipady=5, pady=5,padx=20, sticky=W)
        # #基本信息查询
        # self.frame_dev_info_trans = Label(self.frame_dev_info,text="透传类型：",width=10)
        # self.frame_dev_info_trans.grid(row=0, column=0, ipadx=10, ipady=5, pady=5, sticky=W)
        # self.frame_dev_info_f7 = Radiobutton(self.frame_dev_info,text="状态",variable=self.frame_trans,value="F7",indicatoron=0,bd=4)
        # self.frame_dev_info_f7.grid(row=0,column=1,columnspan=2,padx=20,pady=2,ipady=5,sticky=W)
        # self.frame_dev_info_f8 = Radiobutton(self.frame_dev_info,text="信息",variable=self.frame_trans,value="F8",indicatoron=0,bd=4)
        # self.frame_dev_info_f8.grid(row=0,column=3,columnspan=2,padx=20,pady=2,ipady=5,sticky=W)
        # self.frame_dev_info_id = Label(self.frame_dev_info,text="外设ID：",width=10)
        # self.frame_dev_info_id.grid(row=1, column=0, ipadx=5, ipady=5, pady=5, sticky=W)
        # self.frame_dev_info_64 = Radiobutton(self.frame_dev_info,text="ADAS",variable=self.frame_devid,value="64",bd=4)
        # self.frame_dev_info_64.grid(row=1,column=1,pady=5,ipady=5, sticky=W)
        # self.frame_dev_info_65 = Radiobutton(self.frame_dev_info,text="DSM",variable=self.frame_devid,value="65",bd=4)
        # self.frame_dev_info_65.grid(row=1,column=2,pady=5,ipady=5,sticky=W)
        # self.frame_dev_info_66 = Radiobutton(self.frame_dev_info,text="TPMS",variable=self.frame_devid,value="66",bd=4)
        # self.frame_dev_info_66.grid(row=1,column=3,pady=5,ipady=5,sticky=W)
        # self.frame_dev_info_67 = Radiobutton(self.frame_dev_info,text="BSD",variable=self.frame_devid,value="67",bd=4)
        # self.frame_dev_info_67.grid(row=1,column=4,pady=5,ipady=5,sticky=W)
        # self.frame_dev_info_query = Button(self.frame_dev_info,text="查    询",command=self.query_info,bd=5)
        # self.frame_dev_info_query.grid(row=2, column=1,columnspan=4, ipadx=20, ipady=5, pady=5,padx=50, sticky=W)

        # 基本信息查询
        self.frame_dev_info_trans = Label(self.frame_dev_info,text="透传类型：",width=10)
        self.frame_dev_info_trans.grid(row=0, column=0, ipadx=10, ipady=5, pady=5, sticky=W)

        girls1 = [("状态", 1), ('信息', 2)]
        self.frame_trans = IntVar()
        self.frame_trans.set(1)
        for girl, num in girls1:
            Radiobutton(self.frame_dev_info, text=girl, variable=self.frame_trans, value=num,
                        indicatoron=0, bd=4).grid(row=0, column=num, columnspan=2,padx=20,pady=2,ipady=5,sticky=W)

        self.frame_dev_info_id = Label(self.frame_dev_info,text="外设ID：",width=10)
        self.frame_dev_info_id.grid(row=1, column=0, ipadx=5, ipady=5, pady=5, sticky=W)

        girls1 = [("DSM", 1), ('ADAS', 2), ('BSD', 3)]
        self.frame_devid = IntVar()
        self.frame_devid.set(1)
        for girl, num in girls1:
            Radiobutton(self.frame_dev_info, text=girl, variable=self.frame_devid, value=num).grid(row=1, column=num,
                                                                                ipadx=7, ipady=5, pady=6, sticky=W)

        self.frame_dev_info_query = Button(self.frame_dev_info, text="查    询", command=self.query_info,bd=5)
        self.frame_dev_info_query.grid(row=2, column=1, columnspan=4, ipadx=20, ipady=5, pady=5, padx=10, sticky=W)

        #参数操作
        self.frame_dev_para_case = Label(self.frame_dev_para, text="用例：")
        self.frame_dev_para_case.grid(row=0, column=0, pady=15, sticky=W)
        self.frame_dev_para_select = Button(self.frame_dev_para, text="选择用例", command=self.select_case_file, bd=5,
                                            width=15)
        self.frame_dev_para_select.grid(row=1, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_dev_para_exe = Button(self.frame_dev_para, text="执行用例", command=self.case_exe, bd=5, width=15)
        self.frame_dev_para_exe.grid(row=1, column=1, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_dev_para_query = Button(self.frame_dev_para, text="查询所有参数", command=self.query_allpara, bd=5,
                                         width=15)
        self.frame_dev_para_query.grid(row=2, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_jt_attr_queryattr = Button(self.frame_dev_para,text="查询终端属性",command=self.query_attr,bd=5,width=15)
        self.frame_jt_attr_queryattr.grid(row=2,column=1,ipadx=20,ipady=5,pady=5,padx=5,sticky=W)

        #tts语音
        self.frame_dev_tts_flag = Label(self.frame_dev_tts,text="TTS标记：",width=10)
        self.frame_dev_tts_flag.grid(row=0, column=0, ipadx=20, ipady=5,padx=5, pady=5, sticky=W)
        self.frame_dev_tts_flagcont = Entry(self.frame_dev_tts,textvariable=self.frame_flag,width=18,bd=5)
        self.frame_dev_tts_flagcont.grid(row=0, column=1, ipadx=20, ipady=5,padx=20, pady=5, sticky=W)
        self.frame_dev_tts_voice = Label(self.frame_dev_tts,text="语音内容：",width=10)
        self.frame_dev_tts_voice.grid(row=1, column=0, ipadx=20, ipady=5,padx=5, pady=5, sticky=W)
        self.frame_dev_tts_voicecont = Entry(self.frame_dev_tts,textvariable=self.frame_tts,width=18,bd=5)
        self.frame_dev_tts_voicecont.grid(row=1, column=1, ipadx=20, ipady=5,padx=20, pady=5, sticky=W)
        self.frame_dev_tts_exe = Button(self.frame_dev_tts,text="播    报",command=self.broadcast_vioce,bd=5)
        self.frame_dev_tts_exe.grid(row=2, column=1, ipadx=20, ipady=5,padx=20, pady=5, sticky=W)
        # 立即拍照
        self.frame_dev_takephoto = Button(self.frame_dev_photo,text="【主动拍照窗口】",command=self.window_photo,width=18,bd=5)
        self.frame_dev_takephoto.grid(row=0,column=0,ipadx=20, ipady=5,padx=5, pady=20, sticky=W)
        self.frame_dev_para_window = Button(self.frame_dev_photo,text="【设置参数窗口】",command=self.window_para,bd=5,width=15)
        self.frame_dev_para_window.grid(row=0, column=1, ipadx=20, ipady=5, padx=5, pady=20, sticky=W)
        # self.frame_dev_takephoto = Button(self.frame_dev_photo,text="开启实时视频",command=self.start_instant_video,width=18,bd=5)
        # self.frame_dev_takephoto.grid(row=1,column=0,ipadx=20, ipady=5,padx=5, pady=20, sticky=W)
        # self.frame_dev_para_window = Button(self.frame_dev_photo,text="关闭实时视频",command=self.stop_instant_video,bd=5,width=15)
        # self.frame_dev_para_window.grid(row=1, column=1, ipadx=20, ipady=5, padx=5, pady=20, sticky=W)


        #远程查询告警附件
        self.frame_dev_remote = Button(self.frame_dev_file,text="【远程查询窗口】",command=self.window_remote,width=18,bd=5)
        self.frame_dev_remote.grid(row=0,column=0,ipadx=10, ipady=5,padx=90, pady=30, sticky=W)


    #升级
    # ftp://test:123456@121.40.90.148/RW_CA_SU_V410R004B001SP01-1-001SP02_inc.zip;;
    def start_upgrade(self):
        self.upgrade_path = self.frame_upgrade_path.get()
        if self.upgrade_path:
            msg_body = '01' + byte2str(self.upgrade_path.encode("gbk"))
            body = '8105' + num2big(int(len(msg_body) / 2)) + GlobalVar.DEVICEID + num2big(
                GlobalVar.get_serial_no()) + msg_body
            data = '7E' + body + calc_check_code(body) + '7E'
            send_queue.put(data)
        else:
            messagebox.showinfo(title="error",message="Upgrade package address cannot be empt")

    #构造报文
    def send_msg(self):
        self.msg = self.frame_msg.get()
        send_queue.put(self.msg)

    # #查询信息
    # def query_info(self):
    #     self.trans = self.frame_trans.get()
    #     self.id = self.frame_devid.get()
    #     if self.trans and self.id:
    #         msg_body = self.trans + "01" + self.id
    #         body = "8900" + num2big(int(len(msg_body)/2)) + GlobalVar.DEVICEID + num2big(GlobalVar.get_serial_no(), 2) + msg_body
    #         data = self.agreement_sign + body + calc_check_code(body) + self.agreement_sign
    #         send_queue.put(data)
    #     else:
    #         messagebox.showerror(title="error",message="Parameter Error")

    # 查询信息
    def query_info(self):
        self.trans = self.frame_trans.get()
        if self.trans == 1:
            self.trans = 'F7'
        elif self.trans == 2:
            self.trans = 'F8'
        self.id = self.frame_devid.get()
        if self.id == 1:
            self.id = '65'
        elif self.id == 2:
            self.id = '64'
        elif self.id == 3:
            self.id = '67'
        msg_body = self.trans + "01" + self.id
        body = "8900" + num2big(int(len(msg_body) / 2)) + GlobalVar.DEVICEID + num2big(GlobalVar.get_serial_no(), 2) + msg_body
        data = self.agreement_sign + body + calc_check_code(body) + self.agreement_sign
        send_queue.put(data)

    # 查询参数
    def query_allpara(self):
        logger.debug('—————— 查询终端参数 ——————')
        # body = "8106" + "0015" + GlobalVar.DEVICEID + num2big(GlobalVar.get_serial_no()) + "010000F364"
        msg_body = "0B0000000100000013000000180000002900000055000000560000005B00000083000000840000F3650000F364"
        body = "8106" + num2big(int(len(msg_body)/2)) + GlobalVar.DEVICEID + num2big(GlobalVar.get_serial_no()) + msg_body
        data = self.agreement_sign + body + calc_check_code(body) + self.agreement_sign
        send_queue.put(data)

    # 查询属性
    def query_attr(self):
        logger.debug('—————— 查询终端属性 ——————')
        body = '8107' + '0000' + GlobalVar.DEVICEID + num2big(GlobalVar.get_serial_no())
        data = '7E' + body + calc_check_code(body) + '7E'
        send_queue.put(data)

    def popup_para(attr):
        messagebox.showinfo(title="终端参数", message=attr)

    def set_para(self):
        ip = self.frame_ip.get()
        port = self.frame_port.get()
        limitspeed = self.frame_speed.get()
        carnumber = self.frame_carnumber.get()
        carcolor = self.frame_carcolor.get()
        overspeed_time = self.frame_overspeed_time.get()
        overspeed_chazhi = self.frame_overspeed_chazhi.get()
        default_time = self.frame_default_time.get()

        num = 0
        msg_body = ""
        txt = ""
        if ip:
            num += 1
            ip_len = len(ip)
            msg_body += '00000013' + num2big(ip_len, 1) + str2hex(ip, ip_len)
            txt += '服务器 {} '.format(ip)
        if port:
            num += 1
            msg_body += '00000018' + '04' + num2big(int(port), 4)
            txt += '端口号 {} '.format(port)
        if default_time:
            num += 1
            msg_body += '00000029' + '04' + num2big(int(default_time), 4)
            txt += '缺省时间汇报间隔 {} '.format(default_time)
        if limitspeed:
            num += 1
            msg_body += '00000055' + '04' + num2big(int(limitspeed), 4)
            txt += '最高速度 {} '.format(limitspeed)
        if carnumber:
            num += 1
            num_len = len(byte2str(carnumber.encode("gbk")))/2
            msg_body += '00000083' + num2big(int(num_len),1) + byte2str(carnumber.encode("gbk"))
            txt += '车牌号码 {} '.format(carnumber)
        if carcolor:
            num += 1
            msg_body += '00000084' + "01" + num2big(int(carcolor),1)
            txt += '车辆颜色 {} '.format(carcolor)
        if overspeed_time:
            num += 1
            msg_body += '00000056' + "04" + num2big(int(overspeed_time),4)
            txt += '超速持续时间 {} '.format(overspeed_time)
        if overspeed_chazhi:
            num += 1
            msg_body += '0000005B' + "02" + num2big(int(overspeed_chazhi),2)
            txt += '超速预警差值 {} '.format(overspeed_chazhi)
        if num:
            msg_body = num2big(num, 1) + msg_body
            body = '8103' + num2big(int(len(msg_body) / 2), 2) + GlobalVar.DEVICEID + \
                   num2big(GlobalVar.get_serial_no()) + msg_body
            data = '7E' + body + calc_check_code(body) + '7E'
            logger.debug('—————— 设置终端参数 ——————')
            logger.debug('—————— ' + txt + ' ——————')
            send_queue.put(data)
        # self.window_setpara.destroy()

    # 查询指定参数
    def query_appointpara(self):
        pass

    # 选择测试用例
    def select_case_file(self):
        self.casefile = tkinter.filedialog.askopenfilename()
        self.casefilename = os.path.split(self.casefile)[-1]
        if self.casefilename:
            self.frame_dev_para_case.config(text="用例：" + self.casefilename)
        else:
            self.frame_dev_para_case.config(text="未选择任何用例")

    # 执行测试用例
    def case_exe(self):
        case = GetTestData(self.casefile)
        case.open()
        test_point, data = case.get_excel_data()
        logger.debug('—————— ' + test_point + ' ——————')
        send_queue.put(data)

    #设置参数
    # def set_para(self):
    #     self.ip = self.frame_ip.get()
    #     self.port = self.frame_port.get()
    #     number = 0
    #     msg_body = ""
    #     if self.ip:
    #         number+=1
    #         msg_body += "00000013" + num2big(len(self.ip),1) + str2hex(self.ip,len(self.ip))
    #     if self.port:
    #         number+=1
    #         msg_body += "00000018" + "04" + num2big(int(self.port),4)
    #     if number:
    #         msg_body = num2big(number,1) + msg_body
    #         body = "8103" + num2big(int(len(msg_body)/2),2) + GlobalVar.DEVICEID + num2big(GlobalVar.get_serial_no(), 2) + msg_body
    #         data = self.agreement_sign + body + calc_check_code(body) + self.agreement_sign
    #         send_queue.put(data)

    # TTS语音
    def broadcast_vioce(self):
        self.flag = self.frame_flag.get()
        self.tts = self.frame_tts.get()
        if self.tts:
            if self.flag:
                tts_flag = num2big(int(self.flag), 1)
            else:
                tts_flag = '08'
            msg_body = tts_flag + byte2str(self.tts.encode('gbk'))
            body = '8300' + num2big(int(len(msg_body) / 2)) + GlobalVar.DEVICEID + \
                   num2big(GlobalVar.get_serial_no(), 2) + msg_body
            data = '7E' + body + calc_check_code(body) + '7E'
            send_queue.put(data)
        else:
            messagebox.showerror(title="Parameter Error",message="Please input voice")

    # 立即拍照
    def take_photo(self):
        self.passid = self.frame_channel.get()
        if self.passid == 1:
            self.passid = '01'
        elif self.passid == 2:
            self.passid = '02'
        self.num = self.frame_num.get()
        self.time = self.frame_time.get()
        para_num = 7
        msg_body = ""
        # if self.passid:
        para_num += 1
        msg_body += self.passid
        if self.num:
            para_num += 2
            msg_body += num2big(int(self.num))
        else:
            para_num += 2
            msg_body += "0001"
        if self.time:
            para_num += 2
            msg_body += num2big(int(self.time))
        else:
            para_num += 2
            msg_body += "0001"
        msg_body += "00000000000000"
        body = "8801" + num2big(para_num) + GlobalVar.DEVICEID + num2big(GlobalVar.get_serial_no(), 2) + msg_body
        data = self.agreement_sign + body +  calc_check_code(body) + self.agreement_sign
        send_queue.put(data)
        # else:
        #     messagebox.showerror(title="Parameter Error",message="Please choose the type of snapshot")
        # self.window_takephoto.destroy()


    # 远程查看告警附件
    def query_file(self):
        self.ip = self.frame_ip.get()
        self.port = self.frame_port.get()
        self.flag = self.frame_flag.get()
        self.name = self.frame_name.get()
        if self.ip and self.port and self.flag:
            msg_body = num2big(len(self.ip),1) + str2hex(self.ip,len(self.ip)) + num2big(int(self.port))\
                       + "0000" + self.flag + num2big(len(self.name),1) + str2hex(self.name,len(self.name))
            body = "9211" + num2big(int(len(msg_body)/2)) + GlobalVar.DEVICEID + num2big(GlobalVar.get_serial_no(), 2) + msg_body
            data = self.agreement_sign + body + calc_check_code(body) + self.agreement_sign
            send_queue.put(data)
        else:
            messagebox.showerror(title="error",message="Parameter Error")
        self.window_remotequery.destroy()

    def window_remote(self):
        self.window_remotequery = Toplevel(self.mainwindow)
        self.ww = self.window_remotequery.winfo_screenwidth()
        self.wh = self.window_remotequery.winfo_screenheight()
        self.mw = (self.ww - 400)/2
        self.mh = (self.wh - 300)/2
        self.window_remotequery.geometry("%dx%d+%d+%d" %(400,300,self.mw,self.mh))
        self.window_remotequery.title("远程查询告警附件窗口")

        self.frame_dev_file_ip = Label(self.window_remotequery, text="服务器地址：", width=10)
        self.frame_dev_file_ip.grid(row=0, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_dev_file_ipcont = Entry(self.window_remotequery, textvariable=self.frame_ip, width=18, bd=5)
        self.frame_dev_file_ipcont.grid(row=0, column=1, ipadx=20, ipady=5, padx=20, pady=5, sticky=W)
        self.frame_dev_file_port = Label(self.window_remotequery, text="服务器端口：", width=10)
        self.frame_dev_file_port.grid(row=1, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_dev_file_portcont = Entry(self.window_remotequery, textvariable=self.frame_port, width=18, bd=5)
        self.frame_dev_file_portcont.grid(row=1, column=1, ipadx=20, ipady=5, padx=20, pady=5, sticky=W)
        self.frame_dev_file_flag = Label(self.window_remotequery, text="报警标识号：", width=10)
        self.frame_dev_file_flag.grid(row=2, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_dev_file_flagcont = Entry(self.window_remotequery, textvariable=self.frame_flag, width=18, bd=5)
        self.frame_dev_file_flagcont.grid(row=2, column=1, ipadx=20, ipady=5, padx=20, pady=5, sticky=W)
        self.frame_dev_file_name = Label(self.window_remotequery, text="文件名称：", width=10)
        self.frame_dev_file_name.grid(row=3, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_dev_file_namecont = Entry(self.window_remotequery, textvariable=self.frame_name, width=18, bd=5)
        self.frame_dev_file_namecont.grid(row=3, column=1, ipadx=20, ipady=5, padx=20, pady=5, sticky=W)
        self.frame_dev_file_exe = Button(self.window_remotequery, text="查    询", command=self.query_file, bd=5)
        self.frame_dev_file_exe.grid(row=4, column=1, ipadx=20, ipady=5, padx=20, pady=5, sticky=W)

    def window_photo(self):
        self.window_takephoto= Toplevel(self.mainwindow)
        self.ww = self.window_takephoto.winfo_screenwidth()
        self.wh = self.window_takephoto.winfo_screenheight()
        self.mw = (self.ww - 400) / 2
        self.mh = (self.wh - 300) / 2
        self.window_takephoto.geometry("%dx%d+%d+%d" % (400, 300, self.mw, self.mh))
        self.window_takephoto.title("主动拍照窗口")

        # self.frame_dev_photo_title = Label(self.window_takephoto, text="抓拍类型：", width=10)
        # self.frame_dev_photo_title.grid(row=0, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        # self.frame_dev_photo_type01 = Radiobutton(self.window_takephoto, text="DSM", variable=self.frame_type,
        #                                           value="01", bd=4)
        # self.frame_dev_photo_type01.grid(row=0, column=1, ipadx=5, ipady=5, padx=1, pady=5, sticky=W)
        # self.frame_dev_photo_type02 = Radiobutton(self.window_takephoto, text="ADAS", variable=self.frame_type,
        #                                           value="02", bd=4)
        # self.frame_dev_photo_type02.grid(row=0, column=2, ipadx=5, ipady=5, padx=1, pady=5, sticky=W)
        # self.frame_dev_photo_type03 = Radiobutton(self.window_takephoto, text="3road", variable=self.frame_type,
        #                                           value="03", bd=4)
        # self.frame_dev_photo_type03.grid(row=0, column=3, ipadx=5, ipady=5, padx=1, pady=5, sticky=W)

        self.frame_dev_photo_title = Label(self.window_takephoto, text="抓拍类型：", width=10)
        self.frame_dev_photo_title.grid(row=0, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        girls1 = [("DSM", 1), ('ADAS', 2)]
        self.frame_channel = IntVar()
        self.frame_channel.set(1)
        for girl, num in girls1:
            Radiobutton(self.window_takephoto, text=girl, variable=self.frame_channel, value=num).grid(row=0, column=num,
                                                                                ipadx=7, ipady=5, pady=6, sticky=W)

        self.frame_dev_photo_num = Label(self.window_takephoto, text="拍照张数：", width=10)
        self.frame_dev_photo_num.grid(row=1, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_dev_photo_numvalue = Entry(self.window_takephoto, textvariable=self.frame_num, width=18, bd=5)
        self.frame_dev_photo_numvalue.grid(row=1, column=1, columnspan=3, ipadx=20, ipady=5, padx=20, pady=5, sticky=W)
        self.frame_dev_photo_numexample = Label(self.window_takephoto, text="0：不抓拍   65535：最大张数",fg="red")
        self.frame_dev_photo_numexample.grid(row=2, column=1, columnspan=3, ipadx=10, ipady=5, padx=20,
                                             sticky=W)
        self.frame_dev_photo_time = Label(self.window_takephoto, text="拍照间隔：", width=10)
        self.frame_dev_photo_time.grid(row=3, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_dev_photo_timevalue = Entry(self.window_takephoto, textvariable=self.frame_time, width=18, bd=5)
        self.frame_dev_photo_timevalue.grid(row=3, column=1, columnspan=3, ipadx=20, ipady=5, padx=20, pady=5, sticky=W)
        self.frame_dev_photo_timeexample = Label(self.window_takephoto, text="0：录像      65535：最大间隔",fg="red")
        self.frame_dev_photo_timeexample.grid(row=4, column=1, columnspan=3, ipadx=10, ipady=5, padx=20,
                                              sticky=W)
        self.frame_dev_photo_exe = Button(self.window_takephoto, text="立即抓拍", command=self.take_photo, bd=5)
        self.frame_dev_photo_exe.grid(row=5, column=1, columnspan=3, ipadx=20, ipady=5, padx=20, pady=5, sticky=W)

    def window_para(self):
        self.window_setpara = Toplevel(self.mainwindow)
        self.ww = self.window_setpara.winfo_screenwidth()
        self.wh = self.window_setpara.winfo_screenheight()
        self.mw = (self.ww - 400) / 2
        self.mh = (self.wh - 500) / 2
        self.window_setpara.geometry("%dx%d+%d+%d" % (400, 500, self.mw, self.mh))
        self.window_setpara.title("参数设置窗口")

        self.frame_dev_para_ip = Label(self.window_setpara,text="IP地址：",width=10)
        self.frame_dev_para_ip.grid(row=0, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_dev_para_ipvalue = Entry(self.window_setpara,textvariable=self.frame_ip,bd=5,width=15)
        self.frame_dev_para_ipvalue.grid(row=0, column=1, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_dev_para_port = Label(self.window_setpara,text="端口号：",width=10)
        self.frame_dev_para_port.grid(row=1, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_dev_para_portvalue = Entry(self.window_setpara,textvariable=self.frame_port,bd=5,width=15)
        self.frame_dev_para_portvalue.grid(row=1, column=1, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_dev_para_speed = Label(self.window_setpara,text="最高速度：",width=10)
        self.frame_dev_para_speed.grid(row=2, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_dev_para_speedvalue = Entry(self.window_setpara,textvariable=self.frame_speed,bd=5,width=15)
        self.frame_dev_para_speedvalue.grid(row=2, column=1, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_dev_para_number = Label(self.window_setpara,text="车牌号：",width=10)
        self.frame_dev_para_number.grid(row=3, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_dev_para_numbervalue = Entry(self.window_setpara,textvariable=self.frame_carnumber,bd=5,width=15)
        self.frame_dev_para_numbervalue.grid(row=3, column=1, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_dev_para_color = Label(self.window_setpara,text="车辆颜色：",width=10)
        self.frame_dev_para_color.grid(row=4, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_dev_para_colorvalue = Entry(self.window_setpara,textvariable=self.frame_carcolor,bd=5,width=15)
        self.frame_dev_para_colorvalue.grid(row=4, column=1, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)

        self.frame_dev_para_color = Label(self.window_setpara,text="超速持续时间：",width=10)
        self.frame_dev_para_color.grid(row=5, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_dev_para_colorvalue = Entry(self.window_setpara,textvariable=self.frame_overspeed_time,bd=5,width=15)
        self.frame_dev_para_colorvalue.grid(row=5, column=1, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)

        self.frame_dev_para_color = Label(self.window_setpara,text="超速预警差值：",width=10)
        self.frame_dev_para_color.grid(row=6, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_dev_para_colorvalue = Entry(self.window_setpara,textvariable=self.frame_overspeed_chazhi,bd=5,width=15)
        self.frame_dev_para_colorvalue.grid(row=6, column=1, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)

        self.frame_dev_para_color = Label(self.window_setpara,text="缺省时间汇报间隔：",width=10)
        self.frame_dev_para_color.grid(row=7, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_dev_para_colorvalue = Entry(self.window_setpara, textvariable=self.frame_default_time, bd=5, width=15)
        self.frame_dev_para_colorvalue.grid(row=7, column=1, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)

        self.frame_dev_para_colorexample = Label(self.window_setpara,text="{1:蓝色，2:黄色，3:黑色，4:白色，9:其他}",fg="red")
        self.frame_dev_para_colorexample.grid(row=8, column=1, ipadx=1, ipady=1, padx=5, sticky=W)


        self.frame_dev_para_set = Button(self.window_setpara,text="设    置",command=self.set_para,width=10,bd=5)
        self.frame_dev_para_set.grid(row=10, column=1, ipadx=10, ipady=5, padx=5, pady=5, sticky=W)

    def start_instant_video(self):
        pass

    def stop_instant_video(self):
        pass


