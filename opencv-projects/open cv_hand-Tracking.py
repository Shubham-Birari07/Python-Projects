#Hand Tracking

import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,               # track up to 2 hands
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

# Landmark indices for fingertips and finger joints
# Thumb: 4(tip), 3(IP), 2(MCP)
# Index: 8(tip), 7(PIP), 6(MCP)
# Middle: 12(tip), 11(PIP), 10(MCP)
# Ring: 16(tip), 15(PIP), 14(MCP)
# Pinky: 20(tip), 19(PIP), 18(MCP)
FINGER_TIPS = [4, 8, 12, 16, 20]
FINGER_PIP  = [3, 7, 11, 15, 19]   # PIP joint (or IP for thumb)

def count_fingers(hand_landmarks, handedness):
    """
    Count raised fingers for one hand.
    hand_landmarks: list of normalized landmarks
    handedness: "Left" or "Right" (MediaPipe's classification)
    Returns: number of fingers up (0-5)
    """
    # If landmarks are in a list of NormalizedLandmark objects, extract x,y
    if not hand_landmarks:
        return 0

    # For thumb: compare tip x with IP x (horizontal check)
    # For other fingers: compare tip y with PIP y (vertical check)
    fingers_up = 0

    # Thumb
    thumb_tip = hand_landmarks.landmark[FINGER_TIPS[0]]
    thumb_ip  = hand_landmarks.landmark[FINGER_PIP[0]]
    # Depending on the hand side, thumb up condition differs:
    if handedness == "Right":
        # Right hand: thumb is to the left of the hand, so tip x < ip x when up
        if thumb_tip.x < thumb_ip.x:
            fingers_up += 1
    else:  # Left hand
        if thumb_tip.x > thumb_ip.x:
            fingers_up += 1

    # Index, Middle, Ring, Pinky
    for tip_id, pip_id in zip(FINGER_TIPS[1:], FINGER_PIP[1:]):
        tip = hand_landmarks.landmark[tip_id]
        pip = hand_landmarks.landmark[pip_id]
        # Finger is up if tip is higher (lower y) than PIP
        if tip.y < pip.y:
            fingers_up += 1

    return fingers_up

def get_hand_bbox(hand_landmarks, image_shape):
    """
    Calculate bounding box coordinates from hand landmarks.
    Returns (x_min, y_min, x_max, y_max) in pixel coordinates.
    """
    h, w, _ = image_shape
    x_coords = [lm.x * w for lm in hand_landmarks.landmark]
    y_coords = [lm.y * h for lm in hand_landmarks.landmark]
    x_min, x_max = int(min(x_coords)), int(max(x_coords))
    y_min, y_max = int(min(y_coords)), int(max(y_coords))
    return x_min, y_min, x_max, y_max

# Start webcam
cap = cv2.VideoCapture(0)

print("Press 'q' to quit.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Flip horizontally for a mirror view
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame
    results = hands.process(rgb)

    # Draw landmarks and count fingers if hands detected
    if results.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # Get handedness label
            hand_label = results.multi_handedness[idx].classification[0].label  # "Left" or "Right"

            # Draw hand landmarks and connections
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Count fingers
            fingers = count_fingers(hand_landmarks, hand_label)

            # Get bounding box
            x_min, y_min, x_max, y_max = get_hand_bbox(hand_landmarks, frame.shape)

            # Draw bounding box
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            # Put finger count beside the box (top-right of the box)
            text = f"Fingers: {fingers}"
            text_x = x_max + 10 if x_max + 150 < frame.shape[1] else x_min - 150
            text_y = y_min - 10 if y_min > 30 else y_max + 30

            cv2.putText(frame, text, (text_x, text_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

    # Show output
    cv2.imshow("Hand Tracking & Finger Counting", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



