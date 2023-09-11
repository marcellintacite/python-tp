import os
from tkinter import messagebox

# def convert_gpgga_to_gpgsa(gpgga_sentence):
#     # Diviser la trame GPGGA en éléments séparés par des virgules
#     gpgga_parts = gpgga_sentence.split(',')

#     # Vérifier que la trame GPGGA est valide
#     if len(gpgga_parts) < 15 or gpgga_parts[0] != '$GPGGA':
#         return None  # Trame invalide

#     # Créer la trame GPGSA en utilisant certaines informations de GPGGA
#     gpgsa_sentence = f"$GPGSA,A,3,{','.join(gpgga_parts[7:14])},1.0,1.0,1.0*"

#     # Calculer la somme de contrôle (checksum)
#     checksum = 0
#     for char in gpgsa_sentence:
#         checksum ^= ord(char)

#     # Ajouter le checksum à la trame GPGSA
#     gpgsa_sentence += f"{checksum:02X}\r\n"

#     return gpgsa_sentence


# # Exemple d'utilisation
# gpgga_sentence = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*42"
# gpgsa_sentence = convert_gpgga_to_gpgsa(gpgga_sentence)
# if gpgsa_sentence:
#     print(gpgsa_sentence)


from datetime import datetime
import tkinter as tk


def convert_gpgga_to_gprmc(gpgga_sentence):
    # Diviser la trame GPGGA en éléments séparés par des virgules
    gpgga_parts = gpgga_sentence.split(',')

    # Vérifier que la trame GPGGA est valide
    if len(gpgga_parts) < 15 or gpgga_parts[0] != '$GPGGA':
        return None  # Trame invalide

    # Extraire certaines informations de GPGGA pour GPRMC
    time = gpgga_parts[1]
    lat = gpgga_parts[2] + gpgga_parts[3]
    lon = gpgga_parts[4] + gpgga_parts[5]
    speed = "0.0"  # Valeur par défaut pour la vitesse (peut être ajustée)
    course = "0.0"  # Valeur par défaut pour le cap (peut être ajustée)

    # Créer la trame GPRMC en utilisant les informations extraites
    gprmc_sentence = f"$GPRMC,{time},A,{lat},{lon},{speed},{course},{gpgga_parts[9]},{gpgga_parts[7]},{gpgga_parts[6]},,{gpgga_parts[13]},*"

    # Calculer la somme de contrôle (checksum)
    checksum = 0
    for char in gprmc_sentence:
        checksum ^= ord(char)

    # Ajouter le checksum à la trame GPRMC
    gprmc_sentence += f"{checksum:02X}\r\n"

    return gprmc_sentence


# # Exemple d'utilisation
# gpgga_sentence = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*42"
# gprmc_sentence = convert_gpgga_to_gprmc(gpgga_sentence)
# if gprmc_sentence:
#     print(gprmc_sentence)


def gpgga_to_gsa(gpgga_sentence):
    # Split the GPGGA sentence into its fields
    fields = gpgga_sentence.split(',')

    # Check if the sentence is valid and has enough fields
    if len(fields) < 15 or fields[0] != "$GPGGA":
        return None

    # Extract relevant data from the GPGGA sentence
    time = fields[1]
    latitude = fields[2]
    longitude = fields[4]
    altitude = fields[9]

    # Construct the GSA sentence
    gsa_sentence = f"$GPGSA,A,3,01,02,03,04,05,06,07,08,09,10,11,12,2.5,1.2,1.8,{altitude},,,,,,1.5,1.2,2.2*"

    # Calculate the checksum for the GSA sentence
    checksum = 0
    for char in gsa_sentence:
        checksum ^= ord(char)

    # Append the checksum to the GSA sentence
    gsa_sentence += f"{checksum:02X}"

    return gsa_sentence


# Crée la fenêtre principale.
root = tk.Tk()

root.title("Convertisseur GPGGA vers GPGSA et GPRMC")

root.geometry("950x400")
# mis en forme
root.configure(bg="#352F44")
# Disable resizing the GUI
root.resizable(False, False)


def convert():
    gga_sentence = gga_entry.get()
    gsa_sentence = gpgga_to_gsa(gga_sentence)
    if gsa_sentence:
        gsa_text.delete(1.0, tk.END)
        gsa_text.insert(tk.END, gsa_sentence)
        gsa_text.configure(state='disabled')
        # disable
    gprmc_sentence = convert_gpgga_to_gprmc(gga_sentence)
    if gprmc_sentence:
        gprmc_text.delete(1.0, tk.END)
        gprmc_text.insert(tk.END, gprmc_sentence)
        gprmc_text.configure(state='disabled')
        # disable


