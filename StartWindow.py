from tkinter import Button

from PIL import Image, ImageTk
import tkinter as tk

def SECRETBUTTON():
    label.config(text="SPIELO WETTER APP \nSTINKT AB")
    # Nach 1000 ms (1 Sekunde) Text zurücksetzen
    fenster.after(1000, lambda: label.config(text=" Bürgermeisters \nSpielplatz"))

fenster = tk.Tk()
fenster.title("Bürgermeisters Spielplatz") # Fenster Name
fenster.geometry("400x300")  # Fenstergröße festlegen
fenster.state('zoomed')

# Bild laden
bild = Image.open("krone.png")   # Datei: PNG, JPG, etc.
bild = bild.resize((90, 90))        # Optional: Größe anpassen
bild_tk = ImageTk.PhotoImage(bild)    # Konvertieren für Tkinter

# Label mit Bild erstellen
ButtonSECRET = tk.Button(fenster, font=("Press Start 2P",1), relief="flat", width= 50, height= 22,command=SECRETBUTTON)
ButtonSECRET.place(x=310, y=12)

label2 = tk.Label(fenster, image=bild_tk)
label2.image = bild_tk  # WICHTIG: Referenz speichern!
label2.place(x=298, y=1)

#Label mit text
label = tk.Label(fenster, text=" Bürgermeisters \nSpielplatz", font=("Press Start 2P", 50))
label.place(x=250, y=80)  # Position in Pixeln (x= Breite Y= Höhe)

#Button


Button1 = tk.Button(fenster, text= "SLOTTI KAROTTI", font=("Press Start 2P",30), relief="solid",bd= 3, width= 30, height= 1, bg="lightgrey")
Button1.place(x=170, y=280)

Button2 = tk.Button(fenster, text= "CAPTAIN BLACK", font=("Press Start 2P",30),relief="solid", width= 30,bd= 3, height= 1, bg="lightgrey")
Button2.place(x=170, y=380)

Button3 = tk.Button(fenster, text= "[coming soon...]", font=("Press Start 2P",30),relief="solid", width= 30,bd= 3, height= 1, bg="lightgrey")
Button3.place(x=170, y=480)

Button4 = tk.Button(fenster, text= "KIPPENAUTOMAT", font=("Press Start 2P",30),relief="solid", width= 30,bd= 3, height= 1, bg="lightgrey")
Button4.place(x=170, y=580)

Button5 = tk.Button(fenster, text= "STORE", font=("Press Start 2P",30), width= 30,relief="solid", height= 1,bd= 3, bg="lightgrey")
Button5.place(x=170, y=680)

fenster.mainloop()