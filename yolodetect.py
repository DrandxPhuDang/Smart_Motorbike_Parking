import time
import cv2
import numpy as np
import torch.hub
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import glob
import matplotlib.pyplot as plt
import PIL
import pytesseract
import datetime
import os
from tkinter import *
import shutil
import face_recognition


#DEF MAIN
def all():
    #DEF DELETE FOLDER
    def createFolder(dicret):
        try:
            if not os.path.exists(dicret):
                os.makedirs(dicret)
        except OSError:
            print('No creating folder')
    #DEF PASS
    def nothing(x):
        pass
    fps_reader = cvzone.FPS()
    cv2.namedWindow('Tracking_Face')
    cv2.createTrackbar("MinH_face", "Tracking_Face", 0, 255, nothing)
    cv2.createTrackbar('MinS_face', 'Tracking_Face', 0, 255, nothing)
    cv2.createTrackbar('MinV_face', 'Tracking_Face', 190, 255, nothing)
    cv2.createTrackbar('MaxH_face', 'Tracking_Face', 255, 255, nothing)
    cv2.createTrackbar('MaxS_face', 'Tracking_Face', 255, 255, nothing)
    cv2.createTrackbar('MaxV_face', 'Tracking_Face', 255, 255, nothing)
    #DEFINE
    n = 0
    s = 0
    dem = 0

    #CREATE MODEL MODE
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    segmentor = SelfiSegmentation()
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='Plate_Face_best (9).pt', force_reload=True)
    path = glob.glob("/content/yolov5/runs/detect/exp/FrameVid1_185.JPG")
    remove_BR = cv2.createBackgroundSubtractorMOG2()

    # DEFINE CAMERA
    video_detect = 'video detect 1.mp4'
    ip = 'http://192.168.1.7:4747/video'
    cap_plate = cv2.VideoCapture(video_detect)
    cap_face = cv2.VideoCapture(0)

    def start():
        prev_frame_time = 0
        new_frame_time = 0
        if n == 0:
            #RESET FOLDER WHEN DATE TIME 00:00
            Timer_delete_folder = datetime.datetime.now().strftime('%H:%M:%S')
            Timer_delete_folder = f'{Timer_delete_folder}'
            final_time_delete = ''
            for text_img in Timer_delete_folder:
                 if text_img.isalnum():
                     final_time_delete += text_img
                     if final_time_delete == '000000':
                        shutil.rmtree('License plate', ignore_errors=True)
                        if final_time_delete == '000000':
                            print('Deleting folder....')
                            while final_time_delete != '000000':
                                break

            #RESET FOLDER WHEN STARTING
            shutil.rmtree('License plate', ignore_errors=True)
            shutil.rmtree('Face', ignore_errors=True)
            #PUT TEXT DATE TIME
            font = cv2.FONT_HERSHEY_SIMPLEX
            color = (255, 0, 0)
            stroke = 1
            s_time = datetime.datetime.now().strftime('%d-%m-%Y, %Hh:%Mm:%Ss')
            cv2.putText(frame_results_face, s_time, (0, 20), font, 0.5, color, stroke, cv2.LINE_AA)
            cv2.putText(frame_results, s_time, (0, 20), font, 0.5, color, stroke, cv2.LINE_AA)
            #SHOW FRAME
            ver = np.vstack((frame_results_face, frame_results))
            new_frame_time = time.time()
            fps = 1 / (new_frame_time - prev_frame_time)
            prev_frame_time = new_frame_time
            fps = int(fps)
            fps = str(fps)
            cv2.putText(ver, fps, (20, 670), font, 2, (100, 255, 0), 3, cv2.LINE_AA)
            #_, final_frame_stack = fps_reader.update(ver)
            cv2.imshow('BAI GIU XE TU DONG', ver)

    def next():
        global threshold_2, crop_frame, face_result, number_string, ki_tu_thu_3, int_number, crop_frame_face_2, \
            blur_crop_frame_face, final_img_detect_face, checkin, checkout, results_encoding, text_img
        if n > 0:
            #READ IMAGES DETECT
            img_detect_plate = cv2.imread(f'License plate/License plate {n}/crops/License Plate/image0.jpg')
            img_detect_face = cv2.imread(f'Face/Face {n}/crops/Face/image0.jpg')
            img_detect_face = cv2.cvtColor(img_detect_face, cv2.COLOR_RGB2BGR)
            img_detect_plate = cv2.resize(img_detect_plate, None, fx=2, fy=2)

            min_h_face = cv2.getTrackbarPos("MinH_face", 'Tracking_Face')
            min_s_face = cv2.getTrackbarPos("MinS_face", 'Tracking_Face')
            min_v_face = cv2.getTrackbarPos("MinV_face", 'Tracking_Face')
            max_h_face = cv2.getTrackbarPos("MaxH_face", 'Tracking_Face')
            max_s_face = cv2.getTrackbarPos("MaxS_face", 'Tracking_Face')
            max_v_face = cv2.getTrackbarPos("MaxV_face", 'Tracking_Face')
            frame_hsv_face = cv2.cvtColor(img_detect_face, cv2.COLOR_BGR2HSV)
            min_img_hsv_face = np.array([min_h_face, min_s_face, min_v_face])
            max_img_hsv_face = np.array([max_h_face, max_s_face, max_v_face])
            mask_face = cv2.inRange(frame_hsv_face, min_img_hsv_face, max_img_hsv_face)
            pro_img_face = cv2.bitwise_and(img_detect_face, img_detect_face, mask=mask_face)
            mask_pro_img_face = cvzone.stackImages([mask_face, pro_img_face], 2, 1)

            img_detect_plate = cv2.cvtColor(img_detect_plate, cv2.COLOR_RGB2BGR)
            img_detect_plate = cv2.cvtColor(img_detect_plate, cv2.COLOR_BGR2GRAY)
            img_detect_plate = cv2.GaussianBlur(img_detect_plate, (5, 5), 0)
            _, thresh = cv2.threshold(img_detect_plate, 120, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            contours_face, _ = cv2.findContours(mask_face, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

            #LOOP CONTOURS PLATE
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 2000:
                    x, y, w, h = cv2.boundingRect(cnt)
                    cv2.rectangle(img_detect_plate, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    crop_frame = img_detect_plate[y:y + h, x:x + w]
                    crop_frame = cv2.resize(crop_frame, None, fx=2, fy=2)
                    crop_frame = cv2.GaussianBlur(crop_frame, (5, 5), 0)
                    threshold_2 = cv2.adaptiveThreshold(crop_frame, 255,
                                                        cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 57, 15)
                    kernel = np.ones((2, 2), np.uint8)
                    threshold_2 = cv2.dilate(threshold_2, kernel, iterations=1)

                    threshold_2 = cv2.morphologyEx(threshold_2, cv2.MORPH_OPEN, kernel, iterations=1)
                    invert = 255 - threshold_2
                    # READ TEXT IN IMAGES
                    text_img = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')
                    print(text_img)
            #COUNT LETTER IN STRING
            final_text_img = ''
            for text_img in text_img:
                if text_img.isalnum():
                    final_text_img += text_img
                    number_string = len(final_text_img)
            #LOOP CONTOURS FACE
            for cnt_face in contours_face:
                area_face = cv2.contourArea(cnt_face)
                if area_face > 3500:
                    x_face, y_face, w_face, h_face = cv2.boundingRect(cnt_face)
                    cv2.rectangle(img_detect_face, (x_face, y_face), (x_face + w_face, y_face + h_face), (0, 255, 0), 2)
                    crop_frame_face_2 = img_detect_face[y_face:y_face + h_face, x_face:x_face + w_face]
                    final_img_detect_face = cv2.resize(crop_frame_face_2, None, fx=2, fy=2)
                    #final_img_detect_face = cv2.cvtColor(final_img_detect_face, cv2.COLOR_GRAY2RGB)
            #RESIZE IMAGES
            final_img_detect_face = cv2.resize(final_img_detect_face, (330, 350), fx=1, fy=1)
            crop_frame = cv2.resize(crop_frame, (330, 350), fx=1, fy=1)
            threshold_2 = cv2.resize(threshold_2, (330, 350), fx=1, fy=1)
            #PUT TEXT IN FRAME
            font = cv2.FONT_HERSHEY_SIMPLEX
            color = (255, 0, 0)
            stroke = 1
            s_time = datetime.datetime.now().strftime('%d-%m-%Y, %Hh:%Mm:%Ss')
            s_time = f'{s_time}'
            cv2.putText(frame_results_face, s_time, (0, 20), font, 0.5, color, stroke, cv2.LINE_AA)
            cv2.putText(frame_results, s_time, (0, 20), font, 0.5, color, stroke, cv2.LINE_AA)
            cv2.putText(final_img_detect_face, f' ID {final_text_img}', (0, 330),
                                                               font, 1, color, stroke, cv2.LINE_AA)
            #cv2.putText(final_img_detect_face, f' ID {final_text_img}', (0, 330),
                        #font, 1, color, stroke, cv2.LINE_AA)
            # CONDITION TO SAVING
            # letter_string = final_text_img[2]
            # letter_string_3 = final_text_img[3]
            # ini_string1 = '1234567890'
            # S_2 = f"{letter_string}"
            # S_3 = f"{letter_string_3}"
            # print("character_to_find: ", S_2)
            # print("ID LICENSE PLATE: ", final_text_img)
            # try:
            #     res_2 = ini_string1.index(S_2)
            #     res_3 = ini_string1.index(S_3)
            # except ValueError as e:
            #     cv2.putText(final_img_detect_face, f' ID {final_text_img}', (0, 330),
            #                                                                 font, 1, color, stroke, cv2.LINE_AA)
            #STACK IMAGES
            ver = np.vstack((frame_results_face, frame_results))
            final_stack = cvzone.stackImages([final_img_detect_face, crop_frame], 1, 1)
            final_frame_stack = cvzone.stackImages([ver, final_stack], 2, 1)
            #SAVE IMAGES AND ID RESULTS
            if cv2.waitKey(1) & 0xff == ord('s'):
                createFolder(f'DATA SPACE Input/{final_text_img}')
                s_time = datetime.datetime.now().strftime('(%d-%m, %Hh %Mm)')
                s_time_ID = datetime.datetime.now().strftime('(%d-%m-%Y, %Hh %Mm)')
                s_time = f'{s_time}'
                s_time_ID = f'{s_time_ID}'
                file_name_plate = f'DATA SPACE Input/{final_text_img}/License plate_{final_text_img}.png'
                cv2.imwrite(file_name_plate, crop_frame)
                file_name_face = f'DATA SPACE Input/{final_text_img}/Face_{final_text_img}.png'
                cv2.imwrite(file_name_face, final_img_detect_face)
                ID = f'{final_text_img}_{s_time_ID}'
                f = open(f'DATA SPACE Input/{final_text_img}/ID {final_text_img}.txt', 'a')
                f.write('ID ')
                f.write(ID+'\n')
                f.close()
                cv2.destroyWindow('BAI GIU XE TU DONG')
#---------------------------------------------------------- OUTPUT-----------------------------------------------------
            # SAVE IMAGES AND ID RESULTS
            if cv2.waitKey(2) & 0xff == ord('c'):
                createFolder(f'DATA SPACE Output/{final_text_img}')
                s_time = datetime.datetime.now().strftime('(%d-%m, %Hh %Mm)')
                s_time_ID = datetime.datetime.now().strftime('(%d-%m-%Y, %Hh %Mm)')
                s_time = f'{s_time}'
                s_time_ID = f'{s_time_ID}'
                file_name_plate = f'DATA SPACE Output/{final_text_img}/License plate_{final_text_img}.png'
                cv2.imwrite(file_name_plate, crop_frame)
                file_name_face = f'DATA SPACE Output/{final_text_img}/Face_{final_text_img}.png'
                cv2.imwrite(file_name_face, final_img_detect_face)
                ID = f'{final_text_img}_{s_time_ID}'
                f = open(f'DATA SPACE Output/{final_text_img}/ID {final_text_img}.txt', 'a')
                f.write('ID ')
                f.write(ID + '\n')
                f.close()
                cv2.destroyWindow('BAI GIU XE TU DONG')
# ----------------------------------------------------------------------------------------------------------------------
            #SHOW FRAMES
            #_, final_frame_stack = fps_reader.update(ver)
            cv2.imshow('Tresholds', threshold_2)
            cv2.imshow('BAI GIU XE TU DONG', final_frame_stack)
    #MAIN LOOP
    while True:
        ret, frame_plate = cap_plate.read()
        ret_face, frame_face = cap_face.read()
        if (ret):
            # RESIZE SAME FRAME
            roi = frame_plate[50: 400, 250: 580]
            crop_frame_face = cv2.resize(frame_face, (330, 350), fx=1, fy=1)
            copy_roi = roi.copy()
            # RESULTS DETECTION
            results = model(roi)
            results_face = model(crop_frame_face)
            frame_results = np.squeeze(results.render())
            frame_results_face = np.squeeze(results_face.render())
            # CONVERT TO DETECTING
            if cv2.waitKey(1) & 0xff == ord('t'):
                n = n + 1
                crops = results.crop(save=True, save_dir=f'License plate/License plate {n}')
                crops_face = results_face.crop(save=True, save_dir=f'Face/Face {n}')
            # RESET SYSTEM
            if cv2.waitKey(1) & 0xff == ord('r'):
                n = 0
                cv2.destroyWindow('BAI GIU XE TU DONG')
            # DEF WORKING
            start()
            next()
            # EXIT WINDOWS
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
    #RELEASE CAMERA
    cap_plate.release()
    cv2.destroyAllWindows()
#CALL DEF MAIN
if __name__ == '__main__':
    all()