#Conversion GPGA en GPGSA

def toGPGSA (trame):
    g="$GPGSA,A,3"
    t=trame.split(",")
    for i in range(1,int(t[7])+1):
        if(i<=9):
            g+=",0"+str(i)
        else :
            g+=","+str(i)
    for i in range(0,3):
        g+=","+str(t[8])
    return g

GPGSA=toGPGSA(trame1)


def CkeckSum(PAR):
    chaine=PAR
    m1=PAR.replace(',',"")
    m2=m1.replace("$","")
    xor_result=0
    for char in m2:
        xor_result^=ord(char)
    chaine+=",*"+str(xor_result+2)
    return chaine


def export_frames():
    # Vérifie si le fichier existe.
    if os.path.exists("frames.txt"):
        # Supprime le fichier.
        os.remove("frames.txt")
    # Récupère la trame GPGGA saisie par l'utilisateur.
    gpgga_sentence = gga_entry.get()

    # Convertit la trame GPGGA en GPGSA.
    gsa_sentence = gpgga_to_gsa(gpgga_sentence)

    # Convertit la trame GPGGA en GPRMC.
    gprmc_sentence = convert_gpgga_to_gprmc(gpgga_sentence)

    # Crée un fichier texte pour enregistrer les trames converties.
    file = open("frames.txt", "w")

    # Écrit les trames converties dans le fichier texte.
    file.write(gsa_sentence)
    file.write(gprmc_sentence)
    file.write(gpgga_sentence)
    # showing a dialog box
    messagebox.showinfo(
        "Confirmation", "Félicitation, fichier enreigistré avec succès!")
    # Clear the entry box
    gga_entry.delete(0, tk.END)

    # Ferme le fichier texte.
    file.close()


title = tk.Label(
    root, text="Convertisseur GPGGA vers GPGSA et GPRMC", bg="#352F44", fg="#FFFFFF", font=("Helvetica", 20), pady=5, padx=5, width=50, height=2)
title.grid(row=0, column=0, padx=5, pady=5)


frame = tk.Frame(root)
frame.grid(row=1, column=0, padx=10, pady=10)
frame.configure(bg="#352F44")
# Creation du label
label = tk.Label(
    frame, text="Entrez la trame GPGGA à convertir : ", bg="#352F44", fg="#FFFFFF", font=("Helvetica", 12))
label.grid(row=0, column=0, padx=5, pady=5)


# Crée la zone de saisie de la trame GPGGA.
gga_entry = tk.Entry(frame, width=50, font=("Helvetica", 14))
gga_entry.grid(row=0, column=1, padx=5, pady=5)


# Frame pour les boutons
frame2 = tk.Frame(root)
frame2.grid(row=2, column=0, padx=5, pady=5)
frame2.configure(bg="#352F44")
# Crée le bouton de conversion.
convert_button = tk.Button(frame2, text="Convertir", command=convert, font=(
    "ralaway", 12), bg="#B9B4C7", fg="#352F44", pady=5, padx=5, width=20, height=2)
convert_button.grid(row=2, column=0, padx=10, pady=10)

# Crée le bouton d'exportation
export_button = tk.Button(frame2, text="Exporter",
                          command=export_frames, font=("Helvetica", 12), bg="#5C5470", fg="#FFFFFF", pady=5, padx=5, width=20, height=2)
export_button.grid(row=2, column=1, padx=10, pady=10)


# Frame pour les trames converties
frame3 = tk.Frame(frame2)
frame3.grid(row=0, column=0, padx=5, pady=5)
frame3.configure(bg="#352F44")
# Crée les labels pour les trames converties.
gsa_label = tk.Label(frame3, text="Trame Convertis :", bg="#352F44",
                     fg="#FFFFFF", font=("Helvetica", 12))
gsa_label.grid(row=0, column=0, padx=5, pady=5)

# Crée les zones de texte pour afficher les trames converties.
gsa_text = tk.Text(frame2, height=2, width=50)
gsa_text.grid(row=1, column=0, padx=5, pady=5)
gprmc_text = tk.Text(frame2, height=2, width=50)
gprmc_text.grid(row=1, column=1, padx=5, pady=5)

# Démarre le programme principal.
root.mainloop()
