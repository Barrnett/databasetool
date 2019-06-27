#!C:\Program Files\Python3.7.3
#coding=utf-8
import tkinter
import pymysql
import tkinter.messagebox
import socket,struct
import paramiko
from tkinter import filedialog

class Tckr(object):
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("批量生成工具")
        self.root.geometry("450x300")
        self.root.configure(background='#B0E0E6')
        self.lable1 = tkinter.Label(self.root,text="设备IP：",bg = "#B0E0E6")
        self.lable2 = tkinter.Label(self.root,text="设备密码：",bg = "#B0E0E6")
        self.lable3 = tkinter.Label(self.root,text="vty.ipaddr：",bg = "#B0E0E6")
        self.lable4 = tkinter.Label(self.root,text="maineth个数:",bg = "#B0E0E6")
        self.lable5 = tkinter.Label(self.root,text="switcheth个数:",bg = "#B0E0E6")
        self.input1 = tkinter.Entry(self.root,width=30)
        self.input2 = tkinter.Entry(self.root,width=30)
        self.input2['show']='*'    #界面密码加密
        self.input3 = tkinter.Entry(self.root,width=30)
        self.input4 = tkinter.Entry(self.root,width=30)
        self.input5 = tkinter.Entry(self.root,width=30)
        self.button_begin = tkinter.Button(self.root,text = "开始生成",command = self.jisuan ,width = 10,bg = "#B0E0E6")

    def buju(self):
        self.lable1.place(x=60, y= 30)
        self.lable2.place(x=60, y= 60)
        self.lable3.place(x=60, y= 90)
        self.lable4.place(x=60, y= 120)
        self.lable5.place(x=60, y= 150)
        self.input1.place(x=150, y=30)
        self.input2.place(x=150, y=60)
        self.input3.place(x=150, y= 90)
        self.input4.place(x=150, y=120)
        self.input5.place(x=150, y=150)
        self.button_begin.place(x=160, y=225)

    def jisuan(self):
        host = self.input1.get()
        password = self.input2.get()
        ip = self.input3.get()
        maineth = self.input4.get()
        switcheth = self.input5.get()
        conn = connectsql(host,password)
        try:
            charu(conn)
            charushuju(conn,maineth)
            charushujuswitch(conn,switcheth)
            eqinfor(conn,ip)
            charudiceng(conn,ip)
            conn.commit()
            conn.close()
 #           createYuan(host)
            tkinter.messagebox._show(title="成功",message="成功！！")
        except Exception as e:
            print(e)
            tkinter.messagebox._show(title="错误",message="失败！！")

#连接数据库
def connectsql(host,password):
    try:
        conn = pymysql.connect(host=host, port=3306, user="root", password=password)
        print("connection success!")
        return conn
    except Exception as e:
        print(e)

def charu(conn):
    print('begin input')
    file_path = filedialog.askopenfilename()  #获取sql文件路径
    cursor = conn.cursor()
    cursor.execute('drop database if exists tckr')
    cursor.execute("create database tckr")
    cursor.execute('use tckr')
     ##读取SQL文件,获得sql语句的list
    with open(file_path, encoding='utf-8',errors='ignore') as f:
        sql_list = f.read().split(';')[:-1]                                         # sql文件最后一行加上;
 #      sql_list = [x.replace('\n', ' ') if '\n' in x else x for x in sql_list]     # 将每段sql里的换行符改成空格;没用？？？？
    ##执行sql语句，使用循环执行sql语句
    for sql_item in sql_list:
        cursor.execute(sql_item)
    cursor.close()
    print('input success')

#插入数据表maineth中的内容
def charushuju(conn,maineth):
    print('begin input maineth')
    cursor = conn.cursor()
    for i in range(int(maineth)):
        k = i+1
        cursor.execute("INSERT INTO `maineth` VALUES ('{id_}','{eth_}' ,'{lan_}' , '1', 'no')".format(id_=str(k),eth_="eth"+str(i),lan_="LAN"+str(k)))

#插入数据表switcheth中的内容
def charushujuswitch(conn,switcheth):
    print('begin input switcheth')
    cursor = conn.cursor()
    for i in range(int(switcheth)):
        k = i+1
        m = k + 100
        cursor.execute("INSERT INTO `switcheth` VALUES ('{id_}','{eth_}','{lan_}' , '{num_}', 'no','{index_}')".format(id_=str(m),eth_="ge"+str(k),lan_="slot"+str(k),num_=str(m),index_=str(k)))

def ip2long(ip):
    #将一个字符串IP地址转换为一个32位的网络序列IP地址
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]

#插入数据表ip中的内容
def charudiceng(conn,ip):
    try:
        cursor = conn.cursor()
        gatewayb = ip2long(ip)+1
        gateway = socket.inet_ntoa(struct.pack('!L', gatewayb))
        cursor.execute("INSERT INTO `intravty` VALUES ('eth4', '{ipaddr_}', '255.255.255.252', '{gateway_}')".format(ipaddr_=ip,gateway_=str(gateway)))
        cursor.execute("INSERT INTO `intranet` VALUES ('eth5', '172.20.0.1', '255.255.255.0', '172.20.0.2')")
        lable = ip2long(ip) + 3
        for i in range(251):
            lableip = lable + i
            cursor.execute("INSERT INTO `labelslave` VALUES ('{lable_}', '0')".format(lable_=lableip))
    except Exception as e:
        print(e)

def eqinfor(conn,ip):
    try:
        long1 = ip2long(ip)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO `eqinfo` VALUES ('1', '2', 'tckr', '1234', 'tckr', '0', '1.0',%d, '0', '0','0','0','0','0')"%long1)
    except Exception as e:
        print(e)

#def createYuan(host):
#    ssh = paramiko.SSHClient()
#    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#    ssh.connect(host,22,"root","tckrno1")
#    ssh.exec_command('mysqldump -uroot -p123456 tckr > /home/tckr.sql')

if __name__ == '__main__':
    t = Tckr()
    t.buju()
    tkinter.mainloop()
