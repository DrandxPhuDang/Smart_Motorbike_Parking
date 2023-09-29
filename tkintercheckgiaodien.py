from threading import *
import time
import cv2
import numpy as np
import torch.hub
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import glob
import matplotlib.pyplot as plt
import pytesseract
import datetime
import os
import tkinter as tk
import shutil
import face_recognition
from PIL import ImageTk, Image


def main():
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='Plate_Face_best (9).pt', force_reload=True)
    windows = tk.Tk()
    windows.geometry('1600x768')
    windows.title('LOGIN')
    icon = tk.PhotoImage(file="logo.png")
    windows.iconphoto(True, icon)

    def login_page():
        video_detect = "video detect 1.mp4"
        ip = 'http://192.168.1.11:4747/video'
        cap_plate = cv2.VideoCapture(video_detect)
        cap_face = cv2.VideoCapture(0)
        global img_login, img_google
        img_google = tk.PhotoImage(file='button google.png')
        img_hiden = tk.PhotoImage(file='show.png')
        img_show = tk.PhotoImage(file='hiden.png')

        img_login = tk.PhotoImage(file='backgroung.png')
        img_label = tk.Label(windows, image=img_login, bg='#6699CC')
        img_label.place(x=0, y=0)
        x = tk.IntVar()

        def login_acc():
            acc = username_account.get()
            pas = password_account.get()
            if (acc == 'Drand') & (pas == '1812'):
                remember_lb.destroy()
                bottom_frame.destroy()
                label_frame.destroy()
                login.destroy()
                def sign_out():
                    screen.destroy()
                    top_frame.destroy()
                    frame_in.destroy()
                    frame_out.destroy()
                    bottom_frame.destroy()
                    login_page()
                    cap_plate.release()
                    cap_face.release()

                screen = tk.Frame(windows, bg='light blue', height=768, width=1600)
#--------------------------------------------------------------------------------------------------------------------
                top_frame = tk.Frame(screen, bg='light blue', height=50, width=1600)
                lb_title = tk.Label(top_frame, text='AUTOMACTIC CHECK IN THE PARKING', font=('arial', 35),
                                    fg='dark blue',
                                    bg='light blue')
                lb_title.pack()
                def date_time():
                    s_time = datetime.datetime.now().strftime('%H:%M:%S, %d-%m-%Y')
                    s_time = f'{s_time}'
                    time_lb.config(text=s_time)
                    time_lb.after(100, date_time)
                time_lb = tk.Label(top_frame, bg='light blue', font=('Bold', 15))
                time_lb.pack()
                date_time()
                btn_signout = tk.Button(screen, text='SIGN OUT', font=('arial', 10), bg='red', fg='white',
                                        activebackground='#FF3366', activeforeground='black', border=1, width=15,
                                        command=sign_out)
                btn_signout.place(x=0, y=0)
                def setting():
                    pass
                btn_setting = tk.Button(screen, text='SETTING', font=('arial', 10), bg='green', fg='white',
                                        activebackground='light green', activeforeground='black', border=1, width=15,
                                        command=setting)
                btn_setting.place(x=150, y=0)
                lb_checkin = tk.Label(screen, text='Check In', bg='light blue', font=('Bold', 20))
                lb_checkin.place(x=300, y=50)
                lb_checkin = tk.Label(screen, text='Check Out', bg='light blue', font=('Bold', 20))
                lb_checkin.place(x=1100, y=50)
                top_frame.pack(side=tk.TOP)
