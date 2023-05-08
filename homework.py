import cv2
import streamlit as st
import time

st.title('Monitor Detector')
start = st.button('Start Camera')

if start:
    streamlit_image = st.image([])
    camera = cv2.VideoCapture(0)

    while True:
        check, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Set two texts for day and time
        cv2.putText(img=frame, text=time.strftime('%A'), org=(10, 50),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(255, 255, 255),
                    thickness=2, lineType=cv2.LINE_AA)

        cv2.putText(img=frame, text=time.strftime('%H:%M:%S'), org=(10, 80),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(255, 0, 0),
                    thickness=2, lineType=cv2.LINE_AA)

        streamlit_image.image(frame)
