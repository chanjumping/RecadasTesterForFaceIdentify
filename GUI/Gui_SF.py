from tkinter import *
from tkinter import messagebox
import tkinter.filedialog
from Util.CommonMethod import *
import json
from Util.GlobalVar import *
from ParseModel.ParseUpgrade import *

class SFFuncWindow():
    def __init__(self,para,msg,tts,upgrade,mainwindow):
        self.frame_sf_para = para
        self.frame_sf_tts = tts
        self.frame_sf_upgrade =upgrade
        self.frame_sf_msg = msg
        self.mainwindow = mainwindow
        self.sf_FuncWindow()

    def sf_FuncWindow(self):
        self.frame_msg = StringVar()
        self.frame_flag = StringVar()
        self.frame_voice = StringVar()
        self.frame_version = StringVar()
        self.frame_bps = StringVar()
        # 终端信息
        self.frame_sf_para_querypara = Button(self.frame_sf_para,text="查询参数",command=self.query_para,bd=5,width=10)
        self.frame_sf_para_querypara.grid(row=0,column=0,ipadx=20,ipady=5,padx=20,pady=10,sticky=W)
        self.frame_sf_para_setpara = Button(self.frame_sf_para,text="【点击】设置参数",command=self.window_para,bd=5,width=10)
        self.frame_sf_para_setpara.grid(row=0,column=1,ipadx=20,ipady=5,pady=10,padx=20,sticky=W)
        self.frame_sf_attr_queryattr = Button(self.frame_sf_para,text="查询属性",command=self.query_attr,bd=5,width=10)
        self.frame_sf_attr_queryattr.grid(row=1,column=0,ipadx=20,ipady=5,pady=10,padx=20,sticky=W)
        # 构造报文
        self.frame_sf_msg_title = Label(self.frame_sf_msg,text="构造报文：")
        self.frame_sf_msg_title.grid(row=0,column=0,ipadx=20,ipady=5,padx=10,pady=5,sticky=W)
        self.frame_sf_msg_value = Entry(self.frame_sf_msg,textvariable=self.frame_msg,width=18,bd=5)
        self.frame_sf_msg_value.grid(row=0,column=1,ipadx=20,ipady=5,padx=20,pady=5,sticky=W)
        self.frame_sf_msg_example = Label(self.frame_sf_msg,text="例如：55 *** 19 84 *** 55",fg="red")
        self.frame_sf_msg_example.grid(row=1,column=1,ipadx=20,padx=5,sticky=W)
        self.frame_sf_msg_exe = Button(self.frame_sf_msg,text="发    送",command=self.send_msg,bd=5)
        self.frame_sf_msg_exe.grid(row=2,column=1,ipadx=20,ipady=5,padx=20,pady=5,sticky=W)
        # 语音播报
        self.frame_sf_tts_flag = Label(self.frame_sf_tts,text="TTS标识：")
        self.frame_sf_tts_flag.grid(row=0,column=0,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_sf_tts_flagvalue = Entry(self.frame_sf_tts,textvariable=self.frame_flag,width=18,bd=5)
        self.frame_sf_tts_flagvalue.grid(row=0,column=1,ipadx=20,ipady=5,padx=20,pady=5,sticky=W)
        self.frame_sf_tts_voice = Label(self.frame_sf_tts,text="语音内容：")
        self.frame_sf_tts_voice.grid(row=1,column=0,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_sf_tts_voicevalue = Entry(self.frame_sf_tts,textvariable=self.frame_voice,width=18,bd=5)
        self.frame_sf_tts_voicevalue.grid(row=1,column=1,ipadx=20,ipady=5,padx=20,pady=5,sticky=W)
        self.frame_sf_tts_exe = Button(self.frame_sf_tts,text="播    报",command=self.send_tts,bd=5)
        self.frame_sf_tts_exe.grid(row=2,column=1,ipadx=20,ipady=5,padx=20,pady=5,sticky=W)
        # 升级操作
        self.frame_sf_upgrade_version = Label(self.frame_sf_upgrade,text="目标版本号：")
        self.frame_sf_upgrade_version.grid(row=0,column=0,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_sf_upgrade_versionvalue = Entry(self.frame_sf_upgrade,textvariable=self.frame_version,width=18,bd=5)
        self.frame_sf_upgrade_versionvalue.grid(row=0,column=1,ipadx=20,ipady=5,padx=20,pady=5,sticky=W)
        self.frame_sf_upgrade_bps = Label(self.frame_sf_upgrade,text="分片包大小：")
        self.frame_sf_upgrade_bps.grid(row=1,column=0,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_sf_upgrade_bpsvalue = Entry(self.frame_sf_upgrade,textvariable=self.frame_bps,width=18,bd=5)
        self.frame_sf_upgrade_bpsvalue.grid(row=1,column=1,ipadx=20,ipady=5,padx=20,pady=5,sticky=W)
        self.frame_sf_upgrade_package = Label(self.frame_sf_upgrade,text="升级包：")
        self.frame_sf_upgrade_package.grid(row=2,column=0,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_sf_upgrade_select = Button(self.frame_sf_upgrade,text="选择升级包",command=self.select_package,bd=5)
        self.frame_sf_upgrade_select.grid(row=3,column=0,ipadx=10,ipady=5,padx=10,pady=5,sticky=W)
        self.frame_sf_upgrade_exe = Button(self.frame_sf_upgrade,text="升    级",command=self.start_upgrade,bd=5)
        self.frame_sf_upgrade_exe.grid(row=3,column=1,ipadx=20,ipady=5,padx=20,pady=5,sticky=W)

    # 设置参数窗口
    def window_para(self):
        self.window_setpara = Toplevel(self.mainwindow)
        self.ww = self.window_setpara.winfo_screenwidth()
        self.wh = self.window_setpara.winfo_screenheight()
        self.mw = (self.ww - 400)/2
        self.mh = (self.wh - 400)/2
        self.window_setpara.geometry("%dx%d+%d+%d" %(400,400,self.mw,self.mh))
        self.window_setpara.title("设置参数")

        self.frame_ip = StringVar()
        self.frame_port = StringVar()
        self.frame_productid = StringVar()
        self.frame_limitspeed = StringVar()
        self.frame_adasspeed = StringVar()
        self.frame_volum = StringVar()
        self.frame_mode = StringVar()

        self.frame_sf_para_ip = Label(self.window_setpara,text="IP地址：",width=10)
        self.frame_sf_para_ip.grid(row=0,column=0,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_sf_para_ipvalue = Entry(self.window_setpara,textvariable=self.frame_ip,width=17,bd=5)
        self.frame_sf_para_ipvalue.grid(row=0,column=1,ipadx=20,ipady=5,pady=5,padx=20,sticky=W)
        self.frame_sf_para_port = Label(self.window_setpara,text="端口号：",width=10)
        self.frame_sf_para_port.grid(row=1,column=0,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_sf_para_portvalue = Entry(self.window_setpara,textvariable=self.frame_port,width=17,bd=5)
        self.frame_sf_para_portvalue.grid(row=1,column=1,ipadx=20,ipady=5,pady=5,padx=20,sticky=W)
        self.frame_sf_para_productid = Label(self.window_setpara,text="产品ID：",width=10)
        self.frame_sf_para_productid.grid(row=2,column=0,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_sf_para_productvalue = Entry(self.window_setpara,textvariable=self.frame_productid,width=17,bd=5)
        self.frame_sf_para_productvalue.grid(row=2,column=1,ipadx=20,ipady=5,pady=5,padx=20,sticky=W)
        self.frame_sf_para_limitspeed = Label(self.window_setpara,text="最高速度：",width=10)
        self.frame_sf_para_limitspeed.grid(row=3,column=0,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_sf_para_limitspeedvalue = Entry(self.window_setpara,textvariable=self.frame_limitspeed,width=17,bd=5)
        self.frame_sf_para_limitspeedvalue.grid(row=3,column=1,ipadx=20,ipady=5,pady=5,padx=20,sticky=W)
        self.frame_sf_para_adasspeed = Label(self.window_setpara,text="ADAS告警速度：",width=10)
        self.frame_sf_para_adasspeed.grid(row=4,column=0,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_sf_para_adasspeedvalue = Entry(self.window_setpara,textvariable=self.frame_adasspeed,width=17,bd=5)
        self.frame_sf_para_adasspeedvalue.grid(row=4,column=1,ipadx=20,ipady=5,pady=5,padx=20,sticky=W)
        self.frame_sf_para_volum = Label(self.window_setpara,text="音量：",width=10)
        self.frame_sf_para_volum.grid(row=5,column=0,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_sf_para_volumvalue = Entry(self.window_setpara,textvariable=self.frame_volum,width=17,bd=5)
        self.frame_sf_para_volumvalue.grid(row=5,column=1,ipadx=20,ipady=5,pady=5,padx=20,sticky=W)
        self.frame_sf_para_mode = Label(self.window_setpara,text="模式：",width=10)
        self.frame_sf_para_mode.grid(row=6,column=0,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_sf_para_modevalue = Entry(self.window_setpara,textvariable=self.frame_mode,width=17,bd=5)
        self.frame_sf_para_modevalue.grid(row=6,column=1,ipadx=20,ipady=5,pady=5,padx=20,sticky=W)
        self.frame_sf_para_exe = Button(self.window_setpara,text="设    置",command=self.set_para,bd=5)
        self.frame_sf_para_exe.grid(row=7,column=1,ipadx=20,ipady=5,pady=5,padx=20,sticky=W)

    # 设置参数
    def set_para(self):
        self.ip = self.frame_ip.get()
        self.port = self.frame_port.get()
        self.productid = self.frame_productid.get()
        self.limitspeed = self.frame_limitspeed.get()
        self.adasspeed = self.frame_adasspeed.get()
        self.volum = self.frame_volum.get()
        self.mode = self.frame_mode.get()
        para_list = []
        para_dic = {}
        if self.ip:
            para_list.append({"1": self.ip})
        if self.port:
            para_list.append({"2": self.port})
        if self.productid:
            para_list.append({"3": self.productid})
        if self.limitspeed:
            para_list.append({"4": self.limitspeed})
        if self.adasspeed:
            para_list.append({"5": self.adasspeed})
        if self.volum:
            para_list.append({"6": self.volum})
        if self.mode:
            para_list.append({"7": self.mode})
        para_dic["TerminalParameter"] = para_list
        if para_dic:
            msg_body = str2hex(json.dumps(para_dic), 1024)
            service = num2big((11 << 6) + (4 << 1), 2) + calc_lens_sf(msg_body)
            timestamp = num2big(int(round(time.time() * 1000)), 8)
            pro_id = num2big(748, 2)
            other = '800000'
            body = other + timestamp + pro_id + service + msg_body
            data = '55' + '41' + calc_lens_sf(body) + body + '55'
            send_queue.put(data)
        # self.window_setpara.destroy()

    # 查询参数
    def query_para(self):
        msg_body = ''
        service = num2big((10 << 6) + (4 << 1), 2) + calc_lens_sf(msg_body)
        timestamp = num2big(int(round(time.time() * 1000)), 8)
        pro_id = num2big(748, 2)
        other = '800000'
        body = other + timestamp + pro_id + service
        data = '55' + '41' + calc_lens_sf(body) + body + '55'
        send_queue.put(data)

    # 参数结果弹窗
    def popup_querypara(para):
        messagebox.showinfo(title="终端参数",message=para)

    # 查询属性
    def query_attr(self):
        msg_body = ''
        service = num2big((12 << 6) + (4 << 1), 2) + calc_lens_sf(msg_body)
        timestamp = num2big(int(round(time.time() * 1000)), 8)
        pro_id = num2big(748, 2)
        other = '800000'
        body = other + timestamp + pro_id + service
        data = '55' + '41' + calc_lens_sf(body) + body + '55'
        send_queue.put(data)

    # 属性结果弹窗
    def popup_queryattr(attr):
        messagebox.showinfo(title="终端属性",message=attr)

    # 构造报文
    def send_msg(self):
        self.msg = self.frame_msg.get()
        send_queue.put(self.msg)

    # tts语音播报
    def send_tts(self):
        self.flag = self.frame_flag.get()
        self.tts = self.frame_sf_tts_voicevalue.get()
        if self.tts:
            msg_flag = '08'
            msg_content = byte2str(self.tts.encode('utf-8'))
            if len(msg_content) > 2048:
                msg_content = msg_content[:2048]
            else:
                n = 2048 - len(msg_content)
                msg_content += '0' * n
            msg_body = msg_flag + msg_content
            service = num2big((9 << 6) + (4 << 1), 2) + calc_lens_sf(msg_body)
            timestamp = num2big(int(round(time.time() * 1000)), 8)
            pro_id = num2big(748, 2)
            other = '800000'
            body = other + timestamp + pro_id + service + msg_body
            data = '55' + '41' + calc_lens_sf(body) + body + '55'
            send_queue.put(data)

    # 选择升级文件
    def select_package(self):
        self.upgradefile = tkinter.filedialog.askopenfilename()
        self.upgradefilename = os.path.split(self.upgradefile)[-1]
        if self.upgradefilename:
            self.frame_sf_upgrade_package.configure(text="升级包：" + self.upgradefilename)
        else:
            self.frame_sf_upgrade_package.configure(text="未选择任何升级包")

    # 执行升级
    def start_upgrade(self):
        self.version = self.frame_version.get()
        self.bps = self.frame_bps.get()
        if self.bps and self.upgradefile and self.version:
            upgrade_task_sf(self.upgradefile, self.version, int(self.bps))