# --------------------------------------------------------------------------------------------------------------------
                frame_in = tk.Frame(screen, bg='blue', height=650, width=750)
                lb_plate_in = tk.Label(frame_in)
                lb_face_in = tk.Label(frame_in)
                # def open_cam_in():
                def face_in():
                    ret_face, frame_face = cap_face.read()
                    frame_face = cv2.cvtColor(frame_face, cv2.COLOR_BGR2RGB)
                    #frame_face = frame_face[50: 400, 250: 580]
                    frame_face = Image.fromarray(frame_face).resize((350, 320))
                    frame_face = model(frame_face)
                    frame_face = np.squeeze(frame_face.render())
                    frame_face = Image.fromarray(frame_face)
                    frame_face = ImageTk.PhotoImage(frame_face)
                    lb_face_in.configure(image=frame_face)
                    lb_face_in.image = frame_face
                    lb_face_in.lift()
                    lb_face_in.update()
                    lb_face_in.after(2, face_in)
                    lb_face_in.place(x=0, y=0)

                def plate_in():
                    ret_plate, frame_plate = cap_plate.read()
                    frame_plate = cv2.cvtColor(frame_plate, cv2.COLOR_BGR2RGB)
                    frame_plate = frame_plate[50: 400, 250: 580]
                    frame_plate = model(frame_plate)
                    frame_plate = np.squeeze(frame_plate.render())
                    frame_plate = Image.fromarray(frame_plate).resize((350, 320))
                    frame_plate = ImageTk.PhotoImage(frame_plate)
                    lb_plate_in.imgtk = frame_plate
                    lb_plate_in.configure(image=frame_plate)
                    lb_plate_in.image = frame_plate
                    lb_plate_in.lift()
                    lb_plate_in.update()
                    lb_plate_in.after(1, plate_in)
                    lb_plate_in.place(x=0, y=330)

                def button_camin():
                    def toggle():
                        if sw_camin.config('relief')[-1] == 'sunken':
                            sw_camin.config(relief="raised", image=off)
                            lb_face_in.destroy()
                            cap_face.release()
                            lb_plate_in.destroy()
                            cap_plate.release()
                        else:
                            sw_camin.config(relief="sunken", image=on)
                            face_in()
                            plate_in()
                    lb_camin = tk.Label(screen, text='Camera In', font=('arial', 15), bg='light blue', fg='dark blue', border=1)
                    lb_camin.place(x=0, y=30)
                    on = tk.PhotoImage(file='on_sw.png')
                    off = tk.PhotoImage(file='off_sw.png')
                    sw_camin = tk.Button(screen, image=off, bd=0,  command=toggle, bg='light blue', border=0, width=80,
                                         height=26, activebackground='light blue', relief="raised")
                    sw_camin.place(x=100, y=30)
                button_camin()
                frame_in.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)
#---------------------------------------------------------------------------------------------------------------------
                frame_out = tk.Frame(screen, bg='gray', height=650, width=750)
                frame_out.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5)
