# import threading
import time
from tkinter import messagebox
import helper as helper
import utils_rotate as utils_rotate
import PySimpleGUI as sg
import cv2
import numpy as np
import torch.hub
# import cvzone
# from cvzone.SelfiSegmentationModule import SelfiSegmentation
# import glob
# import matplotlib.pyplot as plt
import pytesseract
import datetime
import os
import tkinter as tk
import shutil
from PIL import ImageTk, Image
# import imutils
from tkinter import ttk
import face_recognition
import xlsxwriter
import serial


def main():
    global count, dem, countout, iffalse, item
    dem = 0
    count = 0
    countout = 0
    iffalse = 0
    item = 0
    #rduinoUnoSerial = serial.Serial('COM3', 115200)  # create Serial object *REMEMBER to check the number of COM
    print("SMART MOTORBIKE PARKING SYSTEM")
    # yolo_LP_detect = torch.hub.load('yolov5', 'custom', path='model/LP_detector.pt', force_reload=True,
    # source='local')
    yolo_license_plate = torch.hub.load(r'D:\Python\CUSTOMDATA\yolov5', 'custom',
                                        path=r'D:\Python\CUSTOMDATA\model\LP_ocr.pt', force_reload=True, source='local')
    yolo_license_plate.conf = 0.60
    # model = torch.hub.load('ultralytics/yolov5', 'custom', path='Plate_Face_best (9).pt', force_reload=True)
    model = torch.hub.load(r'D:\Python\CUSTOMDATA\yolov5', 'custom',
                           path=r'D:\Python\CUSTOMDATA\model\Plate_Face_best (10).pt', force_reload=True,
                           source='local')
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    windows = tk.Tk()
    windows.geometry('480x640')
    windows.resizable(width=False, height=False)
    windows.title('SIGN IN')
    #icon = tk.PhotoImage(file=r"D:\Python\CUSTOMDATA\logo.png")
    #windows.iconphoto(True, icon)

    # -------------------------------------------------MAIN PAGE-------------------------------------------------------
    def root_page():
        global pre_timeframe, new_timeframe
        windows.title('SMART MOTORBIKE PARKING SYSTEM')
        # RESET FOLDER WHEN STARTING
        shutil.rmtree(r'D:\Python\CUSTOMDATA\License plate', ignore_errors=True)
        shutil.rmtree(r'D:\Python\CUSTOMDATA\Face', ignore_errors=True)
        shutil.rmtree(r'D:\Python\CUSTOMDATA\License plate out', ignore_errors=True)
        shutil.rmtree(r'D:\Python\CUSTOMDATA\Face out', ignore_errors=True)
        outWorkbook = xlsxwriter.Workbook("Datamotoparking.xlsx")
        outSheet = outWorkbook.add_worksheet()
        outSheet.write("A1", "STT")
        outSheet.write("B1", "ID face in")
        outSheet.write("C1", "ID License plate in")
        outSheet.write("D1", "TIME check in")
        outSheet.write("G1", "ID face out")
        outSheet.write("H1", "ID License plate out")
        outSheet.write("J1", "TIME check out")
        pre_timeframe = 0
        new_timeframe = 0

        print('start')

        def menu_task():
            def about():
                about_page()

            def setting():
                setting_page()

            menubar = tk.Menu(windows)
            file_menu = tk.Menu(menubar, tearoff=0)
            file_menu.add_command(label='Edit')
            file_menu.add_command(label='Manager')
            file_menu.add_command(label='Caliption')
            file_menu.add_command(label='Setting', command=setting)
            file_menu.add_command(label='About', command=about)
            file_menu.add_separator()
            file_menu.add_command(label='Exit', command=windows.quit)
            menubar.add_cascade(label='File', menu=file_menu)
            windows.config(menu=menubar)

        menu_task()

        def bg_root():
            global img_bg_root
            img_bg_root = tk.PhotoImage(file=r'D:\Python\CUSTOMDATA\image setting\backgroung.png')
            bg_root_label = tk.Label(windows, image=img_bg_root)
            bg_root_label.place(x=0, y=0, relwidth=1, relheight=1)

        bg_root()

        def root_frame():
            root = tk.Frame(windows, bg='light blue')
            root.pack(expand=True)
            # --------------------------------------------------TOP FRAME-----------------------------------------
            root_top = tk.Frame(root, height=100, width=1920, bg='light blue')
            root_top.pack()

            def title_main():
                def date_time():
                    s_time = datetime.datetime.now().strftime('%H:%M:%S, %d-%m-%Y')
                    s_time = f'{s_time}'
                    time_lb.config(text=s_time)
                    time_lb.after(100, date_time)

                time_lb = tk.Label(root_top, bg='light blue', font=('Bold', 15))
                time_lb.pack()
                date_time()
                title_frame = tk.Frame(root_top)
                title_frame.pack()
                lb_title_main = tk.Label(title_frame, text='SMART MOTORBIKE PARKING SYSTEM',
                                         font=('arial', 35), fg='blue', bg='light blue', width=60)
                lb_title_main.pack()

            title_main()

            def signout_btn():
                def sign_out():
                    windows.geometry('480x640')
                    root.destroy()
                    root_top.destroy()
                    root_mid.destroy()
                    root_bot.destroy()
                    shutil.rmtree(r'D:\Python\CUSTOMDATA\License plate', ignore_errors=True)
                    shutil.rmtree(r'D:\Python\CUSTOMDATA\Face', ignore_errors=True)
                    shutil.rmtree(r'D:\Python\CUSTOMDATA\License plate out', ignore_errors=True)
                    shutil.rmtree(r'D:\Python\CUSTOMDATA\Face out', ignore_errors=True)
                    signin_page()
                    try:
                        cap_face.release()
                        cap_plate.release()
                        cap_faceout.release()
                        cap_plateout.release()
                    except:
                        pass

                btn_signout = tk.Button(root_top, text='SIGN OUT', font=('arial', 10), bg='red', fg='white',
                                        activebackground='#FF3366', activeforeground='black', border=1, width=10,
                                        command=sign_out)
                btn_signout.place(x=0, y=0)

            signout_btn()

            # ---------------------------------------------------BUTTON SELLECT CAMERA--------------------------
            def button_camera():

                def choose_cam():
                    show_camera = tk.Toplevel(windows)
                    show_camera.geometry('800x350')
                    show_camera.title('Choose Camera')

                    def sellect_cam():

                        def radio_btn():
                            valueface = tk.StringVar()
                            chooseface = tk.Radiobutton(show_camera, text='Choose Camera', variable=valueface,
                                                        value='passed')
                            chooseface.place(x=10, y=10)

                            value_faceout = tk.StringVar()
                            choosefaceout = tk.Radiobutton(show_camera, text='Choose Camera', variable=value_faceout,
                                                           value='passed')
                            choosefaceout.place(x=410, y=10)

                            value_plate = tk.StringVar()
                            chooseplate = tk.Radiobutton(show_camera, text='Choose Camera', variable=value_plate,
                                                         value='passed')
                            chooseplate.place(x=10, y=185)

                            value_plateout = tk.StringVar()
                            chooseplateout = tk.Radiobutton(show_camera, text='Choose Camera', variable=value_plateout,
                                                            value='passed')
                            chooseplateout.place(x=410, y=185)

                        radio_btn()

                        def sellect():
                            global frame_check_cam_faceout, frame_check_cam_plateout, frame_check_cam_face, frame_check_cam_plate
                            frame_check_cam_faceout = tk.Frame(show_camera, height=100, width=130, bg='light gray')
                            frame_check_cam_faceout.place(x=640, y=25)
                            frame_check_cam_plateout = tk.Frame(show_camera, height=100, width=130, bg='light gray')
                            frame_check_cam_plateout.place(x=640, y=200)
                            frame_check_cam_face = tk.Frame(show_camera, height=100, width=130, bg='light gray')
                            frame_check_cam_face.place(x=240, y=25)
                            frame_check_cam_plate = tk.Frame(show_camera, height=100, width=130, bg='light gray')
                            frame_check_cam_plate.place(x=240, y=200)

                            # --------------------------------------------------CHOOSE FACE OUT--------------
                            def close_frame_check_faceout():
                                global frame_check_cam_faceout, cap_check_faceout
                                cap_check_faceout.release()

                            def getvalue_faceout():
                                global frame_check_cam_faceout, cap_check_faceout, value_faceout, choose_faceout
                                value_faceout = choose_faceout.get()
                                value_faceout = int(value_faceout)
                                cap_check_faceout = cv2.VideoCapture(value_faceout)

                                def cam_check_faceout():
                                    lb_check_faceout = tk.Label(frame_check_cam_faceout, text=f'{value_faceout}',
                                                                font=('arial', 20))
                                    lb_check_faceout.place(x=0, y=0)

                                    def show_check_faceout():
                                        _, frame_faceout = cap_check_faceout.read()
                                        frame_faceout = cv2.cvtColor(frame_faceout, cv2.COLOR_BGR2RGB)
                                        frame_faceout = Image.fromarray(frame_faceout).resize((130, 100))
                                        frame_faceout = ImageTk.PhotoImage(frame_faceout)
                                        lb_check_faceout.configure(image=frame_faceout)
                                        lb_check_faceout.image = frame_faceout
                                        lb_check_faceout.update()
                                        lb_check_faceout.after(15, show_check_faceout())

                                    show_check_faceout()

                                cam_check_faceout()

                            # -----------------------------------------------CHOOSE CAMERA PLATE OUT--------------
                            def close_frame_check_plateout():
                                global frame_check_cam_plateout, cap_check_plateout
                                cap_check_plateout.release()

                            def getvalue_plateout():
                                global frame_check_cam_plateout, cap_check_plateout, value_plateout, choose_plateout
                                value_plateout = choose_plateout.get()
                                value_plateout = int(value_plateout)
                                cap_check_plateout = cv2.VideoCapture(value_plateout)

                                def cam_check_plateout():
                                    lb_check_plateout = tk.Label(frame_check_cam_plateout, text=f'{value_plateout}',
                                                                 font=('arial', 20))
                                    lb_check_plateout.place(x=0, y=0)

                                    def show_check_plateout():
                                        _, frame_plateout = cap_check_plateout.read()
                                        frame_plateout = cv2.cvtColor(frame_plateout, cv2.COLOR_BGR2RGB)
                                        frame_plateout = Image.fromarray(frame_plateout).resize((130, 100))
                                        frame_plateout = ImageTk.PhotoImage(frame_plateout)
                                        lb_check_plateout.configure(image=frame_plateout)
                                        lb_check_plateout.image = frame_plateout
                                        lb_check_plateout.update()
                                        lb_check_plateout.after(17, show_check_plateout())

                                    show_check_plateout()

                                cam_check_plateout()

                            # ----------------------------------------------CHOOSE CAMERA FACE IN-------------
                            def close_frame_check_plate():
                                global frame_check_cam_plate, cap_check_plate
                                cap_check_plate.release()

                            def getvalueface():
                                global frame_check_cam_face, cap_check_face, valueface
                                valueface = choose_face.get()
                                valueface = int(valueface)
                                cap_check_face = cv2.VideoCapture(valueface)

                                def cam_check_face():
                                    lb_check_face = tk.Label(frame_check_cam_face, text=f'{valueface}',
                                                             font=('arial', 20))
                                    lb_check_face.place(x=0, y=0)

                                    def show_check_face():
                                        _, frame = cap_check_face.read()
                                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                        frame = Image.fromarray(frame).resize((130, 100))
                                        frame = ImageTk.PhotoImage(frame)
                                        lb_check_face.configure(image=frame)
                                        lb_check_face.image = frame
                                        lb_check_face.update()
                                        lb_check_face.after(14, show_check_face())

                                    show_check_face()

                                cam_check_face()

                            # ---------------------------------------------CHOOSE CAMERA PLATE--------------
                            def close_frame_check_face():
                                global frame_check_cam_plate, cap_check_plate
                                cap_check_plate.release()

                            def getvalue_plate():
                                global frame_check_cam_plate, cap_check_plate, value_plate
                                value_plate = choose_plate.get()
                                value_plate = int(value_plate)
                                cap_check_plate = cv2.VideoCapture(value_plate)

                                def cam_check_plate():
                                    lb_check_plate = tk.Label(frame_check_cam_plate, text=f'{value_plate}',
                                                              font=('arial', 20))
                                    lb_check_plate.place(x=0, y=0)

                                    def show_check_plate():
                                        _, frame_plate = cap_check_plate.read()
                                        frame_plate = cv2.cvtColor(frame_plate, cv2.COLOR_BGR2RGB)
                                        frame_plate = Image.fromarray(frame_plate).resize((130, 100))
                                        frame_plate = ImageTk.PhotoImage(frame_plate)
                                        lb_check_plate.configure(image=frame_plate)
                                        lb_check_plate.image = frame_plate
                                        lb_check_plate.update()
                                        lb_check_plate.after(16, show_check_plate())

                                    show_check_plate()

                                cam_check_plate()

                            # ----------------------------------------------------BUTTON CHECK---------------
                            def combobox():
                                global choose_face, choose_plate, choose_faceout, choose_plateout
                                Camera_sellect_face = [0, 1, 2, 3, 4, 5, 6, '...']
                                Camera_sellect_faceout = [0, 1, 2, 3, 4, 5, 6, '...']
                                Camera_sellect_plate = [0, 1, 2, 3, 4, 5, 6, '...']
                                Camera_sellect_plateout = [0, 1, 2, 3, 4, 5, 6, '...']
                                choose_face = ttk.Combobox(show_camera, values=Camera_sellect_face, width=10)
                                choose_face.place(x=15, y=40)
                                choose_face.set(0)
                                choose_plate = ttk.Combobox(show_camera, values=Camera_sellect_plate, width=10)
                                choose_plate.place(x=15, y=215)
                                choose_plate.set(0)
                                choose_faceout = ttk.Combobox(show_camera, values=Camera_sellect_faceout, width=10)
                                choose_faceout.place(x=415, y=40)
                                choose_faceout.set(0)
                                choose_plateout = ttk.Combobox(show_camera, values=Camera_sellect_plateout, width=10)
                                choose_plateout.place(x=415, y=215)
                                choose_plateout.set(0)

                            combobox()

                            def btn_run():
                                btnget = tk.Button(show_camera, text='Save', font=('arial', 10),
                                                   command=close_frame_check_face)
                                btnget.place(x=170, y=35)
                                btngetout = tk.Button(show_camera, text='Save', font=('arial', 10),
                                                      command=close_frame_check_faceout)
                                btngetout.place(x=570, y=35)

                                btnget1 = tk.Button(show_camera, text='Save', font=('arial', 10),
                                                    command=close_frame_check_plate)
                                btnget1.place(x=170, y=210)
                                btngetout1 = tk.Button(show_camera, text='Save', font=('arial', 10),
                                                       command=close_frame_check_plateout)
                                btngetout1.place(x=570, y=210)

                            btn_run()

                            def btn_ok():
                                btnok = tk.Button(show_camera, text='Check', font=('arial', 10), command=getvalueface)
                                btnok.place(x=110, y=35)
                                btnokout = tk.Button(show_camera, text='Check', font=('arial', 10),
                                                     command=getvalue_faceout)
                                btnokout.place(x=510, y=35)
                                btnok1 = tk.Button(show_camera, text='Check', font=('arial', 10),
                                                   command=getvalue_plate)
                                btnok1.place(x=110, y=210)
                                btnokout1 = tk.Button(show_camera, text='Check', font=('arial', 10),
                                                      command=getvalue_plateout)
                                btnokout1.place(x=510, y=210)

                            btn_ok()

                            def btn_cancel():
                                def cancel_btn():
                                    try:
                                        show_camera.destroy()
                                        cap_check_face.release()
                                        cap_check_plate.release()
                                        cap_check_faceout.release()
                                        cap_check_plateout.release()
                                    except:
                                        pass

                                btncancel = tk.Button(show_camera, text='DONE', font=('arial', 10), command=cancel_btn)
                                btncancel.place(x=725, y=310)

                            btn_cancel()

                        sellect()

                        def radio_btn_ip():
                            chooseip = tk.StringVar()
                            chooseip = tk.Radiobutton(show_camera, text='Ip Camera', variable=chooseip, value='passed')
                            chooseip.place(x=10, y=70)
                            chooseipout = tk.StringVar()
                            chooseipout = tk.Radiobutton(show_camera, text='Ip Camera', variable=chooseipout,
                                                         value='passed')
                            chooseipout.place(x=410, y=70)

                            chooseip1 = tk.StringVar()
                            chooseip1 = tk.Radiobutton(show_camera, text='Ip Camera', variable=chooseip1,
                                                       value='passed')
                            chooseip1.place(x=10, y=245)
                            chooseipout1 = tk.StringVar()
                            chooseipout1 = tk.Radiobutton(show_camera, text='Ip Camera', variable=chooseipout1,
                                                          value='passed')
                            chooseipout1.place(x=410, y=245)

                        radio_btn_ip()

                        def entry_ip():
                            global valueface, cap_check_face
                            entry_face = tk.Entry(show_camera, font=('arial', 10))
                            entry_face.place(x=15, y=100)
                            entry_face.insert(0, 'http://192.168.1.11:4747/video')
                            entry_faceout = tk.Entry(show_camera, font=('arial', 10))
                            entry_faceout.place(x=415, y=100)
                            entry_faceout.insert(0, 'http://192.168.1.11:4747/video')

                            def get_face():
                                global valueface, cap_check_face
                                valueface = entry_face.get()
                                valueface = str(valueface)
                                cap_check_face = cv2.VideoCapture(valueface)

                                def cam_check_face():
                                    lb_check_face = tk.Label(frame_check_cam_face, text=f'{valueface}',
                                                             font=('arial', 20))
                                    lb_check_face.place(x=0, y=0)

                                    def show_check_face():
                                        _, frame = cap_check_face.read()
                                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                        frame = Image.fromarray(frame).resize((130, 100))
                                        frame = ImageTk.PhotoImage(frame)
                                        lb_check_face.configure(image=frame)
                                        lb_check_face.image = frame
                                        lb_check_face.update()
                                        lb_check_face.after(4, show_check_face())

                                    show_check_face()

                                cam_check_face()

                            btn_face = tk.Button(show_camera, text='OK', font=('arial', 10), command=get_face)
                            btn_face.place(x=175, y=95)

                            def get_faceout():
                                global value_faceout, cap_check_faceout
                                value_faceout = entry_faceout.get()
                                value_faceout = str(value_faceout)
                                cap_check_faceout = cv2.VideoCapture(value_faceout)

                                def cam_check_faceout():
                                    lb_check_faceout = tk.Label(frame_check_cam_faceout, text=f'{value_faceout}',
                                                                font=('arial', 20))
                                    lb_check_faceout.place(x=0, y=0)

                                    def show_check_faceout():
                                        _, frame_faceout = cap_check_faceout.read()
                                        frame_faceout = cv2.cvtColor(frame_faceout, cv2.COLOR_BGR2RGB)
                                        frame_faceout = Image.fromarray(frame_faceout).resize((130, 100))
                                        frame_faceout = ImageTk.PhotoImage(frame_faceout)
                                        lb_check_faceout.configure(image=frame_faceout)
                                        lb_check_faceout.image = frame_faceout
                                        lb_check_faceout.update()
                                        lb_check_faceout.after(5, show_check_faceout())

                                    show_check_faceout()

                                cam_check_faceout()

                            btn_faceout = tk.Button(show_camera, text='OK', font=('arial', 10), command=get_faceout)
                            btn_faceout.place(x=575, y=95)

                            entry_plate = tk.Entry(show_camera, font=('arial', 10))
                            entry_plate.place(x=15, y=275)
                            entry_plate.insert(0, 'http://192.168.1.11:4747/video')
                            entry_plateout = tk.Entry(show_camera, font=('arial', 10))
                            entry_plateout.place(x=415, y=275)
                            entry_plateout.insert(0, 'http://192.168.1.11:4747/video')

                            def get_plate():
                                global value_plate, cap_check_plate
                                value_plate = entry_plate.get()
                                value_plate = str(value_plate)
                                cap_check_plate = cv2.VideoCapture(value_plate)

                                def cam_check_plate():
                                    lb_check_plate = tk.Label(frame_check_cam_plate, text=f'{value_plate}',
                                                              font=('arial', 20))
                                    lb_check_plate.place(x=0, y=0)

                                    def show_check_plate():
                                        _, frame_plate = cap_check_plate.read()
                                        frame_plate = cv2.cvtColor(frame_plate, cv2.COLOR_BGR2RGB)
                                        frame_plate = Image.fromarray(frame_plate).resize((130, 100))
                                        frame_plate = ImageTk.PhotoImage(frame_plate)
                                        lb_check_plate.configure(image=frame_plate)
                                        lb_check_plate.image = frame_plate
                                        lb_check_plate.update()
                                        lb_check_plate.after(6, show_check_plate())

                                    show_check_plate()

                                cam_check_plate()

                            btnip1 = tk.Button(show_camera, text='OK', font=('arial', 10), command=get_plate)
                            btnip1.place(x=175, y=270)

                            def get_plateout():
                                global value_plateout, cap_check_plateout
                                value_plateout = entry_plateout.get()
                                value_plateout = str(value_plateout)
                                cap_check_plateout = cv2.VideoCapture(value_plateout)

                                def cam_check_plateout():
                                    lb_check_plateout = tk.Label(frame_check_cam_plateout, text=f'{value_plateout}',
                                                                 font=('arial', 20))
                                    lb_check_plateout.place(x=0, y=0)

                                    def show_check_plateout():
                                        _, frame_plateout = cap_check_plateout.read()
                                        frame_plateout = cv2.cvtColor(frame_plateout, cv2.COLOR_BGR2RGB)
                                        frame_plateout = Image.fromarray(frame_plateout).resize((130, 100))
                                        frame_plateout = ImageTk.PhotoImage(frame_plateout)
                                        lb_check_plateout.configure(image=frame_plateout)
                                        lb_check_plateout.image = frame_plateout
                                        lb_check_plateout.update()
                                        lb_check_plateout.after(7, show_check_plateout())

                                    show_check_plateout()

                                cam_check_plateout()

                            btnipout1 = tk.Button(show_camera, text='OK', font=('arial', 10), command=get_plateout)
                            btnipout1.place(x=575, y=270)

                        entry_ip()

                        def frame_check():
                            check_cam_lb = tk.Label(show_camera, text='Test Camera Face In')
                            check_cam_lb.place(x=245, y=0)
                            check_camout_lb = tk.Label(show_camera, text='Test Camera Face Out')
                            check_camout_lb.place(x=645, y=0)
                            check_cam_lb1 = tk.Label(show_camera, text='Test Camera Plate In')
                            check_cam_lb1.place(x=245, y=175)
                            check_camout_lb1 = tk.Label(show_camera, text='Test Camera Plate Out')
                            check_camout_lb1.place(x=645, y=175)

                        frame_check()

                    sellect_cam()

                    show_camera.update()

                btn_setting = tk.Button(root_top, text='Camera', font=('arial', 10), bg='green', fg='white',
                                        activebackground='light green', activeforeground='black', border=1, width=10,
                                        command=choose_cam)
                btn_setting.place(x=88, y=0)

            button_camera()

            def button_folder_Input():

                def open_folder_Input():
                    os.startfile(r'D:\Python\CUSTOMDATA\DATA SPACE Input')

                btn_help = tk.Button(root_top, text='Folder Input', font=('arial', 10), bg='green', fg='white',
                                     activebackground='light green', activeforeground='black', border=1, width=10,
                                     command=open_folder_Input)
                btn_help.place(x=176, y=0)

            button_folder_Input()

            def button_Folder_Output():

                def open_folder_Output():
                    os.startfile(r'D:\Python\CUSTOMDATA\DATA SPACE Output')

                btn_other = tk.Button(root_top, text='Folder Output', font=('arial', 10), bg='green', fg='white',
                                      activebackground='light green', activeforeground='black', border=1, width=10,
                                      command=open_folder_Output)
                btn_other.place(x=264, y=0)

            button_Folder_Output()

            def toggle_camin():
                global frame_left, frame_right, lb_face_in, lb_plate_in, valueface, value_plate

                def toggle():
                    global frame_left, frame_right, cap_face, cap_plate, valueface, value_plate
                    video_detect = r"D:\Python\CUSTOMDATA\video detect 3.mp4"
                    # ip = 'http://192.168.1.11:4747/video'
                    cap_plate = cv2.VideoCapture(value_plate)
                    cap_face = cv2.VideoCapture(valueface)
                    if sw_camin.config('relief')[-1] == 'sunken':
                        sw_camin.config(relief="raised", image=off)
                        frame_left.destroy()
                        cap_face.release()
                        cap_plate.release()
                    else:

                        sw_camin.config(relief="sunken", image=on)
                        left_frame()

                lb_camin = tk.Label(root_top, text='Camera In', font=('arial', 12),
                                    bg='light blue', fg='dark blue', border=1)
                lb_camin.place(x=0, y=30)
                on = tk.PhotoImage(file='D:\Python\CUSTOMDATA\image setting\on_sw.png')
                off = tk.PhotoImage(file='D:\Python\CUSTOMDATA\image setting\off_sw.png')
                sw_camin = tk.Button(root_top, image=off, bd=0, command=toggle, bg='light blue', border=0, width=80,
                                     height=26, activebackground='light blue', relief="raised")
                sw_camin.place(x=100, y=30)

            toggle_camin()

            def toggle_camout():
                def toggle():
                    global frame_left, frame_right, cap_faceout, cap_plateout, value_faceout, value_plateout, \
                        frame_results, frame_results_out
                    video_detect_out = r"D:\Python\CUSTOMDATA\video detect 3.mp4"
                    video_detect_faceout = r"D:\Python\CUSTOMDATA\Video Face 1.mp4"
                    ipout = 'http://192.168.1.11:4747/video'
                    cap_plateout = cv2.VideoCapture(value_plateout)
                    cap_faceout = cv2.VideoCapture(value_faceout)
                    if sw_camout.config('relief')[-1] == 'sunken':
                        sw_camout.config(relief="raised", image=off_out)
                        frame_right.destroy()
                        try:
                            frame_results.destroy()
                            frame_results_out.destroy()
                        except:
                            pass
                    else:
                        sw_camout.config(relief="sunken", image=on_out)
                        right_frame()

                lb_camout = tk.Label(root_top, text='Camera Out', font=('arial', 12),
                                     bg='light blue', fg='dark blue', border=1)
                lb_camout.place(x=0, y=60)
                on_out = tk.PhotoImage(file='D:\Python\CUSTOMDATA\image setting\on_sw.png')
                off_out = tk.PhotoImage(file='D:\Python\CUSTOMDATA\image setting\off_sw.png')
                sw_camout = tk.Button(root_top, image=off_out, bd=0, command=toggle, bg='light blue', border=0,
                                      width=80,
                                      height=26, activebackground='light blue', relief="raised")
                sw_camout.place(x=100, y=60)

            toggle_camout()

            # --------------------------------------------------MID FRAME---------------------------------------
            root_mid = tk.Frame(root, height=650, width=1920, bg='light blue')
            root_mid.pack()

            def getin_getout_frame():
                getin_lb = tk.Label(root_mid, text='ENTRANCE', width=50, font=('arial', 12), fg='red', bg='light green')
                getin_lb.place(x=0, y=0)
                getout_lb = tk.Label(root_mid, text='EXIT', width=50, font=('arial', 12), fg='red', bg='light green')
                getout_lb.place(x=770, y=0)
                ktface_lb = tk.Label(root_mid, text='Face In', font=('arial', 12),
                                     fg='black',
                                     bg='light blue')
                ktface_lb.place(x=1280, y=0)
                ktfaceout_lb = tk.Label(root_mid, text='Face Out', font=('arial', 12),
                                        fg='black', bg='light blue')
                ktfaceout_lb.place(x=1400, y=0)
                checkin_getin = tk.Label(root_mid, text='Camera Show', font=('arial', 11), fg='blue', bg='light blue')
                checkin_getin.place(x=0, y=25)
                checkout_getin = tk.Label(root_mid, text='Check In', font=('arial', 11), fg='blue', bg='light blue')
                checkout_getin.place(x=360, y=25)
                checkin_getout = tk.Label(root_mid, text='Camera Show', font=('arial', 11), fg='blue', bg='light blue')
                checkin_getout.place(x=770, y=25)
                checkout_getout = tk.Label(root_mid, text='Check Out', font=('arial', 11), fg='blue', bg='light blue')
                checkout_getout.place(x=1130, y=25)

            getin_getout_frame()

            def display_checkin_id():
                global display_plate_lb, plate_lb, display_face_lb, face_lb
                display_plate_lb = tk.Label(root_mid, text=f'', font=('arial', 10),
                                            fg='dark blue', width=12, bg='white', border=5,
                                            highlightthickness=5)
                display_plate_lb.place(x=120, y=50)
                plate_lb = tk.Label(root_mid, text='Face ID: ', font=('arial', 10), fg='black',
                                    bg='light blue')
                plate_lb.place(x=0, y=55)
                display_face_lb = tk.Label(root_mid, text=f'', font=('arial', 10),
                                           fg='dark blue', width=12, bg='white', border=5, highlightthickness=5)
                display_face_lb.place(x=120, y=95)
                face_lb = tk.Label(root_mid, text='License Plate ID: ', font=('arial', 10), fg='black',
                                   bg='light blue')
                face_lb.place(x=0, y=100)

            display_checkin_id()

            def display_checkout_id():
                global plateout_lb, display_plateout_lb, faceout_lb, display_faceout_lb
                plateout_lb = tk.Label(root_mid, text='Face ID: ', font=('arial', 10), fg='black', bg='light blue')
                plateout_lb.place(x=770, y=55)
                display_plateout_lb = tk.Label(root_mid, text='', font=('arial', 10),
                                               fg='dark blue', width=12, bg='white', border=5, highlightthickness=5)
                display_plateout_lb.place(x=890, y=50)
                faceout_lb = tk.Label(root_mid, text='License Plate ID: ', font=('arial', 10), fg='black',
                                      bg='light blue')
                faceout_lb.place(x=770, y=100)
                display_faceout_lb = tk.Label(root_mid, text='', font=('arial', 10),
                                              fg='dark blue', width=12, bg='white', border=5, highlightthickness=5)
                display_faceout_lb.place(x=890, y=95)

            display_checkout_id()

            def display_time_check():
                global time_lb_in, display_plate_in_lb, timeout_lb_in, display_plateout_in_lb
                time_lb_in = tk.Label(root_mid, text='Time Check In: ', font=('arial', 10), fg='black', bg='light blue')
                time_lb_in.place(x=360, y=55)
                display_plate_in_lb = tk.Label(root_mid, text='', font=('arial', 10),
                                               fg='dark blue', width=12, bg='white', border=5, highlightthickness=5)
                display_plate_in_lb.place(x=480, y=50)
                timeout_lb_in = tk.Label(root_mid, text='Time Check Out: ', font=('arial', 10), fg='black',
                                         bg='light blue')
                timeout_lb_in.place(x=1130, y=55)
                display_plateout_in_lb = tk.Label(root_mid, text='', font=('arial', 10),
                                                  fg='dark blue', width=12, bg='white', border=5, highlightthickness=5)
                display_plateout_in_lb.place(x=1270, y=50)

            display_time_check()

            def total():
                global total_lb, display_total_lb
                total_lb = tk.Label(root_mid, text='Total Pay: ', font=('arial', 10), fg='black',
                                    bg='light blue')
                total_lb.place(x=1130, y=95)
                display_total_lb = tk.Label(root_mid, text='', font=('arial', 10),
                                            fg='dark blue', width=12, bg='white', border=5, highlightthickness=5)
                display_total_lb.place(x=1270, y=95)

            total()

            def state():
                global checkstate_lb, display_checkstate_lb
                checkstate_lb = tk.Label(root_mid, text='State: ', font=('arial', 10), fg='black',
                                         bg='light blue')
                checkstate_lb.place(x=360, y=95)
                display_checkstate_lb = tk.Label(root_mid, text=f'', font=('arial', 10),
                                                 fg='dark blue', width=12, bg='white', border=5, highlightthickness=5)
                display_checkstate_lb.place(x=480, y=95)

            state()

            def left_frame():
                global frame_left, frame_right, lb_face_in, lb_plate_in
                frame_left = tk.Frame(root_mid, height=515, width=770, bg='#66CCFF')
                frame_left.place(x=0, y=132)
                results_face_lb = tk.Label(frame_left, bg='black', text='')
                results_face_lb.place(x=385, y=0)
                results_plate_lb = tk.Label(frame_left, bg='black', text='')
                results_plate_lb.place(x=385, y=255)

                def cam_face_in():
                    lb_face_in = tk.Label(frame_left)
                    lb_face_in.place(x=0, y=0)

                    def video_stream_face():
                        global result_frame_face, pre_timeframe, new_timeframe
                        _, frame_face = cap_face.read()
                        frame_face = cv2.cvtColor(frame_face, cv2.COLOR_BGR2RGB)
                        frame_face = Image.fromarray(frame_face).resize((385, 255))
                        frame_face = ImageTk.PhotoImage(image=frame_face)
                        lb_face_in.imgtk = frame_face
                        lb_face_in.configure(image=frame_face)
                        lb_face_in.lift()
                        lb_face_in.update()
                        lb_face_in.after(2, video_stream_face)

                    video_stream_face()

                cam_face_in()

                def cam_plate_in():
                    lb_plate_in = tk.Label(frame_left)
                    lb_plate_in.place(x=0, y=260)

                    def video_stream_plate():
                        global result_frame_plate
                        _, frame_plate = cap_plate.read()
                        frame_plate = cv2.cvtColor(frame_plate, cv2.COLOR_BGR2RGB)
                        frame_plate = Image.fromarray(frame_plate).resize((385, 255))
                        frame_plate = ImageTk.PhotoImage(image=frame_plate)
                        lb_plate_in.imgtk = frame_plate
                        lb_plate_in.configure(image=frame_plate)
                        lb_plate_in.lift()
                        lb_plate_in.update()
                        lb_plate_in.after(1, video_stream_plate)

                    video_stream_plate()

                cam_plate_in()

            def right_frame():
                global frame_left, frame_right, lb_face_out, lb_plate_out
                frame_right = tk.Frame(root_mid, height=515, width=770, bg='#66CCFF')
                frame_right.place(x=770, y=132)

                def cam_face_out():
                    lb_face_out = tk.Label(frame_right)
                    lb_face_out.place(x=0, y=0)

                    def video_stream_faceout():
                        global result_frame_faceout
                        _, frame_faceout = cap_faceout.read()
                        frame_faceout = cv2.cvtColor(frame_faceout, cv2.COLOR_BGR2RGB)
                        # result_frame_faceout = model(frame_faceout)
                        # frame_faceout = np.squeeze(result_frame_faceout.render())
                        frame_faceout = Image.fromarray(frame_faceout).resize((385, 255))
                        frame_faceout = ImageTk.PhotoImage(image=frame_faceout)
                        lb_face_out.imgtk = frame_faceout
                        lb_face_out.configure(image=frame_faceout)
                        lb_face_out.lift()
                        lb_face_out.update()
                        lb_face_out.after(7, video_stream_faceout)

                    video_stream_faceout()

                cam_face_out()

                def cam_plate_out():
                    global cap_plateout
                    lb_plate_out = tk.Label(frame_right)
                    lb_plate_out.place(x=0, y=260)

                    def video_stream_plateout():
                        global result_frame_plateout
                        _, frame_plateout = cap_plateout.read()
                        frame_plateout = cv2.cvtColor(frame_plateout, cv2.COLOR_BGR2RGB)
                        # result_frame_plateout = model(frame_plateout)
                        # frame_plateout = np.squeeze(result_frame_plateout.render())
                        frame_plateout = Image.fromarray(frame_plateout).resize((385, 255))
                        frame_plateout = ImageTk.PhotoImage(image=frame_plateout)
                        lb_plate_out.imgtk = frame_plateout
                        lb_plate_out.configure(image=frame_plateout)
                        lb_plate_out.lift()
                        lb_plate_out.update()
                        lb_plate_out.after(8, video_stream_plateout)

                    video_stream_plateout()

                cam_plate_out()

            # --------------------------------------------------BOT FRAME-----------------------------------------------------------
            # --------------------------------------------------BUTTON DETECT OUTPUT-------------------------------------------------
            root_bot = tk.Frame(root, height=50, width=1920, bg='#0000BB')
            root_bot.pack()

            def btn_detect_out():

                def varout_count():
                    global varout, countout
                    #varout = ArduinoUnoSerial.read()
                    # varout = str(varout, encoding='latin-1')
                    # varout = varout.strip('\r\n')
                    if (countout == 0):
                        try:
                            if (varout == '2'):
                                face_plate_saveout()
                        except:
                            print("WAITING OTHER MOTORBIKE OUT")
                    if (countout == 1):
                        if (varout == '3'):
                            countout = 0
                            print("WAITING OTHER MOTORBIKE OUT")
                    varout_lb.after(39, varout_count)

                varout_lb = tk.Label(root_top, bg='light blue', font=('Bold', 15))
                varout_count()

                def face_plate_saveout():
                    # RESET FOLDER WHEN STARTING
                    shutil.rmtree(r'D:\Python\CUSTOMDATA\License plate out', ignore_errors=True)
                    shutil.rmtree(r'D:\Python\CUSTOMDATA\Face out', ignore_errors=True)

                    def cam_face_out():
                        lb_face_out = tk.Label(frame_right)

                        # lb_face_out.place(x=0, y=0)

                        def video_stream_faceout():
                            global result_frame_faceout
                            _, frame_faceout = cap_faceout.read()
                            frame_faceout = cv2.cvtColor(frame_faceout, cv2.COLOR_BGR2RGB)
                            result_frame_faceout = model(frame_faceout)
                            frame_faceout = np.squeeze(result_frame_faceout.render())
                            frame_faceout = Image.fromarray(frame_faceout).resize((385, 255))
                            frame_faceout = ImageTk.PhotoImage(image=frame_faceout)
                            lb_face_out.imgtk = frame_faceout
                            lb_face_out.configure(image=frame_faceout)
                            lb_face_out.lift()
                            lb_face_out.update()

                        video_stream_faceout()

                    cam_face_out()

                    def cam_plate_out():
                        global cap_plateout
                        lb_plate_out = tk.Label(frame_right)

                        # lb_plate_out.place(x=0, y=260)

                        def video_stream_plateout():
                            global result_frame_plateout
                            _, frame_plateout = cap_plateout.read()
                            frame_plateout = cv2.cvtColor(frame_plateout, cv2.COLOR_BGR2RGB)
                            result_frame_plateout = model(frame_plateout)
                            frame_plateout = np.squeeze(result_frame_plateout.render())
                            frame_plateout = Image.fromarray(frame_plateout).resize((385, 255))
                            frame_plateout = ImageTk.PhotoImage(image=frame_plateout)
                            lb_plate_out.imgtk = frame_plateout
                            lb_plate_out.configure(image=frame_plateout)
                            lb_plate_out.lift()
                            lb_plate_out.update()

                        video_stream_plateout()

                    cam_plate_out()

                    crops = result_frame_plateout.crop(save=True,
                                                       save_dir=r'D:\Python\CUSTOMDATA\License plate out\License plate')
                    crops_face = result_frame_faceout.crop(save=True, save_dir=r'D:\Python\CUSTOMDATA\Face out\Face')

                    show_detect_out()

                btn_detectout = tk.Button(root_bot, text='Show Dectect', font=('arial', 15), bg='#FFFF00', fg='black',
                                          activeforeground='#FFFF66', activebackground='black', width=12,
                                          command=face_plate_saveout)
                btn_detectout.place(x=770, y=0)

            btn_detect_out()

            def show_detect_out():
                global img_plateout, img_faceout, display_plateout_lb, img_faceout_1, final_text_imgout, bill_total
                img_plateout = Image.open(
                    r'D:\Python\CUSTOMDATA\License plate out\License plate\crops\License Plate\image0.jpg')
                try:
                    img_faceout_1 = Image.open(r'D:\Python\CUSTOMDATA\Face out\Face\crops\Face\image02.jpg')
                    img_faceout_1 = img_faceout_1.resize((120, 120))
                    img_faceout_1 = ImageTk.PhotoImage(img_faceout_1)
                    detect_faceout_1 = cv2.imread(r'D:\Python\CUSTOMDATA\Face out\Face\crops\Face\image02.jpg')
                except:
                    img_faceout_1 = None

                img_faceout = Image.open(r'D:\Python\CUSTOMDATA\Face out\Face\crops\Face\image0.jpg')
                img_plateout = img_plateout.resize((385, 255))
                img_faceout = img_faceout.resize((385, 255))
                img_plateout = ImageTk.PhotoImage(img_plateout)
                img_faceout = ImageTk.PhotoImage(img_faceout)
                global final_crop_frame_plateout, final_crop_frame_faceout, text_imgout, final_img_detect_faceout, crop_frameout, threshold_2out
                detect_faceout = cv2.imread(r'D:\Python\CUSTOMDATA\Face out\Face\crops\Face\image0.jpg')
                detect_plateout = cv2.imread(
                    r'D:\Python\CUSTOMDATA\License plate out\License plate\crops\License Plate\image0.jpg')
                # LOOP CONTOURS PLATE
                platesout = model(detect_plateout, size=640)
                list_platesout = platesout.pandas().xyxy[0].values.tolist()
                list_read_platesout = set()
                if len(list_platesout) == 0:
                    text_imgout = helper.read_plate(yolo_license_plate, detect_plateout)
                    print(text_imgout)
                    if text_img != "unknown":
                        list_read_platesout.add(text_img)
                else:
                    for plateout in list_platesout:
                        flag = 0
                        x = int(plateout[0])  # xmin
                        y = int(plateout[1])  # ymin
                        w = int(plateout[2] - plateout[0])  # xmax - xmin
                        h = int(plateout[3] - plateout[1])  # ymax - ymin
                        crop_imgout = detect_plateout[y:y + h, x:x + w]
                        cv2.rectangle(detect_plateout, (int(plateout[0]), int(plateout[1])),
                                      (int(plateout[2]), int(plateout[3])),
                                      color=(0, 0, 225), thickness=2)
                        text_imgout = ""
                        for cc in range(0, 2):
                            for ct in range(0, 2):
                                text_imgout = helper.read_plate(yolo_license_plate,
                                                                utils_rotate.deskew(crop_imgout, cc, ct))
                                if text_imgout != "unknown":
                                    list_read_platesout.add(text_imgout)
                                    flag = 1
                                    break
                            if flag == 1:
                                break

                    # COUNT LETTER IN STRING
                    final_text_imgout = ''
                    for text_imgout in text_imgout:
                        if text_imgout.isalnum():
                            final_text_imgout += text_imgout
                            number_stringout = len(final_text_imgout)

                    def display_checkout_id():
                        global display_plateout_lb, plateout_lb, display_faceout_lb, faceout_lb, \
                            timeout_lb_in, display_plateout_in_lb, total_lb, display_total_lb, bill_total, \
                            frame_results, frame_results_out, ktface_lb, ktfaceout_lb

                        def destroyout_lb():
                            display_plateout_lb.destroy()
                            plateout_lb.destroy()
                            display_faceout_lb.destroy()
                            faceout_lb.destroy()
                            total_lb.destroy()
                            display_total_lb.destroy()
                            timeout_lb_in.destroy()
                            display_plateout_in_lb.destroy()
                            try:
                                frame_results.destroy()
                                frame_results_out.destroy()
                                ktface_lb.destroy()
                                ktfaceout_lb.destroy()
                            except:
                                print('No destroy face show exit!')

                        destroyout_lb()

                        def resultsout_show():
                            global results_faceoutother_lb
                            results_faceout_lb = tk.Label(frame_right, image=img_faceout)
                            results_faceout_lb.place(x=385, y=0)
                            if img_faceout_1 != None:
                                results_faceoutother_lb = tk.Label(results_faceout_lb, image=img_faceout_1)
                                results_faceoutother_lb.place(x=0, y=0)
                            if img_faceout_1 == None:
                                try:
                                    results_faceoutother_lb.destroy()
                                except:
                                    print('No other face destroy')
                            results_plateout_lb = tk.Label(frame_right, image=img_plateout)
                            results_plateout_lb.place(x=385, y=260)

                        resultsout_show()
                        global countout, stand_3out

                        if (number_stringout == 8) or (number_stringout == 9):
                            checkout = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
                            stand_2out = f'{final_text_imgout[2]}'
                            try:
                                stand_3out = [f'{final_text_imgout[0]}', f'{final_text_imgout[1]}',
                                              f'{final_text_imgout[4]}',
                                              f'{final_text_imgout[5]}',
                                              f'{final_text_imgout[6]}', f'{final_text_imgout[7]}',
                                              f'{final_text_imgout[8]}']
                            except:
                                stand_3out = [f'{final_text_imgout[0]}', f'{final_text_imgout[1]}',
                                              f'{final_text_imgout[4]}',
                                              f'{final_text_imgout[5]}',
                                              f'{final_text_imgout[6]}', f'{final_text_imgout[7]}']
                            for demout in stand_3out:
                                if (demout in checkout):
                                    stand_3out = True
                                else:
                                    stand_3out = False
                                    break
                            if (stand_2out not in checkout) & (stand_3out == True):

                                def plateout_id():
                                    display_plateout_lb.config(text=final_text_imgout)
                                    display_plateout_lb.after(100, plateout_id)

                                display_plateout_lb = tk.Label(root_mid, text=f'{final_text_imgout}',
                                                               font=('arial', 10),
                                                               fg='dark blue', width=12, bg='white', border=5,
                                                               highlightthickness=5)
                                display_plateout_lb.place(x=890, y=50)
                                plateout_lb = tk.Label(root_mid, text='Face ID: ', font=('arial', 10), fg='black',
                                                       bg='light blue')
                                plateout_lb.place(x=770, y=55)
                                plateout_id()

                                def faceout_id():
                                    display_faceout_lb.config(text=final_text_imgout)
                                    display_faceout_lb.after(100, faceout_id)

                                display_faceout_lb = tk.Label(root_mid, text=f'{final_text_imgout}', font=('arial', 10),
                                                              fg='dark blue', width=12, bg='white', border=5,
                                                              highlightthickness=5)
                                display_faceout_lb.place(x=890, y=95)
                                faceout_lb = tk.Label(root_mid, text='License Plate ID: ', font=('arial', 10),
                                                      fg='black',
                                                      bg='light blue')
                                faceout_lb.place(x=770, y=100)
                                faceout_id()

                                def date_timeout():
                                    s_timeout = datetime.datetime.now().strftime('%H:%M, %d-%m-%Y')
                                    s_timeout = f'{s_timeout}'
                                    display_plateout_in_lb.config(text=s_timeout)

                                timeout_lb_in = tk.Label(root_mid, text='Time Check Out: ', font=('arial', 10),
                                                         fg='black',
                                                         bg='light blue')
                                timeout_lb_in.place(x=1130, y=55)
                                display_plateout_in_lb = tk.Label(root_mid, text='', font=('arial', 10),
                                                                  fg='dark blue', width=12, bg='white', border=5,
                                                                  highlightthickness=5)
                                display_plateout_in_lb.place(x=1270, y=50)
                                date_timeout()

                                def save_resultsout():
                                    global bill_total

                                    def createFolderout(dicret):
                                        try:
                                            if not os.path.exists(dicret):
                                                os.makedirs(dicret)
                                        except OSError:
                                            print('No creating folder')

                                    createFolderout(f'D:\Python\CUSTOMDATA\DATA SPACE Output\{final_text_imgout}')
                                    s_timeout = datetime.datetime.now().strftime('(%d-%m, %Hh %Mm)')
                                    s_timeout_ID = datetime.datetime.now().strftime('(%d-%m-%Y, %Hh %Mm)')
                                    s_timeout = f'{s_timeout}'
                                    s_timeout_ID = f'{s_timeout_ID}'
                                    file_name_plate = f'D:\Python\CUSTOMDATA\DATA SPACE Output\{final_text_imgout}\License plate_{final_text_imgout}.png'
                                    cv2.imwrite(file_name_plate, detect_plateout)
                                    file_name_face = f'D:\Python\CUSTOMDATA\DATA SPACE Output\{final_text_imgout}\Face_{final_text_imgout}.png'
                                    cv2.imwrite(file_name_face, detect_faceout)
                                    if img_faceout_1 != None:
                                        file_name_face_1 = f'D:\Python\CUSTOMDATA\DATA SPACE Output\{final_text_imgout}\Face_{final_text_imgout}_(1).png'
                                        cv2.imwrite(file_name_face_1, detect_faceout_1)
                                    ID = f'{final_text_imgout}_{s_timeout_ID}'
                                    f = open(
                                        f'D:\Python\CUSTOMDATA\DATA SPACE Output\{final_text_imgout}\ID {final_text_imgout}.txt',
                                        'a')
                                    f.write('ID ')
                                    f.write(ID + '\n')
                                    f.close()

                                save_resultsout()

                                def face_re():
                                    global bill_total, frame_results, frame_results_out, results_encoding, results_encodingout, countout, iffalse
                                    folder_path = f'D:\Python\CUSTOMDATA\DATA SPACE Input\{final_text_imgout}'
                                    path_list = os.listdir(folder_path)
                                    img_list = []
                                    faceids = []

                                    for path in path_list:
                                        img = face_recognition.load_image_file(os.path.join(folder_path, path))
                                        height, width, _ = img.shape
                                        face_location = (0, width, height, 0)
                                        encodings = face_recognition.face_encodings(img, known_face_locations=[
                                            face_location])
                                        if len(encodings) > 0:
                                            results_encoding = encodings[0]
                                        else:
                                            print("No faces found in the image!")
                                            quit()

                                        imgout = face_recognition.load_image_file(
                                            f'D:\Python\CUSTOMDATA\DATA SPACE Output\{final_text_imgout}\Face_{final_text_imgout}.png')
                                        heightout, widthout, _ = imgout.shape
                                        face_locationout = (0, widthout, heightout, 0)
                                        encodingsout = face_recognition.face_encodings(imgout, known_face_locations=[
                                            face_locationout])
                                        if len(encodingsout) > 0:
                                            results_encodingout = encodingsout[0]
                                        else:
                                            print("No faces found in the imageout!")
                                            quit()

                                        results_re = face_recognition.compare_faces([results_encoding],
                                                                                    results_encodingout)

                                        if results_re[0] == True:

                                            #ArduinoUnoSerial.write('R'.encode())  # send 1 to the arduino's Data code
                                            print("LED turned ON")

                                            print(results_re[0])
                                            bill_total = '2.000vnd'

                                            def createFolderouta(dicreta):
                                                try:
                                                    if not os.path.exists(dicreta):
                                                        os.makedirs(dicreta)
                                                except OSError:
                                                    print('No creating folder')

                                            createFolderouta(
                                                f'D:\Python\CUSTOMDATA\DATA SPACE Output\{final_text_imgout}\check_out')
                                            savedatain = f'D:\Python\CUSTOMDATA\DATA SPACE Output\{final_text_imgout}\check_out\Face_{final_text_imgout}_IN.png'
                                            cv2.imwrite(savedatain, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
                                            savedataout = f'D:\Python\CUSTOMDATA\DATA SPACE Output\{final_text_imgout}\check_out/Face_{final_text_imgout}_OUT.png'
                                            cv2.imwrite(savedataout, cv2.cvtColor(imgout, cv2.COLOR_RGB2BGR))

                                            frame_results = tk.Frame(root_top, height=100, width=100, bg='light blue')
                                            frame_results.place(x=1280, y=00)
                                            label_results = tk.Label(frame_results)
                                            label_results.place(x=0, y=0)
                                            img = Image.fromarray(img).resize((100, 100))
                                            img = ImageTk.PhotoImage(image=img)
                                            label_results.imgtk = img
                                            label_results.configure(image=img)
                                            label_results.update()

                                            frame_results_out = tk.Frame(root_top, height=100, width=100,
                                                                         bg='light blue')
                                            frame_results_out.place(x=1400, y=0)
                                            label_results_out = tk.Label(frame_results_out)
                                            label_results_out.place(x=0, y=0)
                                            imgout = Image.fromarray(imgout).resize((100, 100))
                                            imgout = ImageTk.PhotoImage(image=imgout)
                                            label_results_out.imgtk = imgout
                                            label_results_out.configure(image=imgout)
                                            label_results_out.update()
                                            countout = 1
                                            break

                                        if results_re[0] == False:
                                            #ArduinoUnoSerial.write('N'.encode())  # send 0 to the arduino's Data code
                                            print("LED turned OFF")
                                            bill_total = 'False'

                                            def total():
                                                total_lb = tk.Label(root_mid, text='Total Pay: ', font=('arial', 10),
                                                                    fg='black',
                                                                    bg='light blue')
                                                total_lb.place(x=1130, y=95)
                                                display_total_lb = tk.Label(root_mid, text=f'False',
                                                                            font=('arial', 10),
                                                                            fg='red', width=12, bg='white',
                                                                            border=5,
                                                                            highlightthickness=5)
                                                display_total_lb.place(x=1270, y=95)

                                            total()
                                            iffalse += 1
                                            if (iffalse >= 5):
                                                countout = 1
                                                iffalse = 0
                                                break

                                face_re()

                                def total():
                                    total_lb = tk.Label(root_mid, text='Total Pay: ', font=('arial', 10), fg='black',
                                                        bg='light blue')
                                    total_lb.place(x=1130, y=95)
                                    display_total_lb = tk.Label(root_mid, text=f'{bill_total}', font=('arial', 10),
                                                                fg='red', width=12, bg='white', border=5,
                                                                highlightthickness=5)
                                    display_total_lb.place(x=1270, y=95)

                                total()


                            else:
                                #ArduinoUnoSerial.write('N'.encode())  # send 0 to the arduino's Data code
                                print("LED turned OFF")

                                def plateout_id():
                                    display_plateout_lb.config(text='No Found ID')
                                    display_plateout_lb.after(100, plateout_id)

                                display_plateout_lb = tk.Label(root_mid, text=f'', font=('arial', 10),
                                                               fg='dark blue', width=12, bg='white', border=5,
                                                               highlightthickness=5)
                                display_plateout_lb.place(x=890, y=50)
                                plateout_lb = tk.Label(root_mid, text='Face ID: ', font=('arial', 10), fg='black',
                                                       bg='light blue')
                                plateout_lb.place(x=770, y=55)
                                plateout_id()

                                def faceout_id():
                                    display_faceout_lb.config(text='No Found ID')
                                    display_faceout_lb.after(100, faceout_id)

                                display_faceout_lb = tk.Label(root_mid, text=f'', font=('arial', 10),
                                                              fg='dark blue', width=12, bg='white', border=5,
                                                              highlightthickness=5)
                                display_faceout_lb.place(x=890, y=95)
                                faceout_lb = tk.Label(root_mid, text='License Plate ID: ', font=('arial', 10),
                                                      fg='black',
                                                      bg='light blue')
                                faceout_lb.place(x=770, y=100)
                                faceout_id()

                                def date_timeout():
                                    s_timeout = datetime.datetime.now().strftime('%H:%M, %d-%m-%Y')
                                    s_timeout = f'{s_timeout}'
                                    display_plateout_in_lb.config(text=s_timeout)

                                timeout_lb_in = tk.Label(root_mid, text='Time Check In: ', font=('arial', 10),
                                                         fg='black',
                                                         bg='light blue')
                                timeout_lb_in.place(x=1130, y=55)
                                display_plateout_in_lb = tk.Label(root_mid, text='', font=('arial', 10),
                                                                  fg='dark blue', width=12, bg='white', border=5,
                                                                  highlightthickness=5)
                                display_plateout_in_lb.place(x=1270, y=50)
                                date_timeout()

                                def total():
                                    total_lb = tk.Label(root_mid, text='Total Pay: ', font=('arial', 10), fg='black',
                                                        bg='light blue')
                                    total_lb.place(x=1130, y=95)
                                    display_total_lb = tk.Label(root_mid, text=f'False', font=('arial', 10),
                                                                fg='red', width=12, bg='white', border=5,
                                                                highlightthickness=5)
                                    display_total_lb.place(x=1270, y=95)

                                total()

                        else:
                            #ArduinoUnoSerial.write('N'.encode())  # send 0 to the arduino's Data code
                            print("LED turned OFF")

                            def plateout_id():
                                display_plateout_lb.config(text='No Found ID')
                                display_plateout_lb.after(100, plateout_id)

                            display_plateout_lb = tk.Label(root_mid, text=f'', font=('arial', 10),
                                                           fg='dark blue', width=12, bg='white', border=5,
                                                           highlightthickness=5)
                            display_plateout_lb.place(x=890, y=50)
                            plateout_lb = tk.Label(root_mid, text='Face ID: ', font=('arial', 10), fg='black',
                                                   bg='light blue')
                            plateout_lb.place(x=770, y=55)
                            plateout_id()

                            def faceout_id():
                                display_faceout_lb.config(text='No Found ID')
                                display_faceout_lb.after(100, faceout_id)

                            display_faceout_lb = tk.Label(root_mid, text=f'', font=('arial', 10),
                                                          fg='dark blue', width=12, bg='white', border=5,
                                                          highlightthickness=5)
                            display_faceout_lb.place(x=890, y=95)
                            faceout_lb = tk.Label(root_mid, text='License Plate ID: ', font=('arial', 10), fg='black',
                                                  bg='light blue')
                            faceout_lb.place(x=770, y=100)
                            faceout_id()

                            def date_timeout():
                                s_timeout = datetime.datetime.now().strftime('%H:%M, %d-%m-%Y')
                                s_timeout = f'{s_timeout}'
                                display_plateout_in_lb.config(text=s_timeout)

                            timeout_lb_in = tk.Label(root_mid, text='Time Check In: ', font=('arial', 10), fg='black',
                                                     bg='light blue')
                            timeout_lb_in.place(x=1130, y=55)
                            display_plateout_in_lb = tk.Label(root_mid, text='', font=('arial', 10),
                                                              fg='dark blue', width=12, bg='white', border=5,
                                                              highlightthickness=5)
                            display_plateout_in_lb.place(x=1270, y=50)
                            date_timeout()

                            def total():
                                total_lb = tk.Label(root_mid, text='Total Pay: ', font=('arial', 10), fg='black',
                                                    bg='light blue')
                                total_lb.place(x=1130, y=95)
                                display_total_lb = tk.Label(root_mid, text=f'False', font=('arial', 10),
                                                            fg='red', width=12, bg='white', border=5,
                                                            highlightthickness=5)
                                display_total_lb.place(x=1270, y=95)

                            total()

                    display_checkout_id()

            # -------------------------------------------------------BUTTON DETECT INPUT---------------------------------------------
            def btn_detect():

                def var_count():
                    global var, count
                    #var = ArduinoUnoSerial.read()
                    var = str(var, encoding='latin-1')
                    var = var.strip('\r\n')
                    if (count == 0):
                        try:
                            if (var == '1'):
                                face_plate_save()
                        except:
                            print("WAITING OTHER MOTORBIKE")
                    if (count == 1):
                        if (var == '0'):
                            count = 0
                            print("WAITING OTHER MOTORBIKE")
                    var_lb.after(29, var_count)

                var_lb = tk.Label(root_top, bg='light blue', font=('Bold', 15))
                var_count()

                def face_plate_save():
                    # RESET FOLDER WHEN STARTING
                    shutil.rmtree(r'D:\Python\CUSTOMDATA\License plate', ignore_errors=True)
                    shutil.rmtree(r'D:\Python\CUSTOMDATA\Face', ignore_errors=True)

                    def cam_face_in():
                        lb_face_in = tk.Label(frame_left)

                        # lb_face_in.place(x=0, y=0)

                        def video_stream_face():
                            global result_frame_face, pre_timeframe, new_timeframe
                            _, frame_face = cap_face.read()
                            new_timeframe = time.time()
                            fps = 1 / (new_timeframe - pre_timeframe)
                            pre_timeframe = new_timeframe
                            fps = int(fps)
                            print(fps)
                            frame_face = cv2.cvtColor(frame_face, cv2.COLOR_BGR2RGB)
                            result_frame_face = model(frame_face)
                            frame_face = np.squeeze(result_frame_face.render())
                            frame_face = Image.fromarray(frame_face).resize((385, 255))
                            frame_face = ImageTk.PhotoImage(image=frame_face)
                            lb_face_in.imgtk = frame_face
                            lb_face_in.configure(image=frame_face)
                            lb_face_in.lift()
                            lb_face_in.update()

                        video_stream_face()

                    cam_face_in()

                    def cam_plate_in():
                        lb_plate_in = tk.Label(frame_left)

                        # lb_plate_in.place(x=0, y=260)

                        def video_stream_plate():
                            global result_frame_plate
                            _, frame_plate = cap_plate.read()
                            frame_plate = cv2.cvtColor(frame_plate, cv2.COLOR_BGR2RGB)
                            result_frame_plate = model(frame_plate)
                            frame_plate = np.squeeze(result_frame_plate.render())
                            frame_plate = Image.fromarray(frame_plate).resize((385, 255))
                            frame_plate = ImageTk.PhotoImage(image=frame_plate)
                            lb_plate_in.imgtk = frame_plate
                            lb_plate_in.configure(image=frame_plate)
                            lb_plate_in.lift()
                            lb_plate_in.update()

                        video_stream_plate()

                    cam_plate_in()

                    crops = result_frame_plate.crop(save=True,
                                                    save_dir=f'D:\Python\CUSTOMDATA\License plate\License plate')
                    crops_face = result_frame_face.crop(save=True, save_dir=f'D:\Python\CUSTOMDATA\Face\Face')

                    show_detect()

                btn_detect = tk.Button(root_bot, text='Show Dectect', font=('arial', 15), bg='#FFFF00', fg='black',
                                       activeforeground='#FFFF66', activebackground='black', width=12,
                                       command=face_plate_save)
                btn_detect.place(x=0, y=0)

            btn_detect()

            def show_detect():
                global img_plate, img_face, display_plate_lb, final_text_img, img_face_1
                img_plate = Image.open(
                    f'D:\Python\CUSTOMDATA\License plate\License plate\crops\License Plate\image0.jpg')
                img_face = Image.open(f'D:\Python\CUSTOMDATA\Face\Face\crops\Face\image0.jpg')
                try:
                    img_face_1 = Image.open(f'D:\Python\CUSTOMDATA\Face\Face\crops\Face\image02.jpg')
                    img_face_1 = img_face_1.resize((120, 120))
                    img_face_1 = ImageTk.PhotoImage(img_face_1)
                    detect_face_1 = cv2.imread(f'D:\Python\CUSTOMDATA\Face\Face\crops\Face\image02.jpg')
                except:
                    img_face_1 = None

                img_plate = img_plate.resize((385, 255))
                img_face = img_face.resize((385, 255))
                img_plate = ImageTk.PhotoImage(img_plate)
                img_face = ImageTk.PhotoImage(img_face)
                global final_crop_frame_plate, final_crop_frame_face, text_img, final_img_detect_face, crop_frame, threshold_2
                detect_face = cv2.imread(f'D:\Python\CUSTOMDATA\Face\Face\crops\Face\image0.jpg')
                detect_plate = cv2.imread(
                    f'D:\Python\CUSTOMDATA\License plate\License plate\crops\License Plate\image0.jpg')
                # LOOP CONTOURS PLATE
                plates = model(detect_plate, size=640)
                list_plates = plates.pandas().xyxy[0].values.tolist()
                list_read_plates = set()

                if len(list_plates) == 0:
                    text_img = helper.read_plate(yolo_license_plate, detect_plate)
                    if text_img != "unknown":
                        list_read_plates.add(text_img)

                else:
                    for plate in list_plates:
                        flag = 0
                        x = int(plate[0])  # xmin
                        y = int(plate[1])  # ymin
                        w = int(plate[2] - plate[0])  # xmax - xmin
                        h = int(plate[3] - plate[1])  # ymax - ymin
                        crop_img = detect_plate[y:y + h, x:x + w]
                        cv2.rectangle(detect_plate, (int(plate[0]), int(plate[1])), (int(plate[2]), int(plate[3])),
                                      color=(0, 0, 225), thickness=2)
                        text_img = ""
                        for cc in range(0, 2):
                            for ct in range(0, 2):
                                text_img = helper.read_plate(yolo_license_plate, utils_rotate.deskew(crop_img, cc, ct))
                                if text_img != "unknown":
                                    list_read_plates.add(text_img)
                                    flag = 1
                                    break
                            if flag == 1:
                                break

                # COUNT LETTER IN STRING
                final_text_img = ''
                for text_img in text_img:
                    if text_img.isalnum():
                        final_text_img += text_img
                        number_string = len(final_text_img)

                def display_checkin_id():
                    global display_plate_lb, plate_lb, display_face_lb, face_lb, checkstate_lb, \
                        display_checkstate_lb, time_lb_in, display_plate_in_lb, results_face_lb

                    def destroy_lb():
                        display_plate_lb.destroy()
                        plate_lb.destroy()
                        display_face_lb.destroy()
                        face_lb.destroy()
                        checkstate_lb.destroy()
                        display_checkstate_lb.destroy()
                        time_lb_in.destroy()
                        display_plate_in_lb.destroy()

                    destroy_lb()

                    def results_show():
                        global results_faceother_lb
                        results_face_lb = tk.Label(frame_left, image=img_face)
                        results_face_lb.place(x=385, y=0)
                        if img_face_1 != None:
                            results_faceother_lb = tk.Label(results_face_lb, image=img_face_1)
                            results_faceother_lb.place(x=0, y=0)
                        if img_face_1 == None:
                            try:
                                results_faceother_lb.destroy()
                            except:
                                print('No other face destroy')

                        results_plate_lb = tk.Label(frame_left, image=img_plate)
                        results_plate_lb.place(x=385, y=260)

                    results_show()
                    global count, stand_3

                    if (number_string == 8) or (number_string == 9):
                        check = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
                        stand_2 = f'{final_text_img[2]}'
                        try:
                            stand_3 = [f'{final_text_img[0]}', f'{final_text_img[1]}', f'{final_text_img[4]}',
                                       f'{final_text_img[5]}',
                                       f'{final_text_img[6]}', f'{final_text_img[7]}', f'{final_text_img[8]}']
                        except:
                            stand_3 = [f'{final_text_img[0]}', f'{final_text_img[1]}', f'{final_text_img[4]}',
                                       f'{final_text_img[5]}',
                                       f'{final_text_img[6]}', f'{final_text_img[7]}']
                        for dem in stand_3:
                            if (dem in check):
                                stand_3 = True
                            else:
                                stand_3 = False
                                break
                        if (stand_2 not in check) & (stand_3 == True):

                            def plate_id():
                                display_plate_lb.config(text=final_text_img)
                                display_plate_lb.after(100, plate_id)

                            display_plate_lb = tk.Label(root_mid, text=f'{final_text_img}', font=('arial', 10),
                                                        fg='dark blue', width=12, bg='white', border=5,
                                                        highlightthickness=5)
                            display_plate_lb.place(x=120, y=50)
                            plate_lb = tk.Label(root_mid, text='Face ID: ', font=('arial', 10), fg='black',
                                                bg='light blue')
                            plate_lb.place(x=0, y=55)
                            plate_id()

                            def face_id():
                                display_face_lb.config(text=final_text_img)
                                display_face_lb.after(100, face_id)

                            display_face_lb = tk.Label(root_mid, text=f'{final_text_img}', font=('arial', 10),
                                                       fg='dark blue', width=12, bg='white', border=5,
                                                       highlightthickness=5)
                            display_face_lb.place(x=120, y=95)
                            face_lb = tk.Label(root_mid, text='License Plate ID: ', font=('arial', 10), fg='black',
                                               bg='light blue')
                            face_lb.place(x=0, y=100)
                            face_id()

                            def date_time():
                                s_time = datetime.datetime.now().strftime('%H:%M, %d-%m-%Y')
                                s_time = f'{s_time}'
                                display_plate_in_lb.config(text=s_time)

                            time_lb_in = tk.Label(root_mid, text='Time Check In: ', font=('arial', 10), fg='black',
                                                  bg='light blue')
                            time_lb_in.place(x=360, y=55)
                            display_plate_in_lb = tk.Label(root_mid, text='', font=('arial', 10),
                                                           fg='dark blue', width=12, bg='white', border=5,
                                                           highlightthickness=5)
                            display_plate_in_lb.place(x=480, y=50)
                            date_time()

                            def state():
                                checkstate_lb = tk.Label(root_mid, text='State: ', font=('arial', 10), fg='black',
                                                         bg='light blue')
                                checkstate_lb.place(x=360, y=95)
                                display_checkstate_lb = tk.Label(root_mid, text=f'{stand_3}', font=('arial', 10),
                                                                 fg='red', width=12, bg='white', border=5,
                                                                 highlightthickness=5)
                                display_checkstate_lb.place(x=480, y=95)

                            state()

                            def save_results():

                                def createFolder(dicret):
                                    try:
                                        if not os.path.exists(dicret):
                                            os.makedirs(dicret)
                                    except OSError:
                                        print('No creating folder')

                                createFolder(f'D:\Python\CUSTOMDATA\DATA SPACE Input\{final_text_img}')
                                s_time = datetime.datetime.now().strftime('(%d-%m, %Hh %Mm)')
                                s_time_ID = datetime.datetime.now().strftime('(%d-%m-%Y, %Hh %Mm)')
                                s_time = f'{s_time}'
                                s_time_ID = f'{s_time_ID}'
                                file_name_plate = f'D:\Python\CUSTOMDATA\DATA SPACE Input\{final_text_img}\License plate_{final_text_img}.png'
                                cv2.imwrite(file_name_plate, detect_plate)
                                file_name_face = f'D:\Python\CUSTOMDATA\DATA SPACE Input\{final_text_img}\Face_{final_text_img}.png'
                                cv2.imwrite(file_name_face, detect_face)
                                try:
                                    file_name_face_1 = f'D:\Python\CUSTOMDATA\DATA SPACE Input\{final_text_img}\Face_{final_text_img}_(1).png'
                                    cv2.imwrite(file_name_face_1, detect_face_1)
                                except:
                                    print("No saving other face")
                                ID = f'{final_text_img}_{s_time_ID}'
                                f = open(
                                    f'D:\Python\CUSTOMDATA\DATA SPACE Input\{final_text_img}\ID {final_text_img}.txt',
                                    'a')
                                f.write('ID ')
                                f.write(ID + '\n')
                                f.close()

                            save_results()
                            #ArduinoUnoSerial.write('L'.encode())  # send 0 to the arduino's Data code
                            print("LED_in turned ON")
                            count = 1

                        else:
                            #ArduinoUnoSerial.write('N'.encode())  # send 0 to the arduino's Data code
                            print("LED_in turned OFF")

                            def plate_id():
                                display_plate_lb.config(text='No Found ID')
                                display_plate_lb.after(100, plate_id)

                            display_plate_lb = tk.Label(root_mid, text=f'', font=('arial', 10),
                                                        fg='dark blue', width=12, bg='white', border=5,
                                                        highlightthickness=5)
                            display_plate_lb.place(x=120, y=50)
                            plate_lb = tk.Label(root_mid, text='Face ID: ', font=('arial', 10), fg='black',
                                                bg='light blue')
                            plate_lb.place(x=0, y=55)
                            plate_id()

                            def face_id():
                                display_face_lb.config(text='No Found ID')
                                display_face_lb.after(100, face_id)

                            display_face_lb = tk.Label(root_mid, text=f'', font=('arial', 10),
                                                       fg='dark blue', width=12, bg='white', border=5,
                                                       highlightthickness=5)
                            display_face_lb.place(x=120, y=95)
                            face_lb = tk.Label(root_mid, text='License Plate ID: ', font=('arial', 10), fg='black',
                                               bg='light blue')
                            face_lb.place(x=0, y=100)
                            face_id()

                            def date_time():
                                s_time = datetime.datetime.now().strftime('%H:%M, %d-%m-%Y')
                                s_time = f'{s_time}'
                                display_plate_in_lb.config(text=s_time)

                            time_lb_in = tk.Label(root_mid, text='Time Check In: ', font=('arial', 10), fg='black',
                                                  bg='light blue')
                            time_lb_in.place(x=360, y=55)
                            display_plate_in_lb = tk.Label(root_mid, text='', font=('arial', 10),
                                                           fg='dark blue', width=12, bg='white', border=5,
                                                           highlightthickness=5)
                            display_plate_in_lb.place(x=480, y=50)
                            date_time()

                            def state():
                                global stand_3
                                checkstate_lb = tk.Label(root_mid, text='State: ', font=('arial', 10), fg='black',
                                                         bg='light blue')
                                checkstate_lb.place(x=360, y=95)
                                display_checkstate_lb = tk.Label(root_mid, text='False', font=('arial', 10),
                                                                 fg='red', width=12, bg='white', border=5,
                                                                 highlightthickness=5)
                                display_checkstate_lb.place(x=480, y=95)

                            state()

                    else:
                        #ArduinoUnoSerial.write('N'.encode())  # send 0 to the arduino's Data code
                        print("LED_in turned OFF")

                        def plate_id():
                            display_plate_lb.config(text='No Found ID')
                            display_plate_lb.after(100, plate_id)

                        display_plate_lb = tk.Label(root_mid, text=f'', font=('arial', 10),
                                                    fg='dark blue', width=12, bg='white', border=5,
                                                    highlightthickness=5)
                        display_plate_lb.place(x=120, y=50)
                        plate_lb = tk.Label(root_mid, text='Face ID: ', font=('arial', 10), fg='black', bg='light blue')
                        plate_lb.place(x=0, y=55)
                        plate_id()

                        def face_id():
                            display_face_lb.config(text='No Found ID')
                            display_face_lb.after(100, face_id)

                        display_face_lb = tk.Label(root_mid, text=f'', font=('arial', 10),
                                                   fg='dark blue', width=12, bg='white', border=5, highlightthickness=5)
                        display_face_lb.place(x=120, y=95)
                        face_lb = tk.Label(root_mid, text='License Plate ID: ', font=('arial', 10), fg='black',
                                           bg='light blue')
                        face_lb.place(x=0, y=100)
                        face_id()

                        def date_time():
                            s_time = datetime.datetime.now().strftime('%H:%M, %d-%m-%Y')
                            s_time = f'{s_time}'
                            display_plate_in_lb.config(text=s_time)

                        time_lb_in = tk.Label(root_mid, text='Time Check In: ', font=('arial', 10), fg='black',
                                              bg='light blue')
                        time_lb_in.place(x=360, y=55)
                        display_plate_in_lb = tk.Label(root_mid, text='', font=('arial', 10),
                                                       fg='dark blue', width=12, bg='white', border=5,
                                                       highlightthickness=5)
                        display_plate_in_lb.place(x=480, y=50)
                        date_time()

                        def state():
                            global stand_3
                            checkstate_lb = tk.Label(root_mid, text='State: ', font=('arial', 10), fg='black',
                                                     bg='light blue')
                            checkstate_lb.place(x=360, y=95)
                            display_checkstate_lb = tk.Label(root_mid, text=f'False', font=('arial', 10),
                                                             fg='red', width=12, bg='white', border=5,
                                                             highlightthickness=5)
                            display_checkstate_lb.place(x=480, y=95)

                        state()

                display_checkin_id()

        root_frame()
        windows.update()

    # -----------------------------------------------SIGN IN PAGE--------------------------------------------------------
    def signin_page():
        def bg_windows():
            global img_bg_windows
            img_bg_windows = tk.PhotoImage(file=r'D:\Python\CUSTOMDATA\image setting\backgroung.png')
            background_label = tk.Label(windows, image=img_bg_windows)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)

        bg_windows()

        # -----------------------------------------------SIGN IN FRAME-----------------------------------------------------------
        def signin_frame():
            signin = tk.Frame(windows, height=480, width=360, bg='white')
            signin.pack(expand=True)
            # FRAME SIGN IN TOP
            signin_top = tk.Frame(signin, height=70, width=360, bg='white')
            signin_top.pack()

            def title_sign_in():
                global img_sign_in
                img_sign_in = tk.PhotoImage(file=r'D:\Python\CUSTOMDATA\image setting\Login Text.png')

                # LABEL DATE TIME
                def date_time():
                    s_time = datetime.datetime.now().strftime('%H:%M:%S, %d-%m-%Y')
                    s_time = f'{s_time}'
                    time_lb.config(text=s_time)
                    time_lb.after(10, date_time)

                time_lb = tk.Label(signin_top, fg='dark blue', bg='white', font=('Bold', 10))
                time_lb.pack()
                date_time()
                # LABEL LOGIN
                login_label = tk.Label(signin_top, image=img_sign_in, bg='white')
                login_label.pack(expand=True)

            title_sign_in()

            # FRAME SIGN IN MID
            signin_mid = tk.Frame(signin, height=340, width=360, bg='white')
            signin_mid.pack()

            # ------------------------------------------SHOW PASSWORD AND USERNAME---------------------------------------------------
            def entry_acc_pass():
                def on_enter(e):
                    username_account.delete(0, 'end')

                def on_leave(e):
                    name = username_account.get()
                    if name == '':
                        username_account.insert(0, 'Drand')

                def on_enter_pass(e):
                    password_account.delete(0, 'end')

                def on_leave_pass(e):
                    name = password_account.get()
                    if name == '':
                        password_account.insert(0, '1812')

                # -------------------------------------------------ENTRY USER------------------------------------------------------------
                user_lb = tk.Label(signin_mid, text='Username', bg='white', font=('Bold', 10), fg='gray')
                user_lb.place(x=25, y=0)
                username_account = tk.Entry(signin_mid, width=20, border=1, bd=0, font=('Arial', 20), fg='black',
                                            bg='#B9D3EE', highlightcolor='dark blue',
                                            highlightthickness=2, highlightbackground='light blue')
                username_account.place(x=25, y=25)
                username_account.insert(0, 'Drand')
                username_account.bind('<FocusIn>', on_enter)
                username_account.bind('<FocusOut>', on_leave)

                # -------------------------------------------------ENTRY PASSWORD--------------------------------------------------------
                pass_lb = tk.Label(signin_mid, text='Password', bg='white', font=('Bold', 10), fg='gray')
                pass_lb.place(x=25, y=75)
                password_account = tk.Entry(signin_mid, width=20, border=1, bd=0, font=('Arial', 20), fg='black',
                                            bg='#B9D3EE', highlightcolor='dark blue', highlightthickness=2, show='*',
                                            highlightbackground='light blue')
                password_account.place(x=25, y=100)
                password_account.insert(0, '1812')
                password_account.bind('<FocusIn>', on_enter_pass)
                password_account.bind('<FocusOut>', on_leave_pass)

                # ---------------------------------------------------BUTTON SIGN IN------------------------------------------------------
                def button_sign_in():

                    def sign_in_page():
                        user = username_account.get()
                        pas = password_account.get()
                        if (user == 'Drand') & (pas == '1812'):
                            windows.geometry('1920x800')
                            windows.resizable(width=True, height=True)
                            signin.destroy()
                            signin_top.destroy()
                            signin_mid.destroy()
                            signin_bot.destroy()
                            root_page()
                        elif (user != 'Drand') & (pas != '1812'):
                            messagebox.showerror("Invalid", "Incorrect Your Account!")
                        elif (user != 'Drand') & (pas == '1812'):
                            messagebox.showerror("Invalid", "Incorrect Your User!")
                        elif (user == 'Drand') & (pas != '1812'):
                            messagebox.showerror("Invalid", "Incorrect Your Password!")

                    global on_cancel, off_cancel, on_login, off_login
                    on_cancel = tk.PhotoImage(file=r'D:\Python\CUSTOMDATA\image setting\Button Sign in_on.png')
                    off_cancel = tk.PhotoImage(file=r'D:\Python\CUSTOMDATA\image setting\Button Sign in_off.png')
                    on_login = tk.PhotoImage(file=r'D:\Python\CUSTOMDATA\image setting\Button Login_on.png')
                    off_login = tk.PhotoImage(file=r'D:\Python\CUSTOMDATA\image setting\Button Login_off.png')
                    cancel_btn = tk.Button(signin_mid, image=off_cancel,
                                           font=('Bold', 15), bg='white', fg='white', border=0,
                                           command=windows.destroy, activebackground='white')
                    cancel_btn.place(x=175, y=180)
                    login_btn = tk.Button(signin_mid, image=on_login,
                                          font=('Bold', 15), bg='white', fg='white',
                                          border=0, activebackground='white', command=sign_in_page)
                    login_btn.place(x=30, y=180)

                button_sign_in()

                # ------------------------------------------------SHOW PASSWORD----------------------------------------------------------
                def show_password():
                    img_hiden = tk.PhotoImage(file=r'D:\Python\CUSTOMDATA\image setting\show.png')
                    img_show = tk.PhotoImage(file=r'D:\Python\CUSTOMDATA\image setting\hiden.png')

                    def show_pass(command):
                        if command == 'show':
                            password_account.config(show='*')
                            show_hide_password.config(image=img_show)
                            show_hide_password.config(command=lambda: show_pass('hide'))
                        else:
                            password_account.config(show='')
                            show_hide_password.config(image=img_hiden)
                            show_hide_password.config(command=lambda: show_pass('show'))

                    show_hide_password = tk.Button(password_account, image=img_show, bd=0, bg='#B9D3EE',
                                                   command=lambda: show_pass('hide'))
                    show_hide_password.place(x=260, y=0)

                show_password()

            entry_acc_pass()

            # --------------------------------------------------REMEMBER TICK ACCOUNT------------------------------------------------
            def remember_tick_accunt():
                x = tk.IntVar()

                def remember_tick():
                    pass

                tick_remember = tk.Checkbutton(signin_mid, text='Remember me', font=('Bold', 10), bg='white', fg='black'
                                               , variable=x, onvalue=1, offvalue=0, command=remember_tick,
                                               activebackground='white')
                tick_remember.place(x=25, y=150)
                forgot_btn = tk.Button(signin_mid, text='Forgot Account?',
                                       font=('Bold', 10),
                                       bg='white', border=0, fg='dark blue', underline=True,
                                       activeforeground='light blue',
                                       activebackground='white')
                forgot_btn.place(x=225, y=150)

            remember_tick_accunt()

            def or_sign_in():
                or_sign_in_lable = tk.Label(signin_mid, text='━━━━━━━━━ Or Sign In With ━━━━━━━━━━', font=('arial', 10)
                                            , fg='gray', bg='white')
                or_sign_in_lable.place(x=5, y=250)

            or_sign_in()

            # ----------------------------------------------BUTTON OTHER SIGN UP-----------------------------------------------------
            def button_or_sign_in():
                global google, facebook, twitter
                google = tk.PhotoImage(file=r'D:\Python\CUSTOMDATA\image setting\Button_gg.png')
                facebook = tk.PhotoImage(file=r'D:\Python\CUSTOMDATA\image setting\Button_fb.png')
                twitter = tk.PhotoImage(file=r'D:\Python\CUSTOMDATA\image setting\Button_tw.png')

                def google_sign_in():
                    pass

                def facebook_sign_in():
                    pass

                def twitter_sign_in():
                    pass

                google_btn = tk.Button(signin_mid, image=google, fg='white', border=0, command=google_sign_in,
                                       relief="raised", activebackground='white', bg='white')
                google_btn.place(x=80, y=280)

                facebook_btn = tk.Button(signin_mid, image=facebook, fg='white', border=0, command=facebook_sign_in,
                                         relief="raised", activebackground='white', bg='white')
                facebook_btn.place(x=150, y=280)

                twitter_btn = tk.Button(signin_mid, image=twitter, fg='white', border=0, command=twitter_sign_in,
                                        relief="raised", activebackground='white', bg='white')
                twitter_btn.place(x=220, y=275)

            button_or_sign_in()

            # FRAME SIGN IN BOT
            signin_bot = tk.Frame(signin, height=70, width=360, bg='#E8E8E8')
            signin_bot.pack()

            # --------------------------------------------------BUTTON SIGN UP-------------------------------------------------------
            def button_sign_up():
                def signup():
                    signin.destroy()
                    signin_top.destroy()
                    signin_mid.destroy()
                    signin_bot.destroy()
                    signup_page()

                global img_sign_up
                img_sign_up = tk.PhotoImage(file=r'D:\Python\CUSTOMDATA\image setting\Sign up.png')
                sign_up_lb = tk.Label(signin_bot, text="Don't have an account?", font=('Bold', 12), bg='#E8E8E8',
                                      fg='black')
                sign_up_lb.place(x=25, y=9)
                sign_btn = tk.Button(signin_bot, image=img_sign_up, height=20, border=0,
                                     bg='#E8E8E8', activebackground='#E8E8E8', command=signup)
                sign_btn.place(x=192, y=7)
                copyright_lb = tk.Label(signin_bot, text="copyright by Phu Dang", font=('arial', 8), bg='#E8E8E8',
                                        fg='black')
                copyright_lb.place(x=120, y=40)

            button_sign_up()

        signin_frame()

    signin_page()

    # ------------------------------------------------------SIGN UP PAGE----------------------------------------------------
    def signup_page():
        windows.title('SIGN UP')

        def signup_frame():
            signup = tk.Frame(windows, height=480, width=360, bg='white')
            signup.pack(expand=True)
            # FRAME SIGN IN TOP
            signup_top = tk.Frame(signup, height=70, width=360, bg='white')
            signup_top.pack()

            def title_sign_up():
                global img_sign_up
                img_sign_up = tk.PhotoImage(file=r'D:\Python\CUSTOMDATA\image setting\sign up 1.png')

                # LABEL DATE TIME
                def date_time():
                    s_time = datetime.datetime.now().strftime('%H:%M:%S, %d-%m-%Y')
                    s_time = f'{s_time}'
                    time_lb.config(text=s_time)
                    time_lb.after(10, date_time)

                time_lb = tk.Label(signup_top, fg='dark blue', bg='white', font=('Bold', 10))
                time_lb.pack()
                date_time()
                # LABEL LOGIN
                sign_up_label = tk.Label(signup_top, image=img_sign_up, bg='white', height=60)
                sign_up_label.pack(expand=True)

            title_sign_up()
            # FRAME SIGN IN MID
            signup_mid = tk.Frame(signup, height=340, width=360, bg='white')
            signup_mid.pack()

            # ---------------------------------------------------ENTRY ACCOUNT-------------------------------------------------------
            # ---------------------------------------------------SHOW PASS AND USER--------------------------------------------------
            def entry_acc_repass():
                def on_enter(e):
                    username_account.delete(0, 'end')

                def on_leave(e):
                    name = username_account.get()
                    if name == '':
                        username_account.insert(0, 'Drand')

                def on_enter_pass(e):
                    password_account.delete(0, 'end')

                def on_leave_pass(e):
                    name = password_account.get()
                    if name == '':
                        password_account.insert(0, '1812')

                def on_enter_repass(e):
                    repassword_account.delete(0, 'end')

                def on_leave_repass(e):
                    name = repassword_account.get()
                    if name == '':
                        repassword_account.insert(0, '1812')

                # --------------------------------------------------ENTRY USER-----------------------------------------------------------
                user_lb = tk.Label(signup_mid, text='Username', bg='white', font=('Bold', 10), fg='gray')
                user_lb.place(x=25, y=0)
                username_account = tk.Entry(signup_mid, width=20, border=1, bd=0, font=('Arial', 20), fg='black',
                                            bg='#B9D3EE', highlightcolor='dark blue',
                                            highlightthickness=2, highlightbackground='light blue')
                username_account.place(x=25, y=25)
                username_account.insert(0, 'Drand')
                username_account.bind('<FocusIn>', on_enter)
                username_account.bind('<FocusOut>', on_leave)
                # -------------------------------------------------ENTRY PASSWORD--------------------------------------------------------
                pass_lb = tk.Label(signup_mid, text='Password', bg='white', font=('Bold', 10), fg='gray')
                pass_lb.place(x=25, y=70)
                password_account = tk.Entry(signup_mid, width=20, border=1, bd=0, font=('Arial', 20), fg='black',
                                            bg='#B9D3EE', highlightcolor='dark blue', highlightthickness=2, show='*',
                                            highlightbackground='light blue')
                password_account.place(x=25, y=95)
                password_account.insert(0, '1812')
                password_account.bind('<FocusIn>', on_enter_pass)
                password_account.bind('<FocusOut>', on_leave_pass)

                # -------------------------------------------------SHOW PASSWORD---------------------------------------------------------
                def show_password():
                    img_hiden = tk.PhotoImage(file=r'D:\Python\CUSTOMDATA\image setting\show.png')
                    img_show = tk.PhotoImage(file=r'D:\Python\CUSTOMDATA\image setting\hiden.png')

                    def show_pass(command):
                        if command == 'show':
                            password_account.config(show='*')
                            show_hide_password.config(image=img_show)
                            show_hide_password.config(command=lambda: show_pass('hide'))
                        else:
                            password_account.config(show='')
                            show_hide_password.config(image=img_hiden)
                            show_hide_password.config(command=lambda: show_pass('show'))

                    show_hide_password = tk.Button(password_account, image=img_show, bd=0, bg='#B9D3EE',
                                                   command=lambda: show_pass('hide'))
                    show_hide_password.place(x=260, y=0)

                show_password()
                # -------------------------------------------------ENTRY REPASSWORD------------------------------------------------------
                repass_lb = tk.Label(signup_mid, text='Re-Password', bg='white', font=('Bold', 10), fg='gray')
                repass_lb.place(x=25, y=140)
                repassword_account = tk.Entry(signup_mid, width=20, border=1, bd=0, font=('Arial', 20), fg='black',
                                              bg='#B9D3EE', highlightcolor='dark blue', highlightthickness=2, show='*',
                                              highlightbackground='light blue')
                repassword_account.place(x=25, y=165)
                repassword_account.insert(0, '1812')
                repassword_account.bind('<FocusIn>', on_enter_repass)
                repassword_account.bind('<FocusOut>', on_leave_repass)

                # ----------------------------------------------------BUTTON SHOW REPASS-------------------------------------------------
                def show_repassword():
                    img_hiden = tk.PhotoImage(file=r'D:\Python\CUSTOMDATA\image setting\show.png')
                    img_show = tk.PhotoImage(file=r'D:\Python\CUSTOMDATA\image setting\hiden.png')

                    def show_repass(command):
                        if command == 'show':
                            repassword_account.config(show='*')
                            show_hide_repassword.config(image=img_show)
                            show_hide_repassword.config(command=lambda: show_repass('hide'))
                        else:
                            repassword_account.config(show='')
                            show_hide_repassword.config(image=img_hiden)
                            show_hide_repassword.config(command=lambda: show_repass('show'))

                    show_hide_repassword = tk.Button(repassword_account, image=img_show, bd=0, bg='#B9D3EE',
                                                     command=lambda: show_repass('hide'))
                    show_hide_repassword.place(x=260, y=0)

                show_repassword()

            entry_acc_repass()

            # ------------------------------------------------AGREE TICK------------------------------------------------------------
            def agree_tick_signup():
                x = tk.IntVar()

                def agree_tick():
                    pass

                tick_remember = tk.Checkbutton(signup_mid, text='I read and agree to', font=('Bold', 10), bg='white',
                                               fg='black'
                                               , variable=x, onvalue=1, offvalue=0, command=agree_tick,
                                               activebackground='white')
                tick_remember.place(x=25, y=215)
                agree_btn = tk.Button(signup_mid, text='Terms & Conditions',
                                      font=('Bold', 10),
                                      bg='white', border=0, fg='dark blue', underline=True,
                                      activeforeground='light blue',
                                      activebackground='white')
                agree_btn.place(x=160, y=215)

            agree_tick_signup()

            # -----------------------------------------------------BUTTON REGISTER---------------------------------------------------
            def register_btn():
                def return_signin():
                    signup.destroy()
                    signup_top.destroy()
                    signup_mid.destroy()
                    signup_bot.destroy()
                    signin_page()

                def register():
                    pass

                global img_register, img_return
                img_register = tk.PhotoImage(file=r'D:\Python\CUSTOMDATA\image setting\register.png')
                img_return = tk.PhotoImage(file=r'D:\Python\CUSTOMDATA\image setting\return.png')
                register_btn = tk.Button(signup_mid, image=img_register,
                                         font=('Bold', 15), bg='white', fg='white', border=0,
                                         command=register, activebackground='white')
                register_btn.place(x=30, y=245)
                return_btn = tk.Button(signup_mid, image=img_return,
                                       font=('Bold', 15), bg='white', fg='white',
                                       border=0, activebackground='white', command=return_signin)
                return_btn.place(x=175, y=245)

            register_btn()

            # --------------------------------------------------LABEL OTHER SIGN UP--------------------------------------------------
            def or_sign_up():
                or_sign_up_lable = tk.Label(signup_mid, text='━━━━━━━━━ Or Sign Up With ━━━━━━━━━━', font=('arial', 10)
                                            , fg='gray', bg='white')
                or_sign_up_lable.place(x=5, y=310)

            or_sign_up()
            # FRAME SIGN IN BOT
            signup_bot = tk.Frame(signup, height=70, width=360, bg='#E8E8E8')
            signup_bot.pack()

            # ---------------------------------------------------BUTTON OTHER SIGN UP------------------------------------------------
            def button_or_sign_up():
                global google, facebook, twitter
                google = tk.PhotoImage(file=r'D:\Python\CUSTOMDATA\image setting\Button_gg.png')
                facebook = tk.PhotoImage(file=r'D:\Python\CUSTOMDATA\image setting\Button_fb.png')
                twitter = tk.PhotoImage(file=r'D:\Python\CUSTOMDATA\image setting\Button_tw.png')

                def google_sign_in():
                    pass

                def facebook_sign_in():
                    pass

                def twitter_sign_in():
                    pass

                google_btn = tk.Button(signup_bot, image=google, fg='white', border=0, command=google_sign_in,
                                       relief="raised", activebackground='#E8E8E8', bg='#E8E8E8')
                google_btn.place(x=80, y=15)
                facebook_btn = tk.Button(signup_bot, image=facebook, fg='white', border=0, command=facebook_sign_in,
                                         relief="raised", activebackground='#E8E8E8', bg='#E8E8E8')
                facebook_btn.place(x=150, y=15)
                twitter_btn = tk.Button(signup_bot, image=twitter, fg='white', border=0, command=twitter_sign_in,
                                        relief="raised", activebackground='#E8E8E8', bg='#E8E8E8')
                twitter_btn.place(x=220, y=10)

            button_or_sign_up()

        signup_frame()

    # -------------------------------------------------WINDOWS SETTING------------------------------------------------------
    def setting_page():
        setting_sys_page = tk.Toplevel(windows)
        setting_sys_page.geometry('480x640')
        setting_sys_page.resizable(width=False, height=False)
        setting_sys_page.title('Setting System')
        icon = tk.PhotoImage(file=r"D:\Python\CUSTOMDATA\image setting\logo.png")
        setting_sys_page.iconphoto(True, icon)

        def bg_setting_sys_page():
            global img_bg_setting_sys_page
            img_bg_setting_sys_page = tk.PhotoImage(file=r'D:\Python\CUSTOMDATA\image setting\backgroung.png')
            bg_setting_sys_page_label = tk.Label(setting_sys_page, image=img_bg_setting_sys_page)
            bg_setting_sys_page_label.place(x=0, y=0, relwidth=1, relheight=1)

        bg_setting_sys_page()
        notebook_tab = ttk.Notebook(setting_sys_page)
        notebook_tab.pack()

        def tab_page():
            global frame_tab1, frame_tab2
            frame_tab1 = tk.Frame(notebook_tab, width=440, height=600, bg="light gray")
            frame_tab1.pack(fill=tk.BOTH, expand=1)
            frame_tab2 = tk.Frame(notebook_tab, width=440, height=600, bg="light gray")
            frame_tab2.pack(fill=tk.BOTH, expand=1)
            frame_tab3 = tk.Frame(notebook_tab, width=440, height=600, bg="light gray")
            frame_tab3.pack(fill=tk.BOTH, expand=1)
            frame_tab4 = tk.Frame(notebook_tab, width=440, height=600, bg="light gray")
            frame_tab4.pack(fill=tk.BOTH, expand=1)
            notebook_tab.add(frame_tab1, text='Home')
            notebook_tab.add(frame_tab2, text='Advance')
            notebook_tab.add(frame_tab3, text='Account')
            notebook_tab.add(frame_tab4, text='Language')

        tab_page()
        setting_sys_page.update()

    # ---------------------------------------------WINDOWS ABOUT SYSTEM------------------------------------------------------
    def about_page():
        about_sys_page = tk.Toplevel(windows)
        about_sys_page.geometry('480x240')
        about_sys_page.resizable(width=False, height=False)
        about_sys_page.title('About')
        icon = tk.PhotoImage(file=r"D:\Python\CUSTOMDATA\logo.png")
        about_sys_page.iconphoto(True, icon)

        def frame_about():
            global frame_abt
            frame_abt = tk.Frame(about_sys_page, height=480, width=480)
            frame_abt.place(x=0, y=0)

        frame_about()

        def title_about():
            global frame_abt
            title_abt = tk.Label(frame_abt, text='SMART MOTORBIKE PARKING SYSTEM', font=('arial', 13))
            title_abt.place(x=80, y=20)
            title_abt_3 = tk.Label(frame_abt, text='(by Drand)', font=('arial', 11))
            title_abt_3.place(x=380, y=20)
            lb_logo_abt = tk.Label(frame_abt)
            lb_logo_abt.place(x=20, y=60)
            img_abt = Image.open(r'D:\Python\CUSTOMDATA\image setting\logo_abt.png')
            img_abt = img_abt.resize((90, 90))
            img_abt = ImageTk.PhotoImage(img_abt)
            lb_logo_abt.imgtk = img_abt
            lb_logo_abt.configure(image=img_abt)
            lb_logo_abt.update()
            title_built = tk.Label(frame_abt, text='Built #Version 1.0, built on March 13, 2023', font=('arial', 10))
            title_built.place(x=150, y=60)
            title_license = tk.Label(frame_abt, text='Licensed to Tran Phu Dang', font=('arial', 10))
            title_license.place(x=150, y=100)
            title_sub = tk.Label(frame_abt, text='Subscription is active until January 1, 2030', font=('arial', 10))
            title_sub.place(x=150, y=120)
            title_power = tk.Label(frame_abt, text='Powered by Tran Phu Dang', font=('arial', 10))
            title_power.place(x=150, y=160)
            title_cpright = tk.Label(frame_abt, text='Copyright by Tran Phu Dang, 2023', font=('arial', 10))
            title_cpright.place(x=150, y=180)
            btn_close = tk.Button(frame_abt, text='Close', font=('arial', 10), command=about_sys_page.destroy)
            btn_close.place(x=400, y=200)

        title_about()

    # ----------------------------------------------------END PAGE ABOUT-----------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------
    windows.mainloop()


if __name__ == '__main__':
    main()
