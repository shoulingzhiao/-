 # -*- coding: UTF-8 -*-
import os
import shutil
import tkinter as TK
import tkinter.messagebox as Msg
from tkinter import filedialog 
import sys

# 窗口
window = TK.Tk()
window.geometry("500x400") 
window.title("Replace File") 
#window.iconbitmap('favicon.ico')


# 需要替换图片的路径名
strPathReplaceImg = TK.StringVar()
# 被替换图片的路径名
strPathBeReplaceImg = TK.StringVar()
#状态提示
strLabelStatus = TK.StringVar()

def toString(num):
    return str(num).decode("gbk")
    
def selectFileReplaceImg():
    path_ = filedialog.askdirectory()
    strPathReplaceImg.set(path_)
    
def selectBeFileReplaceImg():
    path_ = filedialog.askdirectory()
    strPathBeReplaceImg.set(path_)
    
def path_format(path):
    path = os.path.abspath(path)
    path = os.path.normpath(path)
    path = path.replace( os.path.sep, "/" )
    return path

def replace_img():
    strPathReplace = path_format(strPathReplaceImg.get())
    strPathBeReplace = path_format(strPathBeReplaceImg.get())
    
    replace_path = strPathReplace
    origin_path = os.path.join(strPathReplace, "origin_img")
    unreplace_path = os.path.join(strPathReplace, "unreplace_img")
    be_replace_path = strPathBeReplace
    
    if strPathReplaceImg.get()=="" or not os.path.exists(replace_path):
        strLabelStatus.set("没有替换目录")
        return
    if strPathBeReplaceImg.get()=="" or not os.path.exists(be_replace_path):
        strLabelStatus.set("没有被替换目录")
        return

    if not os.path.isdir(origin_path):
        os.makedirs(origin_path)

    if os.path.isdir(unreplace_path):
        shutil.rmtree(unreplace_path)
    os.makedirs(unreplace_path)
    
    tmImg = {}
    for root, _ , files in os.walk(replace_path):
        for file in files:
            tmImg[file] = os.path.join(root, file)
    
    tmImgReplace = {}
    for root, _ , files in os.walk(be_replace_path): 
        for file in files:
            if file in tmImg:
                dst_ = os.path.join(root, file)
                strLabelStatus.set("替换文件: " + file)
                dst_o = os.path.join(origin_path, file)
                if not os.path.isfile(dst_o):
                    shutil.copy2(dst_, dst_o)
                os.remove(dst_)
                shutil.copy2(tmImg[file], dst_)
                tmImgReplace[file] = file
    Msg.showinfo(title='提示', message='替换结束！')            
    strLabelStatus.set("替换结束！")
    for file in tmImg:
        if file not in tmImgReplace:
            print(u"还没有替换替换文件: " + file)
            dst_ = tmImg[file]
            dst_un = os.path.join(unreplace_path, file)
            if not os.path.isfile(dst_un):
                shutil.copy2(dst_, dst_un)
    
    print("done replace\n")


# 替换路径选择
labelReplaceImg = TK.Label(window, text='请选择替换（新文件）文件夹:').place(relx=0.1, rely=0.1,anchor='w')
inputReplaceImg = TK.Entry(window, textvariable = strPathReplaceImg, bg='white',width=48).place(relx=0.1, rely=0.16,anchor='w')
btnReplaceImg = TK.Button(window, text='浏览',width=8,command=selectFileReplaceImg).place(relx=0.8, rely=0.16,anchor='w')

# 被替换路径选择
labelBeReplaceImg = TK.Label(window, text='请选择被替换（旧文件）文件夹:').place(relx=0.1, rely=0.3,anchor='w')
inputBeReplaceImg = TK.Entry(window, textvariable = strPathBeReplaceImg, bg='white',width=48).place(relx=0.1, rely=0.36,anchor='w')
btnBeReplaceImg = TK.Button(window, text='浏览',width=8,command=selectBeFileReplaceImg).place(relx=0.8, rely=0.36,anchor='w')

# 替换按钮
btnReplace = TK.Button(window, text="替换", width=12, relief="raised",command=replace_img)
btnReplace.place(relx=0.5, rely=0.8, anchor='s')

# 提示Label
labelTip = TK.Label(window, text="注意：路径请勿包含中文", fg="red")
labelTip.place(relx=0.5, rely=1, anchor='s')

# 测试 LabelstrLabelStatus
labelStatus = TK.Label(window, textvariable=strLabelStatus, fg="#002bff")
labelStatus.place(relx=0.5, rely=0.6, anchor='center')
strStatusInit ="选择替换文件夹和被替换文件夹后，点击替换按钮开始替换"
strLabelStatus.set(strStatusInit)

window.mainloop()