# --------------------------------------------------------------------------------------------------------------------
                screen.pack(expand=True)

            elif (acc != 'Drand') & (pas != '1812'):
                screen = tk.Toplevel(windows)
                screen.title('ERROR Login')
                screen.geometry('620x72')
                screen.config(bg='gray')
                label_e = tk.Label(screen, text='Error!', font=('Bold', 15), fg='Red', bg='gray')
                label_e.pack(expand=True)
                label_t = tk.Label(screen, text='Incorrect Your Username or Password!', font=('Bold', 20), fg='Black',
                                   bg='gray')
                label_t.pack(expand=True)
                btn_error = tk.Button(screen, border=1, text='OK', font=('Bold', 10), fg='white', bg='red',
                                      activeforeground='white'
                                      , activebackground='#FF3366', command=screen.destroy)
                btn_error.pack(expand=True)
                screen.mainloop()
            elif (acc != 'Drand') & (pas == '1812'):
                screen = tk.Toplevel(windows)
                screen.title('ERROR Login')
                screen.geometry('620x72')
                screen.config(bg='gray')
                label_e = tk.Label(screen, text='Error!', font=('Bold', 15), fg='Red', bg='gray')
                label_e.pack(expand=True)
                label_t = tk.Label(screen, text='Incorrect Your Username', font=('Bold', 20), fg='Black',
                                   bg='gray')
                label_t.pack(expand=True)
                btn_error = tk.Button(screen, border=1, text='OK', font=('Bold', 10), fg='white', bg='red',
                                      activeforeground='white'
                                      , activebackground='#FF3366', command=screen.destroy)
                btn_error.pack(expand=True)
                screen.mainloop()
            elif (acc == 'Drand') & (pas != '1812'):
                screen = tk.Toplevel(windows)
                screen.title('ERROR Login')
                screen.geometry('620x72')
                screen.config(bg='gray')
                label_e = tk.Label(screen, text='Error!', font=('Bold', 15), fg='Red', bg='gray')
                label_e.pack(expand=True)
                label_t = tk.Label(screen, text='Incorrect Your Password!', font=('Bold', 20), fg='Black',
                                   bg='gray')
                label_t.pack(expand=True)
                btn_error = tk.Button(screen,border=1, text='OK', font=('Bold', 10), fg='white', bg='red', activeforeground='white'
                                      , activebackground='#FF3366', command=screen.destroy)
                btn_error.pack(expand=True)
                screen.mainloop()

        def remember_tick():
            pass

        def forward_register_acc():
            login.destroy()
            remember_lb.destroy()
            bottom_frame.destroy()
            label_frame.destroy()
            signup_page()

        def show_pass(command):
            if command == 'show':
                password_account.config(show='*')
                show_hide_password.config(image=img_show)
                show_hide_password.config(command=lambda: show_pass('hide'))
            else:
                password_account.config(show='')
                show_hide_password.config(image=img_hiden)
                show_hide_password.config(command=lambda: show_pass('show'))

        def on_enter(e):
            username_account.delete(0, 'end')

        def on_leave(e):
            name = username_account.get()
            if name == '':
                username_account.insert(0, 'Ex. Phudang')

        def on_enter_pass(e):
            password_account.delete(0, 'end')

        def on_leave_pass(e):
            name = password_account.get()
            if name == '':
                password_account.insert(0, 'Ex. 18122000')

        login = tk.Frame(windows, height=480, width=480, bg='white')

        def date_time():
            s_time = datetime.datetime.now().strftime('%d-%m-%Y, %Hh:%Mm:%Ss')
            s_time = f'{s_time}'
            time_lb.config(text=s_time)
            time_lb.after(100, date_time)

        time_lb = tk.Label(login, bg='white', font=('Bold', 10))
        time_lb.pack()
        date_time()

        login_lb = tk.Label(login, text='SIGN IN SYSTEM', bg='white', font=('Bold', 30), fg='dark Blue')
        login_lb.pack()

        user_lb = tk.Label(login, text='Username', bg='white', font=('Bold', 10), fg='gray')
        user_lb.pack()

        username_account = tk.Entry(login, width=25, border=0, bd=0, font=('Arial', 20), fg='#4F4F4F', bg='white',
                                    highlightcolor='dark blue',
                                    highlightthickness=2, highlightbackground='light blue')
        username_account.pack(pady=5)
        username_account.insert(0, 'Drand')
        username_account.bind('<FocusIn>', on_enter)
        username_account.bind('<FocusOut>', on_leave)

        pass_lb = tk.Label(login, text='Password', bg='white', font=('Bold', 10), fg='gray')
        pass_lb.pack()
        password_account = tk.Entry(login, width=25, border=0, bd=0, font=('Arial', 20), fg='#4F4F4F', bg='white',
                                    highlightcolor='dark blue',
                                    highlightthickness=2, show='*', highlightbackground='light blue')
        password_account.pack(pady=5)
        password_account.insert(0, '1812')
        password_account.bind('<FocusIn>', on_enter_pass)
        password_account.bind('<FocusOut>', on_leave_pass)
        show_hide_password = tk.Button(password_account, image=img_show, bd=0, bg='white',
                                       command=lambda: show_pass('hide'))
        show_hide_password.place(x=340, y=0)

        remember_lb = tk.Frame(login, bg='white')

        tick_remember = tk.Checkbutton(remember_lb, text='Remember me', font=('Bold', 10), bg='white', fg='black'
                                       , variable=x, onvalue=1, offvalue=0, command=remember_tick,
                                       activebackground='white')
        tick_remember.pack(side=tk.LEFT, padx=80)
        forgot_btn = tk.Button(remember_lb, text='Forgot Account?',
                               font=('Bold', 10),
                               bg='white', border=0, fg='dark blue', underline=True,
                               activebackground='white')
        forgot_btn.pack(side=tk.RIGHT, padx=80)

        remember_lb.pack()

        bottom_frame = tk.Frame(login, bg='white')
        cancel_btn = tk.Button(bottom_frame, text='Cancel',
                               font=('Bold', 15),
                               bg='dark blue', fg='white', width=10, border=0, command=windows.destroy,
                               activebackground='light blue')
        cancel_btn.pack(side=tk.RIGHT, padx=5)
        login_btn = tk.Button(bottom_frame, text='Login',
                              font=('Bold', 15),
                              bg='dark blue', fg='white', width=10, border=0, activebackground='light blue',
                              command=login_acc)
        login_btn.pack(side=tk.LEFT, padx=5)
        bottom_frame.pack(pady=5)

        label_frame = tk.Frame(login, bg='white')
        label_sign = tk.Label(label_frame, text="Don't have an account?",
                              font=('Bold', 12), bg='white', fg='black')
        label_sign.pack(side=tk.LEFT, padx=5)
        sign_btn = tk.Button(label_frame, text='Sign up Account',
                             font=('Bold', 12),
                             bg='white', border=0, fg='dark blue', underline=True, command=forward_register_acc,
                             activebackground='white')
        sign_btn.pack(side=tk.RIGHT, padx=0)
        label_frame.pack(pady=5)

        label_sign = tk.Label(login, text="Or sign in with",
                              font=('Bold', 12), bg='white', fg='black')
        label_sign.pack(pady=5)
        sign_btn = tk.Button(login, image=img_google)
        sign_btn.pack(pady=5)

        login.pack(expand=True)

    def signup_page():

        global img_login, img_google
        img_login = tk.PhotoImage(file='backgroung.png')
        img_label = tk.Label(windows, image=img_login, bg='#6699CC')
        img_label.place(x=0, y=0)
        img_hiden = tk.PhotoImage(file='show.png')
        img_show = tk.PhotoImage(file='hiden.png')
        img_google = tk.PhotoImage(file='button google.png')
        x = tk.IntVar()

        signup = tk.Frame(windows, bg='white')

        def remember_tick():
            pass

        def signup_acc():
            pass

        def forward_login_acc():
            signup.destroy()
            conditions_lb.destroy()
            bottom_frame.destroy()
            login_page()

        def show_pass(command):
            if command == 'show':
                password_account.config(show='*')
                show_hide_password.config(image=img_show)
                show_hide_password.config(command=lambda: show_pass('hide'))
            else:
                password_account.config(show='')
                show_hide_password.config(image=img_hiden)
                show_hide_password.config(command=lambda: show_pass('show'))

        def show_repass(command):
            if command == 'show':
                repassword_account.config(show='*')
                show_hide_repassword.config(image=img_show)
                show_hide_repassword.config(command=lambda: show_repass('hide'))
            else:
                repassword_account.config(show='')
                show_hide_repassword.config(image=img_hiden)
                show_hide_repassword.config(command=lambda: show_repass('show'))

        def on_enter(e):
            username_account.delete(0, 'end')

        def on_leave(e):
            name = username_account.get()
            if name == '':
                username_account.insert(0, 'Ex. Phudang')

        def on_enter_pass(e):
            password_account.delete(0, 'end')

        def on_leave_pass(e):
            name = password_account.get()
            if name == '':
                password_account.insert(0, 'Ex. 18122000')

        def on_enter_repass(e):
            repassword_account.delete(0, 'end')

        def on_leave_repass(e):
            name = repassword_account.get()
            if name == '':
                repassword_account.insert(0, 'Ex. 18122000')

        def date_time():
            s_time = datetime.datetime.now().strftime('%H:%M:%S, %d-%m-%Y')
            s_time = f'{s_time}'
            time_lb.config(text=s_time)
            time_lb.after(100, date_time)

        time_lb = tk.Label(signup, bg='white', font=('Bold', 10))
        time_lb.pack()
        date_time()

        login_lb = tk.Label(signup, text='SIGN UP SYSTEM', bg='white', font=('Bold', 30), fg='dark Blue')
        login_lb.pack()

        user_lb = tk.Label(signup, text='Username', bg='white', font=('Bold', 10), fg='gray')
        user_lb.pack()

        username_account = tk.Entry(signup, width=25, border=0, bd=0, font=('Arial', 20), fg='#4F4F4F', bg='white',
                                    highlightcolor='dark blue',
                                    highlightthickness=2, highlightbackground='light blue')
        username_account.pack(pady=5)
        username_account.insert(0, 'Ex. Phudang')
        username_account.bind('<FocusIn>', on_enter)
        username_account.bind('<FocusOut>', on_leave)

        pass_lb = tk.Label(signup, text='Password', bg='white', font=('Bold', 10), fg='gray')
        pass_lb.pack()
        password_account = tk.Entry(signup, width=25, border=0, bd=0, font=('Arial', 20), fg='#4F4F4F', bg='white',
                                    highlightcolor='dark blue',
                                    highlightthickness=2, show='*', highlightbackground='light blue')
        password_account.pack(pady=5)
        password_account.insert(0, 'Ex. 18122000')
        password_account.bind('<FocusIn>', on_enter_pass)
        password_account.bind('<FocusOut>', on_leave_pass)
        show_hide_password = tk.Button(password_account, image=img_show, bd=0, bg='white',
                                       command=lambda: show_pass('hide'))
        show_hide_password.place(x=340, y=0)

        repass_lb = tk.Label(signup, text='Re-Password', bg='white', font=('Bold', 10), fg='gray')
        repass_lb.pack()
        repassword_account = tk.Entry(signup, width=25, border=0, bd=0, font=('Arial', 20), fg='#4F4F4F', bg='white',
                                      highlightcolor='dark blue',
                                      highlightthickness=2, show='*', highlightbackground='light blue')
        repassword_account.pack(pady=5)
        repassword_account.insert(0, 'Ex. 18122000')
        repassword_account.bind('<FocusIn>', on_enter_repass)
        repassword_account.bind('<FocusOut>', on_leave_repass)

        show_hide_repassword = tk.Button(repassword_account, image=img_show, bd=0, bg='white',
                                         command=lambda: show_repass('hide'))
        show_hide_repassword.place(x=340, y=0)

        conditions_lb = tk.Frame(signup, bg='white')

        tick_condi = tk.Checkbutton(conditions_lb, text='I read and agree to', font=('Bold', 10), bg='white', fg='black'
                                    , variable=x, onvalue=1, offvalue=0, command=remember_tick,
                                    activebackground='white')
        tick_condi.pack(side=tk.LEFT, padx=60)
        terms_btn = tk.Button(conditions_lb, text='Terms & Conditions',
                              font=('Bold', 10),
                              bg='white', border=0, fg='dark blue', underline=True,
                              activebackground='white')
        terms_btn.pack(side=tk.RIGHT, padx=60)

        conditions_lb.pack()

        bottom_frame = tk.Frame(signup, bg='white')
        return_btn = tk.Button(bottom_frame, text='Return',
                               font=('Bold', 15),
                               bg='dark blue', fg='white', width=10, border=0, command=forward_login_acc,
                               activebackground='dark blue')
        return_btn.pack(side=tk.RIGHT, padx=5)
        login_btn = tk.Button(bottom_frame, text='Create',
                              font=('Bold', 15),
                              bg='dark blue', fg='white', width=10, border=0, activebackground='dark blue',
                              command=signup_acc)
        login_btn.pack(side=tk.LEFT, padx=5)
        bottom_frame.pack(pady=5)

        label_sign = tk.Label(signup, text="Or sign up with",
                              font=('Bold', 12), bg='white', fg='black')
        label_sign.pack(pady=5)
        sign_btn = tk.Button(signup, image=img_google)
        sign_btn.pack(pady=5)

        signup.pack(expand=True)

    login_page()
    windows.mainloop()
main()
