#face detection
import cv2

img = cv2.imread("images/example6.png")

# Check if image loaded successfully
if img is None:
    print("Error: Could not load image from 'images/example3.png'")
else:
    gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Use the correct path to the cascade file
    f = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Check if cascade loaded successfully
    if f.empty():
        print("Error: Could not load cascade classifier")
    else:
        d = f.detectMultiScale(gry, 2, 2)

        for (x, y, w, h) in d:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow("wscube tech", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()