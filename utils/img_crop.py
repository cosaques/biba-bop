import numpy as np
from ultralytics import YOLO
import cv2
import os

# Charger le modèle YOLOv8 pré-entraîné
model = YOLO('yolov8n.pt')  # Utilisez un modèle léger comme yolov8n pour commencer.

# Chemin vers l'image d'entrée
image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test.jpg")

# Charger l'image
image = cv2.imread(image_path)

# Détecter des objets dans l'image
results = model(image)

# Extraire les résultats de détection (boîtes englobantes, classes, etc.)
box = results[0].boxes[0]  # Détection de boîtes englobantes dans la première image
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
save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crop.jpg")
cv2.imwrite(save_path, padded_image)
print(f"Image sauvegardée sous {save_path}")
