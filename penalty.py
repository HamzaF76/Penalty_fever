import ctypes
import cv2
import numpy as np
import pyautogui
import time
import os

# Fonction pour simuler un clic précis en utilisant ctypes
def clic_souris(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)
    ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # Clic gauche enfoncé
    ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # Clic gauche relâché

# Fonction pour détecter le cercle rouge dans une région spécifique de l'écran et cliquer dessus
def detecter_cercle_rouge():
    x_gauche, y_haut = 247, 562
    x_droit, y_bas = 587, 754
    largeur = x_droit - x_gauche
    hauteur = y_bas - y_haut

    # Dossier de sauvegarde des captures d'écran
    dossier_sauvegarde = r'C:\Users\hamza\script_jeu'

    # Créer le dossier s'il n'existe pas déjà
    if not os.path.exists(dossier_sauvegarde):
        os.makedirs(dossier_sauvegarde)

    # Nombre d'itérations pour capturer plusieurs écrans
    nombre_iterations = 50
    intervalle_capture = 0.05  # Intervalle entre chaque capture en secondes

    for i in range(nombre_iterations):
        capture = pyautogui.screenshot(region=(x_gauche, y_haut, largeur, hauteur))
        
        # Enregistrer chaque capture d'écran dans le dossier de sauvegarde avec un nom unique
        nom_fichier = os.path.join(dossier_sauvegarde, f'capture_{i+1}.png')
        capture.save(nom_fichier)

        img_np = np.array(capture)
        img_rgb = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

        rouge_bas = np.array([0, 0, 150])
        rouge_haut = np.array([100, 100, 255])
        masque = cv2.inRange(img_rgb, rouge_bas, rouge_haut)

        contours, _ = cv2.findContours(masque, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            contour = max(contours, key=cv2.contourArea)
            ((x, y), rayon) = cv2.minEnclosingCircle(contour)
            x, y = int(x), int(y)
            
            # Afficher les coordonnées avant de cliquer
            print(f"Coordonnées du clic : x={x_gauche + x}, y={y_haut + y}")

            # Clic au centre du cercle détecté en utilisant ctypes
            clic_souris(x_gauche + x, y_haut + y)
            return True

        time.sleep(intervalle_capture)  # Attendre avant de prendre la prochaine capture

    return False

# Exemple d'utilisation
detecter_cercle_rouge()
