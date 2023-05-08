import cv2

# Blue Green Red

video = cv2.VideoCapture(0)

# To wait for camera to load if needed
# time.sleep(1)

while True:
    check, frame = video.read()
    cv2.imshow('My video', frame)

# Create a keyboard object
    key = cv2.waitKey(1)
# If the user press that button the video will stop
    if key == ord('q'):
        break

video.release()