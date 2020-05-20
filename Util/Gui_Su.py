from tkinter import *
from tkinter import ttk
from ParseModel.ParseUpgrade import *
import tkinter,tkinter.filedialog
import os
from Util.GetTestData import *
from Util.CommonMethod import *
from Util.GlobalVar import *
from ParseModel.Parse_SU import *
import os,shutil


class SuFuncWindow():

    def __init__(self, common, para, state, picture, daily, mode, upgrade, msg):
        self.frame_su_common = common
        self.frame_su_para = para
        self.frame_su_state = state
        self.frame_su_picture = picture
        self.frame_su_daily = daily
        self.frame_su_mode = mode
        self.frame_su_upgrade = upgrade
        self.frame_su_msg = msg
        self.su_func_window()
        self.adas_sign = "64"
        self.dsm_sign = "65"
        self.msn = "033D"
        self.agreement_sign = "7E"
        self.certificate_for_replace = False
        self.driver_name_for_replace = False

        self.face_id_for_delete = False
        self.certificate_for_delete = False

        self.face_for_modify_mask = False
        self.certificate_for_modify_mask = False
        self.driver_name_for_modify_mask = False

        self.certificate_for_modify = False
        self.face_name_for_modify = False
        self.face_format_for_modify = False
        self.face_src_for_modify = False
        self.driver_name_for_modify = False

    def su_func_window(self):
        self.frame_start_daily = tkinter.StringVar()
        self.frame_stop_daily = tkinter.StringVar()
        # self.frame_worksign = tkinter.StringVar()
        # self.frame_standsign = tkinter.StringVar()
        self.frame_upgrade_bps =tkinter.StringVar()
        self.frame_msg = tkinter.StringVar()

        # 通用指令
        self.frame_su_common_ADAS_query = Button(self.frame_su_common,text="ADAS查询指令",command=self.adas_query,width=15,bd=5)
        self.frame_su_common_ADAS_query.grid(row=0,column=0,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_su_common_DSM_query = Button(self.frame_su_common,text="DSM查询指令",command=self.dsm_query,width=14,bd=5)
        self.frame_su_common_DSM_query.grid(row=0,column=1,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_su_common_ADAS_default = Button(self.frame_su_common,text="恢复ADAS默认参数",command=self.adas__default_para,bd=5)
        self.frame_su_common_ADAS_default.grid(row=1,column=0,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_su_common_DSM_default = Button(self.frame_su_common,text="恢复DSM默认参数",command=self.dsm_default_para,bd=5)
        self.frame_su_common_DSM_default.grid(row=1,column=1,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_su_common_ADAS_infor = Button(self.frame_su_common,text="读取ADAS基本信息",command=self.adas_infor,bd=5)
        self.frame_su_common_ADAS_infor.grid(row=2,column=0,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_su_common_DSM_infor = Button(self.frame_su_common,text="读取DSM基本信息",command=self.dsm_infor,bd=5)
        self.frame_su_common_DSM_infor.grid(row=2,column=1,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)

        # 参数操作
        self.frame_su_para_case = Label(self.frame_su_para,text="用例：")
        self.frame_su_para_case.grid(row=0,column=0,pady=15,sticky=W)
        self.frame_su_para_select = Button(self.frame_su_para,text="选择用例",command=self.select_case_file,bd=5,width=15)
        self.frame_su_para_select.grid(row=1,column=0,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_su_para_exe = Button(self.frame_su_para,text="执行用例",command=self.case_exe,bd=5,width=15)
        self.frame_su_para_exe.grid(row=1,column=1,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_su_para_ADAS = Button(self.frame_su_para,text="查询ADAS参数",command=self.adas_para_query,bd=5,width=15)
        self.frame_su_para_ADAS.grid(row=2,column=0,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_su_para_DSM = Button(self.frame_su_para,text="查询DSM参数",command=self.dsm_para_query,bd=5,width=15)
        self.frame_su_para_DSM.grid(row=2,column=1,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)

        # 外设状态
        self.frame_su_state_ADAS = Button(self.frame_su_state,text="查询ADAS工作状态",command=self.adas_work_stat,bd=5)
        self.frame_su_state_ADAS.grid(row=0,column=0,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_su_state_DSM = Button(self.frame_su_state,text="查询DSM工作状态",command=self.dsm_work_stat,bd=5)
        self.frame_su_state_DSM.grid(row=0,column=1,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)

        # 抓拍
        self.frame_su_picture_ADAS = Button(self.frame_su_picture,text="ADAS主动抓拍",command=self.adas_take_photo,bd=5,width=15)
        self.frame_su_picture_ADAS.grid(row=0,column=0,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_su_picture_DSM = Button(self.frame_su_picture,text="DSM主动抓拍",command=self.dsm_take_photo,bd=5,width=15)
        self.frame_su_picture_DSM.grid(row=0,column=1,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)

        # 日志操作
        self.frame_su_daily_start = Label(self.frame_su_daily,text="输入起始日期：",bd=5,width=10)
        self.frame_su_daily_start.grid(row=0,column=0,ipadx=20,ipady=5,pady=5,sticky=W)
        self.frame_su_daily_startcont = Entry(self.frame_su_daily,textvariable=self.frame_start_daily,bd=5,width=19)
        self.frame_su_daily_startcont.grid(row=0,column=1,ipadx=20,ipady=5,pady=5,padx=15,sticky=W)
        self.frame_su_daily_stop = Label(self.frame_su_daily,text="输入结束日期：",bd=5,width=10)
        self.frame_su_daily_stop.grid(row=1,column=0,ipadx=20,ipady=5,pady=5,sticky=W)
        self.frame_su_daily_stopcont = Entry(self.frame_su_daily,textvariable=self.frame_stop_daily,bd=5,width=19)
        self.frame_su_daily_stopcont.grid(row=1,column=1,ipadx=20,ipady=5,pady=5,padx=15,sticky=W)
        self.frame_su_daily_exe = Button(self.frame_su_daily,text="获取日志",command=self.get_log,bd=5)
        self.frame_su_daily_exe.grid(row=2,column=1,ipadx=20,ipady=5,pady=5,padx=15,sticky=W)

        # 模式操作
        self.frame_su_mode_work = Label(self.frame_su_mode,text="工作模式：",width=13)
        self.frame_su_mode_work.grid(row=0,column=0,ipadx=20,ipady=5,pady=5,sticky=W)
        girls1 = [("行车", 1), ('测试', 2), ('不修改', 3)]
        self.mode_value = tkinter.IntVar()
        self.mode_value.set(1)
        for girl, num in girls1:
            Radiobutton(self.frame_su_mode, text=girl, variable=self.mode_value, value=num).grid(row=0, column=num,
                                                                                ipadx=7, ipady=5, pady=6, sticky=W)
        girls2 = [("苏标", 1), ('陕标', 2), ('不修改', 3)]
        self.standard_value = tkinter.IntVar()
        self.standard_value.set(1)
        for girl, num in girls2:
            Radiobutton(self.frame_su_mode, text=girl, variable=self.standard_value, value=num).grid(row=1,
                                                            column=num, ipadx=7, ipady=5, pady=6, sticky=W)

        self.frame_su_mode_exe = Button(self.frame_su_mode,text="模式切换",command=self.model_change,bd=5)
        self.frame_su_mode_exe.grid(row=2,column=1,columnspan=3,ipadx=20,ipady=5,pady=5,padx=15,sticky=W)

        # 升级功能
        self.frame_su_upgrade_bps = Label(self.frame_su_upgrade,text="分片包大小：",width=10)
        self.frame_su_upgrade_bps.grid(row=0,column=0,ipadx=20,ipady=5,pady=5,sticky=W)
        self.frame_su_upgrade_bpsdata = Entry(self.frame_su_upgrade,textvariable=self.frame_upgrade_bps,bd=5,width=18)
        self.frame_su_upgrade_bpsdata.grid(row=0,column=1,ipadx=20,ipady=5,pady=5,padx=20,sticky=W)
        self.frame_su_upgrade_direct = Label(self.frame_su_upgrade,text="升级包：")
        self.frame_su_upgrade_direct.grid(row=1,column=0,columnspan=2,ipadx=20,ipady=5,pady=5,sticky=W)
        self.frame_su_upgrade_select = Button(self.frame_su_upgrade,text="选择升级包",command=self.select_upgrade_file,bd=5)
        self.frame_su_upgrade_select.grid(row=2,column=0,ipadx=10,ipady=5,pady=5,padx=5,sticky=W)
        self.frame_su_upgrade_exe = Button(self.frame_su_upgrade,text="升   级",command=self.start_upgrade,bd=5)
        self.frame_su_upgrade_exe.grid(row=2,column=1,ipadx=20,ipady=5,pady=5,padx=15,sticky=W)

        # 报文构造
        self.frame_su_msg_text = Label(self.frame_su_msg, text="构造的报文：",width=13)
        self.frame_su_msg_text.grid(row=0, column=0, ipadx=20,ipady=5,pady=5, sticky=W)
        self.frame_su_msg_cont = Entry(self.frame_su_msg, textvariable=self.frame_msg,bd=5,width=18)
        self.frame_su_msg_cont.grid(row=0, column=1, ipadx=20,ipady=5,pady=5,padx=15, sticky=W)
        self.frame_su_msg_example = Label(self.frame_su_msg,text="例如：7E *** 65 31 *** 7E",fg="red")
        self.frame_su_msg_example.grid(row=1,column=1,ipadx=20, sticky=W)
        # self.frame_su_msg_examplevalue = Label(self.frame_su_msg,text="55 *** 19 84 *** 55",fg="red")
        # self.frame_su_msg_examplevalue.grid(row=1, column=1,ipady=5,pady=5,padx=15, sticky=W)
        self.frame_su_msg_exe = Button(self.frame_su_msg, text="发   送", command=self.send_msg, bd=5)
        self.frame_su_msg_exe.grid(row=2, column=1, ipadx=20, ipady=5, pady=5,padx=15, sticky=W)

    # ADAS查询
    def adas_query(self):
        data = self.msn + self.adas_sign + "2F"
        check_code = calc_check_code(data)
        message = self.agreement_sign + check_code+ num2big(GlobalVar.get_serial_no(), 2) + data + self.agreement_sign
        send_queue.put(message)

    # DSM查询
    def dsm_query(self):
        data = self.msn + self.dsm_sign + "2F"
        check_code = calc_check_code(data)
        message = self.agreement_sign + check_code + num2big(GlobalVar.get_serial_no(), 2) + data + self.agreement_sign
        send_queue.put(message)

    # 恢复ADAS默认参数
    def adas__default_para(self):
        data = self.msn + self.adas_sign + "30"
        check_code = calc_check_code(data)
        message = self.agreement_sign + check_code + num2big(GlobalVar.get_serial_no(), 2) + data + self.agreement_sign
        send_queue.put(message)

    # 恢复DSM默认参数
    def dsm_default_para(self):
        data = self.msn + self.dsm_sign + "30"
        check_code = calc_check_code(data)
        message = self.agreement_sign + check_code + num2big(GlobalVar.get_serial_no(), 2) + data + self.agreement_sign
        send_queue.put(message)

    # 读取ADAS基本信息
    def adas_infor(self):
        data = self.msn + self.adas_sign + "32"
        check_code = calc_check_code(data)
        message = self.agreement_sign + check_code + num2big(GlobalVar.get_serial_no(), 2) + data + self.agreement_sign
        send_queue.put(message)

    # 读取DSM基本信息
    def dsm_infor(self):
        data = self.msn + self.dsm_sign + "32"
        check_code = calc_check_code(data)
        message = self.agreement_sign + check_code + num2big(GlobalVar.get_serial_no(), 2) + data + self.agreement_sign
        send_queue.put(message)

    # 查询ADAS参数
    def adas_para_query(self):
        data = self.msn + self.adas_sign + "34"
        check_code = calc_check_code(data)
        message = self.agreement_sign + check_code + num2big(GlobalVar.get_serial_no(), 2) + data + self.agreement_sign
        send_queue.put(message)

    # 查询DSM参数
    def dsm_para_query(self):
        data = self.msn + self.dsm_sign + "34"
        check_code = calc_check_code(data)
        message = self.agreement_sign + check_code + num2big(GlobalVar.get_serial_no(), 2) + data + self.agreement_sign
        send_queue.put(message)

    # 查询ADAS工作状态
    def adas_work_stat(self):
        data = self.msn + self.adas_sign + "37"
        check_code = calc_check_code(data)
        message = self.agreement_sign + check_code + num2big(GlobalVar.get_serial_no(), 2) + data + self.agreement_sign
        send_queue.put(message)

    # 查询DSM工作状态
    def dsm_work_stat(self):
        data = self.msn + self.dsm_sign + "37"
        check_code = calc_check_code(data)
        message = self.agreement_sign + check_code + num2big(GlobalVar.get_serial_no(), 2) + data + self.agreement_sign
        send_queue.put(message)

    # ADAS抓拍
    def adas_take_photo(self):
        data = self.msn + self.adas_sign + "52"
        check_code = calc_check_code(data)
        message = self.agreement_sign + check_code + num2big(GlobalVar.get_serial_no(), 2) + data + self.agreement_sign
        send_queue.put(message)

    # DSM抓拍
    def dsm_take_photo(self):
        data = self.msn + self.dsm_sign + "52"
        check_code = calc_check_code(data)
        message = self.agreement_sign + check_code + num2big(GlobalVar.get_serial_no(), 2) + data + self.agreement_sign
        send_queue.put(message)

    # 获取日志
    def get_log(self):
        self.start_daily = self.frame_start_daily.get()
        self.stop_daily = self.frame_stop_daily.get()
        if self.start_daily and self.stop_daily:
            get_log_su(self.start_daily,self.stop_daily)

    # 选择用例文件
    def select_case_file(self):
        self.casefile = tkinter.filedialog.askopenfilename()
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

    # 选择升级包
    def select_upgrade_file(self):
        self.upgradefile = tkinter.filedialog.askopenfilename()
        self.upgradefilename = os.path.split(self.upgradefile)[-1]
        if self.upgradefilename:
            self.frame_su_upgrade_direct.config(text="升级包：" + self.upgradefilename)
        else:
            self.frame_su_upgrade_direct.config(text="未选择任何升级包")

    # 执行升级
    def start_upgrade(self):
        self.fragment = self.frame_upgrade_bps.get()
        if self.fragment and self.upgradefile:
            upgrade_su(self.upgradefile, int(self.fragment))

    # 模式切换
    def model_change(self):
        self.workesign = self.mode_value.get()
        if self.workesign == 1:
            self.workesign = '00'
        elif self.workesign == 2:
            self.workesign = '02'
        elif self.workesign == 3:
            self.workesign = 'FF'
        self.standsign = self.standard_value.get()
        if self.standsign == 1:
            self.standsign = '00'
        elif self.standsign == 2:
            self.standsign = '01'
        elif self.standsign == 3:
            self.standsign = 'FF'
        data = self.msn + self.dsm_sign + "EF" + self.workesign + self.standsign
        check_code = calc_check_code(data)
        message = self.agreement_sign + check_code + num2big(GlobalVar.get_serial_no(), 2) + data + self.agreement_sign
        send_queue.put(message)

    # 构造报文
    def send_msg(self):
        msg = self.frame_msg.get()
        send_queue.put(msg)