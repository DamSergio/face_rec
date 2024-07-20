import sys
import os
import shutil
import face_recognition
import tkinter as tk

from PIL import Image, ImageTk
from pathlib import Path

KNOWN_FACES_DIR = "C:\\ProgramsCLI\\known_faces"
IMAGES_DIR = f"{Path.home()}\\Pictures"
known_faces = {}


def get_face_img(face: tuple[int, any, any, int], image) -> Image:
    top, right, bottom, left = face
    face_image = image[top:bottom, left:right]
    pil_image = Image.fromarray(face_image)

    return pil_image


def ask_name(
    image: Image,
    original_image: str,
    possible_match: str | None = None,
    confidence: None | float | str = None,
) -> None:
    global known_faces

    def submit_name() -> None:
        name = name_entry.get()
        if name:
            save_image(original_image, name)

        if name not in known_faces.keys():
            image.save(f"{KNOWN_FACES_DIR}/{name}.{original_image.split('.')[1]}")
            image_path = os.path.join(
                KNOWN_FACES_DIR, f"{name}.{original_image.split('.')[1]}"
            )
            img = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(img)
            known_faces[name] = face_encodings[0]

            print(f"Added {name} to known faces.")

        root.quit()

    def cancel() -> None:
        root.quit()

    try:
        root = tk.Tk()
        root.title("Name")
        root.geometry("500x500")

        img = image.resize((250, 250))
        img_tk = ImageTk.PhotoImage(img)
        img_label = tk.Label(root, image=img_tk)
        img_label.image = img_tk
        img_label.pack()

        name_label = tk.Label(root, text="Enter name:")
        name_label.pack()

        name_entry = tk.Entry(root)
        if possible_match:
            name_entry.insert(0, possible_match)

        name_entry.pack()

        if confidence:
            confidence_label = tk.Label(
                root, text=f"Confidence: {confidence * 100:.2f}%"
            )
            confidence_label.pack()

        else:
            confidence_label = tk.Label(root, text="Unknown person.")
            confidence_label.pack()

        submit_button = tk.Button(root, text="Submit", command=submit_name)
        submit_button.pack()

        cancel_button = tk.Button(root, text="Cancel", command=cancel)
        cancel_button.pack()

        root.mainloop()
        root.destroy()

    except Exception as e:
        print(f"Error: {e}")


def save_image(image_name: str, person_name: str) -> None:
    try:
        os.makedirs(f"{IMAGES_DIR}/{person_name}", exist_ok=True)
        shutil.copy(image_name, f"{IMAGES_DIR}/{person_name}/{image_name}")
        print(f"Image saved as {image_name} in {person_name} dir.")

    except Exception as e:
        print(f"Error: {e}")


def load_known_faces() -> None:
    global known_faces

    faces = os.listdir(KNOWN_FACES_DIR)
    for face in faces:
        if face.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(KNOWN_FACES_DIR, face)
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)
            if face_encodings:
                known_faces[face.split(".")[0]] = face_encodings[0]

    print(f"Loaded {len(known_faces)} known faces.")


def scan_foler(path: str = ".") -> None:
    try:
        files = os.listdir(path)
        for file in files:
            if not file.lower().endswith(("jpg", "jpeg", "png")):
                continue

            print(f"Scanning {file}...")
            image_path = os.path.join(path, file)
            image = face_recognition.load_image_file(image_path)
            face_locations = face_recognition.face_locations(image)
            if not face_locations:
                print(f"No faces found in {file}.")
                continue

            print(f"Found {len(face_locations)} face(s) in {file}.")

            face_encodings = face_recognition.face_encodings(image, face_locations)
            for index, face_encoding in enumerate(face_encodings):
                matches = face_recognition.compare_faces(
                    list(known_faces.values()), face_encoding
                )
                face_distances = face_recognition.face_distance(
                    list(known_faces.values()), face_encoding
                )
                best_match_index = None
                if matches:
                    best_match_index = min(
                        enumerate(face_distances), key=lambda x: x[1]
                    )[0]

                pil_image = get_face_img(face_locations[index], image)

                if best_match_index is not None:
                    match = list(known_faces.keys())[best_match_index]
                    confidence = 1 - face_distances[best_match_index]
                    print(
                        f"Match found: {match} with {confidence * 100:.2f}% confidence."
                    )
                    print(f"cofidence: {confidence}")

                    if confidence >= 0.80:
                        save_image(file, match)

                    elif confidence >= 0.30:
                        ask_name(pil_image, file, match, confidence)

                    else:
                        ask_name(pil_image, file)

                else:
                    print("No match found.")
                    ask_name(pil_image, file)

                print("\n-----------------------------\n")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    load_known_faces()

    if len(sys.argv) > 1:
        scan_foler(sys.argv[1])

    else:
        scan_foler()
