# -*- coding: utf-8 -*-
"""
Created on Sat Nov 01 21:33:02 2014

@author: HIT706
"""

import numpy as np
from  matplotlib.figure import Figure

import PIL
from PIL import Image
import cv2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Tkinter import *
import tkFileDialog as dialog
import tkMessageBox
import ttk
np.seterr(divide='ignore', invalid='ignore')
class WaterMark(object):
    def __init__(self,parent):
        self.parent = parent
        self.size = 256
        self.N = 32
        self.K = 8
        self.Key1 = np.array([1,2,3,4,5,6,7,8])
        self.Key2 = np.array([8,7,6,5,4,3,2,1])
        self.state =0
        fig = Figure()
        self.axe_1 = fig.add_subplot(221)
        self.axe_1.set_title(u'不含水印图片',fontproperties = 'STXingkai')
        self.axe_2 = fig.add_subplot(222)
        self.axe_2.set_title(u'水印图片',fontproperties = 'STXingkai')
        self.axe_3 = fig.add_subplot(223)
        self.axe_3.set_title(u'含水印图片',fontproperties = 'STXingkai')
        self.axe_4 = fig.add_subplot(224)
        self.axe_4.set_title(u'提取的水印',fontproperties = 'STXingkai')
        
        self.canvas = FigureCanvasTkAgg(fig,self.parent)
        self.canvas._tkcanvas.config(bg = 'gainsboro',highlightthickness = 0)#
        self.canvas._tkcanvas.pack(side = TOP,fill = BOTH,expand = YES,padx=0)
        self.canvas.show()
        
        
        frame = Frame(self.parent)
        frame.pack(fill = X)
        
        
        
        
        
        label = Label(frame,text = '水印图片保存为：')
        label.pack(side = LEFT)
        
        self.filename = StringVar()
        entry = Entry(frame,textvariable = self.filename)
        entry.pack(side = LEFT)
        button2 = Button(frame,text = '添加水印',command = self.insert_mark)
        button2.pack(side = LEFT)
        
        
        
        frame2 = Frame(frame)
        frame2.pack(side = RIGHT)
        button1 = Button(frame2,text = '提取水印',command = self.seperate_mark)
        button1.pack(side = LEFT,padx = 20)
        button3 = Button(frame2,text = '测试',command = self.noise_test)
        button3.pack(side = LEFT)  
        variable = [u'添加白噪声',u'高斯低通滤波']
        self.comboBox = ttk.Combobox(frame2,value = variable,width = 10)
        self.comboBox.set(u'添加白噪声')
        self.comboBox.pack(side = LEFT) 
        
        
        menubar = Menu(self.parent)
        filemenu = Menu(menubar)        
        filemenu.add_command(label = 'open',command = self.open_image)
        filemenu.add_command(label = 'open mark',command = self.open_mark)
        filemenu.add_command(label = 'open picture',command = self.open_picture)        
        menubar.add_cascade(label = 'file',menu = filemenu)        
        self.parent.config(menu = menubar)
        
        
        
        
    def open_image(self):
        self.image = dialog.askopenfilename(parent = self.parent,filetypes = [('*','*.*')],title = 'Open ')
        print self.image
        if self.image != '':
            self.image = cv2.imread(self.image.encode('gbk'))
            self.image = cv2.resize(self.image, (self.size,self.size))
            image = self.change_channals(self.image)
            self.axe_1.imshow(image)
            self.canvas.show()
        
    def open_mark(self):
        self.mark = dialog.askopenfilename(parent = self.parent,filetypes = [('*','*.*')],title = 'Open ')
      #  print type(self.mark)
        if self.mark != '':
            self.mark = cv2.imread(self.mark.encode('gbk'))
            self.mark = cv2.resize(self.mark, (self.N,self.N))
            self.axe_2.imshow(self.mark)
            self.canvas.show()
        
        
    def open_picture(self):   
        self.picture = dialog.askopenfilename(parent = self.parent,filetypes = [('*','*.*')],title = 'Open ')
        if self.picture != '':
            self.picture = cv2.imread(self.picture.encode('gbk'))
            self.picture = cv2.resize(self.picture, (self.size,self.size))
            picture = self.change_channals(self.picture)
            self.axe_3.imshow(picture)
            self.canvas.show()

        
        
    def change_channals(self,image):
        image = image
        image    = PIL.Image.fromarray(np.uint8(image))
        r,g,b = image.split()
        image = PIL.Image.merge('RGB',(b,g,r))
        return image
         
        
        
        
        
