import face_recognition
import cv2
import os

OWNER_IMAGE = "owner_face.jpg"

# 🚀 FACE REGISTRATION
if not os.path.exists(OWNER_IMAGE):

    print("🚀 SNOWY FACE REGISTRATION")
    print("📸 Press SPACE to register your face")
    print("❌ Press ESC to exit")

    cam = cv2.VideoCapture(0)

    while True:

        ret, frame = cam.read()

        if not ret:
            print("❌ Camera error.")
            break

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        face_locations = face_recognition.face_locations(
            rgb_frame
        )

        # 🟢 DRAW FACE BOX
        for (top, right, bottom, left) in face_locations:

            cv2.rectangle(
                frame,
                (left, top),
                (right, bottom),
                (0, 255, 255),
                2
            )

        cv2.putText(
            frame,
            "Press SPACE to Capture Face",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

        cv2.imshow(
            "SNOWY Face Registration",
            frame
        )

        key = cv2.waitKey(1)

        # SPACE
        if key == 32:

            if len(face_locations) == 0:

                print("❌ No face detected.")
                print("⚠️ Please center your face.")

            else:

                cv2.imwrite(
                    OWNER_IMAGE,
                    frame
                )

                print("✅ Owner face registered successfully.")

                break

        # ESC
        elif key == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

# 🔐 FACE VERIFICATION
else:

    print("🔐 SNOWY FACE VERIFICATION")
    print("📸 Looking for authorized user...")

    known_image = face_recognition.load_image_file(
        OWNER_IMAGE
    )

    known_encodings = face_recognition.face_encodings(
        known_image
    )

    # 🚨 SAFETY CHECK
    if len(known_encodings) == 0:

        print("❌ No face detected in owner image.")
        print("🗑️ Delete owner_face.jpg and register again.")

        exit()

    known_encoding = known_encodings[0]

    cam = cv2.VideoCapture(0)

    verified = False

    while True:

        ret, frame = cam.read()

        if not ret:
            print("❌ Camera error.")
            break

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        face_locations = face_recognition.face_locations(
            rgb_frame
        )

        face_encodings = face_recognition.face_encodings(
            rgb_frame
        )

        # 🟢 DRAW BOXES
        for (top, right, bottom, left) in face_locations:

            cv2.rectangle(
                frame,
                (left, top),
                (right, bottom),
                (0, 255, 255),
                2
            )

        # 🧠 VERIFY FACE
        for face_encoding in face_encodings:

            matches = face_recognition.compare_faces(
                [known_encoding],
                face_encoding,
                tolerance=0.50
            )

            face_distance = face_recognition.face_distance(
                [known_encoding],
                face_encoding
            )

            print(
                f"🔍 Face Distance: {face_distance[0]}"
            )

            if True in matches:

                verified = True

                cv2.putText(
                    frame,
                    "ACCESS GRANTED",
                    (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    3
                )

                print(
                    "✅ Identity confirmed."
                )

                print(
                    "🤖 Welcome back Kshitij."
                )

                break

        cv2.imshow(
            "SNOWY Face Verification",
            frame
        )

        if verified:

            cv2.waitKey(2000)

            break

        # ESC KEY
        if cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

    if not verified:

        print("❌ Face not recognized.")