from deepface import DeepFace
import cv2
import threading
import time
from tkinter import messagebox
import helper as helper
import utils_rotate as utils_rotate
import PySimpleGUI as sg
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
from PIL import ImageTk, Image
import imutils
from tkinter import ttk
import face_recognition
import xlsxwriter
import serial

def face_re():
        dirimg = f'D:\Python\CUSTOMDATA\DATA SPACE Input\95G105536\Face_95G105536.png'
        img = face_recognition.load_image_file(f'D:\Python\CUSTOMDATA\DATA SPACE Input\95G109189\Face_95G109189.png')
        height, width, _ = img.shape
        face_location = (0, width, height, 0)
        encodings = face_recognition.face_encodings(img, known_face_locations=[
            face_location])
        if len(encodings) > 0:
            results_encoding = encodings[0]
        else:
            print("No faces found in the image!")
            quit()

        dirimgout = f'D:\Python\CUSTOMDATA\DATA SPACE Output\95G105536\Face_95G105536.png'
        imgout = face_recognition.load_image_file(
            f'D:\Python\CUSTOMDATA\DATA SPACE Output\95G109189\Face_95G109189.jpg')
        heightout, widthout, _ = imgout.shape
        face_locationout = (0, widthout, heightout, 0)
        encodingsout = face_recognition.face_encodings(imgout, known_face_locations=[
            face_locationout])
        if len(encodingsout) > 0:
            results_encodingout = encodingsout[0]
        else:
            print("No faces found in the imageout!")
            quit()

        results_re = face_recognition.compare_faces([results_encoding], results_encodingout)
        output = DeepFace.verify(f"{dirimg}", f"{dirimgout}")
        output = output["verified"]
        print(output)
        if results_re[0] == True:
            print(True)

        if results_re[0] == False:
            print(False)

face_re()