#    def image_read(self,*args,**kwargs):
#        try:
#            self.image = kwargs.pop('image')       
#        except KeyError:
#            self.image  = np.random.rand(100, 100)
#        self.axe_1.imshow(self.image)
#        self.canvas.show()
#    def mark_read(self,*args,**kwargs):
#        try:
#            self.mark = kwargs.pop('mark')       
#        except KeyError:
#            self.mark  = np.random.rand(100, 100)
#        
#        
#        self.mark = cv2.resize(self.mark, (self.N,self.N))
#        
#        self.axe_2.imshow(self.mark)
#        self.canvas.show()
        
        
    def insert_mark(self):
        if self.filename.get() == '':
            firstwarning = tkMessageBox.showwarning(message = '输入不能为空')
            
        else:
           # print self.filename.get()
            self.image = cv2.resize(self.image, (self.size,self.size))
            D = self.image.copy()
         
            
     
            alfa = 10
      
            
            for p in range(self.size/self.K):
                for q in range(self.size/self.K):
                    x=p*self.K
                    y=q*self.K
                    #print  type(D[0,0,0])
                    img_B = np.float32(D[x:x+self.K,y:y+self.K,0]) 
             
                    print 1,img_B[3,3]
                    I_dct1=cv2.dct(img_B)
             
                   
                    if self.mark[p,q,0] < 100:
                        Key  =self.Key1
                    else:
                        Key = self.Key2
            
            
                    I_dct_A = I_dct1.copy()
                    
                    I_dct_A[0,7]=I_dct1[0,7]+alfa*Key[0]
                    I_dct_A[1,6]=I_dct1[1,6]+alfa*Key[1]
                    I_dct_A[2,5]=I_dct1[2,5]+alfa*Key[2]
                    I_dct_A[3,4]=I_dct1[3,4]+alfa*Key[3]
                    I_dct_A[4,3]=I_dct1[4,3]+alfa*Key[4]
                    I_dct_A[5,2]=I_dct1[5,2]+alfa*Key[5]
                    I_dct_A[6,1]=I_dct1[6,1]+alfa*Key[6]
                    I_dct_A[7,0]=I_dct1[7,0]+alfa*Key[7]
    
                    I_dct_A = np.array(I_dct_A)          
                    I_dct_a = cv2.idct(I_dct_A)
              
                    
                    #I_dct_a = I_dct_a
                    max_point = np.max(I_dct_a)
                    min_point = np.min(I_dct_a)
                   # print max_point,I_dct_a[7,7]
                    #I_dct_a = np.uint8(I_dct_a/ max_point*255) -1
                    #I_dct_a = np.uint8(I_dct_a)
                   # print max_point,min_point,I_dct_a[3,3]
                    
                   # E[x:x+self.K,y:y+self.K,0] = I_dct_a 
                    
#                    I_dct_a=np.float32(I_dct_a-min_point+0.0001)/np.float32(max_point-min_point+0.0001)*255.0

                    D[x:x+self.K,y:y+self.K,0] = I_dct_a 
                  
                    
            
            self.picture = D
            E = D.copy()
            filename = 'watermarked/'+self.filename.get()
           #filename 路径有问题
           #could not find a writer for the specified extension in cv::imwrite_
            cv2.imwrite("image.jpg",E)
            E = self.change_channals(E)
            E = np.uint8(E)
           
            self.axe_3.imshow(E)
            self.canvas.show()
        
        
    def seperate_mark(self):
        
        self.Pmark = np.zeros((32,32,3))

        pp = np.zeros(8)
        for p in range(self.size/self.K):
            for q in range(self.size/self.K):
                x=p*self.K
                y=q*self.K
                img_B = np.float32(self.picture[x:x+self.K,y:y+self.K,0])
                
                
#                max_point = np.max(img_B)
#                min_point = np.min(img_B)
#                img_B=np.float32(img_B-min_point+0.0001)/np.float32(max_point-min_point+0.0001)*255.0
                
                I_dct1=cv2.dct(img_B)

                pp[0]=I_dct1[0,7]
                pp[1]=I_dct1[1,6]
                pp[2]=I_dct1[2,5]
                pp[3]=I_dct1[3,4]
                pp[4]=I_dct1[4,3]
                pp[5]=I_dct1[5,2]
                pp[6]=I_dct1[6,1]
                pp[7]=I_dct1[7,0]
                
                        
                if np.corrcoef(pp,self.Key1)[0][1] <= np.corrcoef(pp,self.Key2)[0][1]:
                    self.Pmark[p,q,0] = 1
                    self.Pmark[p,q,1] = 1
                    self.Pmark[p,q,2] = 1

    
        if self.state ==0:
            self.axe_4.imshow(self.Pmark)
            self.canvas.show()

        
    def whitenoise(self,image):
        image = image
        noise = 10*np.random.randn(self.size,self.size,3)
        self.WImage = image + noise
    def gaussian(self,image):
        self.WImage = cv2.GaussianBlur(image,(5,5),1.5)
    def noise_test(self):
        self.state = 1
        
        filter_name =  self.comboBox.get()
       # print filter_name
#        self.whitenoise(self.picture)
        if filter_name == u'添加白噪声':
            self.whitenoise(self.picture)
        elif filter_name == u'高斯低通滤波':
            self.gaussian(self.picture)
        
        figure = Toplevel(self.parent)
        
        fig = Figure()
        
        self.seperate_mark()
                
        canvas = FigureCanvasTkAgg(fig,figure)
        canvas._tkcanvas.config(bg = 'gainsboro',highlightthickness = 0)#
        canvas._tkcanvas.pack(side = TOP,fill = BOTH,expand = YES,padx=0)
        axe1 = fig.add_subplot(211)
        axe1.set_title(filter_name,fontproperties = 'STXingkai')
        WImage = self.change_channals(self.WImage)
        axe1.imshow(WImage)
        axe2 = fig.add_subplot(212)
        axe2.imshow(self.Pmark)
        self.state = 0
        canvas.show()
     

if __name__ == '__main__':
    
    root = Tk()
    
    watermark = WaterMark(root)

    root.mainloop()
























