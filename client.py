# -*- coding: utf-8 -*-

from ftplib import FTP

import time,tarfile,os
import sys
if len(sys.argv)==2:port=int(sys.argv[1])
else:port=2121
#连接ftp

def ftpconnect(host,port, username, password):

    ftp = FTP()

    # 打开调试级别2，显示详细信息

    # ftp.set_debuglevel(2)

    ftp.connect(host, port)

    ftp.login(username, password)
    return ftp

ftp = ftpconnect("192.168.0.163", port,"admin"+str(port), "444")
#从ftp下载文件

def downloadfile(remotepath, localpath):
    # 设置的缓冲区大小
    bufsize = 1024

    fp = open(localpath, 'wb')

    ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)

    ftp.set_debuglevel(0)# 参数为0，关闭调试模式

    fp.close()

#从本地上传文件到ftp

def uploadfile(remotepath, localpath):

    bufsize = 1024

    fp = open(localpath, 'rb')

    ftp.storbinary('STOR ' + remotepath, fp, bufsize)

    ftp.set_debuglevel(0)

    fp.close()
def listdir():
    return {a:b for a,b in ftp.mlsd()}
def ls(cmd):
    if len(cmd)==2:
        # print(ftp.nlst())
        ftp.dir()
        # for i in ftp.mlsd():print(i)
    else:
        print('error')
def post(cmd):
    a=cmd[4:].strip()
    if not os.path.exists(a):
        print('error');return
    if os.path.isfile(a):
        uploadfile(os.path.basename(a),a)
    else:
        postall(a)
def get(cmd):
    a=cmd[3:].strip()
    if a not in ftp.nlst():print('error');return
    if listdir()[a]['type']=='file':
        downloadfile(a,"./down/"+os.path.basename(a))
    else:
        os.chdir("./down/")
        getall(a)
        os.chdir("..")
    # if a in files:
    #     print(os.path.abspath("./down/"+os.path.basename(a)))
    #     downloadfile(a,"./down/"+os.path.basename(a))
    #     print('???')
    # else:
    #     print('error')
def cd(cmd):
    a=cmd[2:].strip()
    if a[0]!='/':ftp.cwd(os.path.join(ftp.pwd(),a))
    else:ftp.cwd(a)
def rm(cmd):
    a=cmd[2:].strip()
    files=listdir()
    if a not in files:
        print('error')
    elif files[a]['type']=='file':
        ftp.delete(a)
    else:
        ftp.rmd(a)
    # ftp.rmd(a)  # 删除远程目录
def mkdir(cmd):
    a=cmd[5:].strip()
    ftp.mkd(a)# 新建远程目录
def postall(path):
    t=os.path.basename(path)
    if t not in ftp.nlst():mkdir('mkdir'+t)
    cd('cd'+t)
    for i in os.listdir(path):
        a=os.path.join(path,i)
        if os.path.isfile(a):uploadfile(os.path.basename(a),a)
        else:postall(a)
    cd('cd ..')
def getall(t):
    if t not in os.listdir():
        os.mkdir(t)
    os.chdir(t);cd('cd'+t)
    for a,j in ftp.mlsd():
        if j['type']=='file':downloadfile(a,a)
        else:getall(a)
    os.chdir('..');cd('cd ..')
def test():
    #host,port, username, password

    ftp = ftpconnect("192.168.0.168", 2121,"admin", "444")

    #下载文件，第一个是ftp服务器路径下的文件，第二个是要下载到本地的路径文件

    downloadfile(r"12.mp3", r"D:\tmp\pytest\down\test.mp3")

    # 上传文件，第一个是要上传到ftp服务器路径下的文件，第二个是本地要上传的的路径文件

    uploadfile('/upload/1.txt', r"D:\tmp\pytest\up\1.txt")

    # ftp.close() #关闭ftp

    # #调用本地播放器播放下载的视频

    # os.system('start D:\soft\kugou\KGMusic\KuGou.exe C:\Users\Administrator\Desktop\ftp\test.mp3')

    print(ftp.getwelcome())# 打印出欢迎信息

    # 获取当前路径

    pwd_path = ftp.pwd()

    print("FTP当前路径:", pwd_path)

    # 显示目录下所有目录信息

    # ftp.dir()

    # 设置FTP当前操作的路径

    ftp.cwd('/upload/')

    # 返回一个文件名列表

    filename_list = ftp.nlst()

    print(filename_list)

    ftp.mkd('目录名')# 新建远程目录

    ftp.rmd('目录名')  # 删除远程目录

    ftp.delete('文件名')  # 删除远程文件

    ftp.rename('fromname', 'toname')  # 将fromname修改名称为toname

    # 逐行读取ftp文本文件

    file = '/upload/1.txt'

    # ftp.retrlines('RETR %s' % file)

    #与 retrlines()类似，只是这个指令处理二进制文件。回调函数 cb 用于处理每一块（块大小默认为 8KB）下载的数据

    # ftp.retrbinary('RETR %s' % file) 
    pass

def main():
    cmd='1'
    while True:
        cmd=input(">>> ").strip()
        if cmd.startswith("ls"):
            ls(cmd)
        elif cmd.startswith("post"):
            post(cmd)
        elif cmd.startswith("get"):
            get(cmd)
            # a=cmd[2:].split()
            # downloadfile(a,"./down/"+os.path.basename(a))
        elif cmd.startswith("mkdir"):
            mkdir(cmd)
        elif cmd.startswith("rm"):
            rm(cmd)
        elif cmd.startswith("cd"):
            cd(cmd)
        elif cmd in ['quit','exit','quit()','exit()']:
            break
        else:
            print('error')
        
if __name__ == "__main__":
    # test()
    main()
        