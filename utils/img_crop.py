import numpy as np
from ultralyticsplus import YOLO
import cv2
import os

# Charger le modèle YOLOv8 pré-entraîné
model = YOLO('kesimeg/yolov8n-clothing-detection')  # Utilisez un modèle léger comme yolov8n pour commencer.

# Dossier des images
input_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")  # Dossier où se trouvent les images
output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")  # Dossier où les images traitées seront sauvegardées

# Vérifier si le dossier de sortie existe, sinon, le créer
os.makedirs(output_folder, exist_ok=True)

target_label = 'clothing'

# Parcourir tous les fichiers du dossier 'img' dont le nom commence par 'A_'
for filename in os.listdir(input_folder):
    if not filename.startswith('A_'):  # Filtrer par extension d'image
        continue

    image_path = os.path.join(input_folder, filename)

    # Charger l'image
    image = cv2.imread(image_path)

    # Détecter des objets dans l'image
    results = model(image)

    # Extraire les résultats de détection (boîtes englobantes, classes, etc.)
    if len(results[0].boxes) == 0:
        print(f"Object not detected for {filename}")
        continue

    detected = False
    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        label = results[0].names[cls_id]
        if label != target_label:
            continue
        detected = True

        x1, y1, x2, y2 = box.xyxy[0]  # Coordonnées de la boîte

        # Découper l'objet détecté
        cropped_image = image[int(y1):int(y2), int(x1):int(x2)]

        # Calculer le ratio de l'image
        h, w = cropped_image.shape[:2]
        target_size = 256
        scale = target_size / max(h, w)  # Trouver le facteur de mise à l'échelle

        # Redimensionner tout en conservant l'aspect ratio
        new_w = int(w * scale)
        new_h = int(h * scale)
        resized_image = cv2.resize(cropped_image, (new_w, new_h))

        # Créer une image de fond blanche de 256x256
        padded_image = np.full((target_size, target_size, 3), 255, dtype=np.uint8)

        # Calculer les positions pour centrer l'image redimensionnée dans l'image de padding
        x_offset = (target_size - new_w) // 2
        y_offset = (target_size - new_h) // 2

        # Copier l'image redimensionnée dans l'image de fond
        padded_image[y_offset:y_offset + new_h, x_offset:x_offset + new_w] = resized_image

        # Sauvegarder l'image
        save_path = os.path.join(output_folder, f"cropped_{filename}")
        cv2.imwrite(save_path, padded_image)
        print(f"Image sauvegardée sous {save_path}")

        break

    if not detected:
        print(f"Label {target_label} not detected for {filename}")
