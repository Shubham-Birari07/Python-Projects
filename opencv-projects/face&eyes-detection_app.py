""" -------  the final project face detection app  ------ """

import cv2

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

smile_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_smile.xml"
)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    """
    detectMiltiSacle helps in scan & detect faces,
    1.1 is scale-factor means zoom-in after each fram to find face,
    minNeighbors 5 because focus for checking image
    """

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    """
    x,y - top=left corner
    (x=w,y+h)

    face = [
    (100,150,80,80) face1
    (200,120,90,90) face2
    ]

    x - how far from left to right
    y - how far from top
    w - width of face
    h - height of face
    """

    roi_gray = gray[y:y + h, x:x + w]
    roi_color = frame[y:y + h, x:x + w]

    """
    this 2 line code will cut/crop the face frame so computer find eye & smile in face frame box

    x = 100
    y = 150
    w = 80
    h = 80

    (100,150)
    w = 80 > 180
    h = 80 > 230
    """

    eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 10)
    if len(eyes) > 0:
        cv2.putText(frame, "eye detected", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    smile = smile_cascade.detectMultiScale(roi_gray, 1.7, 20)
    if len(smile) > 0:
        cv2.putText(frame, "smile detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("Smart face detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
