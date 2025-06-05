from SlotMachine import SlotMachineFenster
from Shop import ShopFenster

from tkinter import Button

from PIL import Image, ImageTk
import tkinter as tk

def SECRETBUTTON():
    lbl_Titel.config(text="GRUPPE ALKOHOLIKER  \nSTINKT AB  ")
    # Nach 1000 ms (1 Sekunde) Text zurücksetzen
    root.after(1000, lambda: lbl_Titel.config(text=" Bürgermeisters \nSpielplatz"))

root = tk.Tk()
root.title("Bürgermeisters Spielplatz") # Fenster Name
root.geometry("400x300")  # Fenstergröße festlegen
root.state('zoomed')

# Bild laden
bild = Image.open("assets/krone.png")   # Datei: PNG, JPG, etc.
bild = bild.resize((90, 90))        # Optional: Größe anpassen
bild_tk = ImageTk.PhotoImage(bild)    # Konvertieren für Tkinter

# Label mit Bild erstellen
ButtonSECRET = tk.Button(root, font=("Press Start 2P",1), relief="flat", width= 50, height= 22,command=SECRETBUTTON)
ButtonSECRET.place(x=310, y=12)

lbl_bild = tk.Label(root, image=bild_tk)
lbl_bild.image = bild_tk  # WICHTIG: Referenz speichern!
lbl_bild.place(x=298, y=1)

#Label mit text
lbl_Titel = tk.Label(root, text=" Bürgermeisters \nSpielplatz", font=("Press Start 2P", 50))
lbl_Titel.place(x=250, y=80)  # Position in Pixeln (x= Breite Y= Höhe)

#Button

Btn_Slot = tk.Button(root, text= "SLOTTI KAROTTI", font=("Press Start 2P",30),command=lambda: [SlotMachineFenster(root), root.withdraw()], relief="solid",bd= 3, width= 30, height= 1, bg="lightgrey")
Btn_Slot.place(x=170, y=280)

Button2 = tk.Button(root, text= "[coming soon...]", font=("Press Start 2P",30),relief="solid", width= 30,bd= 3, height= 1, bg="lightgrey")
Button2.place(x=170, y=380)

Button3 = tk.Button(root, text= "[coming soon...]", font=("Press Start 2P",30),relief="solid", width= 30,bd= 3, height= 1, bg="lightgrey")
Button3.place(x=170, y=480)

Button4 = tk.Button(root, text= "KIPPENAUTOMAT", font=("Press Start 2P",30),relief="solid", width= 30,bd= 3, height= 1, bg="lightgrey")
Button4.place(x=170, y=580)

Btn_Shop = tk.Button(root, text= "STORE", font=("Press Start 2P",30), command=lambda: [ShopFenster(root), root.withdraw()], width= 30,relief="solid", height= 1,bd= 3, bg="lightgrey")
Btn_Shop.place(x=170, y=680)

root.mainloop()