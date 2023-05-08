import glob
import cv2
import emailing
import os
from threading import Thread

# Blue Green Red

video = cv2.VideoCapture(0)

# To wait for camera to load if needed
# time.sleep(1)
first_frame = None
status_list = []
count = 1


def clean_folder():
    # Clean the folder
    images = glob.glob('images/*.png')
    for image in images:
        os.remove(image)

while True:
    status = 0
    # Loading the video
    check, frame = video.read()

    # Set the gray scale as it contains low amount of data compared to BlueGreenRed
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # To make the calculation more efficient by blurring
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # Capturing the first frame that we will use for comparison
    if first_frame is None:
        first_frame = gray_frame_gau

    # Check for difference
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # comparing the black == 0  and white == 255
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]

    # make the thresh_frame wider, more open
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow('My video', dil_frame)

    # Find contours
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Setting object size to check in case the object is a fake object
    # So we will eliminate the white false positives areas

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            # Saving video to image
            cv2.imwrite(f'images/{count}.png', frame)
            count += 1
            # Taking all images in variable
            all_images = glob.glob('images/*.png')
            # Taking the middle one for email attachment as taking the length of the all_images list divided by half
            image = all_images[int(len(all_images) / 2)]

    # Using status and values of 0 and 1 to check when the object will exit the camera so the email will be sent then
    status_list.append(status)
    status_list = status_list[-2:]
    if status_list[0] == 1 and status_list[1] == 0:
        # Creating a thread for sending email, making args to tuple with comma to avoid an error
        email_thread = Thread(target=emailing.send_email, args=(image, ))
        # Allowing the thread to be executed in the  background
        email_thread.daemon = True
        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True

        # calling the threads
        email_thread.start()
        clean_thread.start()



    cv2.imshow('Video', frame)


    # Create a keyboard object
    key = cv2.waitKey(1)
    # If the user press that button the video will stop
    if key == ord('q'):
        break

video.release()
