import face_recognition
from PIL import Image
import os


def save_images(path: str = "./faces") -> None:
    try:
        files = os.listdir(path)
        for file in files:
            if not file.lower().endswith(("jpg", "jpeg", "png")):
                continue

            image_path = os.path.join(path, file)
            image = face_recognition.load_image_file(image_path)
            face_locations = face_recognition.face_locations(image)
            if not face_locations:
                print(f"No faces found in {file}.")
                continue

            print(f"Found {len(face_locations)} face(s) in {file}.")
            for face in face_locations:
                top, right, bottom, left = face
                face_image = image[top:bottom, left:right]
                pil_image = Image.fromarray(face_image)
                pil_image.save(
                    f"C:/ProgramsCLI/known_faces/{file.split('.')[0]}.{file.split('.')[1]}"
                )

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    save_images()
