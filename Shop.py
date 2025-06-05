import tkinter as tk
from tkinter import Button

from PIL import Image, ImageTk

class ShopFenster:
    def __init__(self, master):
        self.master = master
        self.fenster = tk.Toplevel(master)
        self.fenster.title("Shop")
        self.fenster.geometry("400x300")
        self.fenster.state('zoomed')

#Background
        fenster_width = self.fenster.winfo_screenwidth()
        fenster_height = self.fenster.winfo_screenheight()

        bg = Image.open("assets/Shop_background.png")
        bg = bg.resize((fenster_width, fenster_height))  # resize auf ganze Fenstergröße
        bild_tk = ImageTk.PhotoImage(bg)

        # Label mit Bild
        lbl_bg = tk.Label(self.fenster, image=bild_tk)
        lbl_bg.image = bild_tk  # WICHTIG: Referenz speichern!

        # Label auf gesamte Fläche ausdehnen
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

#header
        frame_lang = Image.open("assets/frame_lang.png")  # Datei: PNG, JPG, etc.
        frame_lang = frame_lang.resize((1000, 100))  # Optional: Größe anpassen
        bild_tk = ImageTk.PhotoImage(frame_lang)  # Konvertieren für Tkinter

        lbl_Item1 = tk.Label(self.fenster, image=bild_tk,bg="black", font=("Press Start 2P", 1), width= 1000, height= 100)
        lbl_Item1.image = bild_tk  # WICHTIG: Referenz speichern!
        lbl_Item1.place(x=270, y=9)  # Position in Pixeln (x= Breite Y= Höhe)

        tk.Label(self.fenster, text="Willkomen im Shop!", font=("Press Start 2P", 40), bg = "#A67C52").pack(pady=20)

#Item 1
        Munze = Image.open("assets/Munze.png")  # Datei: PNG, JPG, etc.
        Munze = Munze.resize((250, 250))  # Optional: Größe anpassen
        bild_tk = ImageTk.PhotoImage(Munze)  # Konvertieren für Tkinter

        lbl_Item1 = tk.Label(self.fenster, image=bild_tk,bg="black", font=("Press Start 2P", 1), width= 250, height= 250)
        lbl_Item1.image = bild_tk  # WICHTIG: Referenz speichern!
        lbl_Item1.place(x=250, y=250)  # Position in Pixeln (x= Breite Y= Höhe)

        Btn_Item1 = tk.Button(self.fenster, text="1k Pissgroschen kaufen", font=("Press Start 2P", 7), relief="solid", bd=3,width=27, height=2, bg="#A67C52")
        Btn_Item1.place(x=250, y=510)

#Item 2
        Munze_haufen = Image.open("assets/Munzen_haufen.png")  # Datei: PNG, JPG, etc.
        Munze_haufen = Munze_haufen.resize((250, 250))  # Optional: Größe anpassen
        bild_tk = ImageTk.PhotoImage(Munze_haufen)  # Konvertieren für Tkinter

        lbl_Item2 = tk.Label(self.fenster, image=bild_tk, bg="black", font=("Press Start 2P", 1), width=250, height=250)
        lbl_Item2.image = bild_tk  # WICHTIG: Referenz speichern!
        lbl_Item2.place(x=510, y=250)  # Position in Pixeln (x= Breite Y= Höhe)

        Btn_Item2 = tk.Button(self.fenster, text="10k Pissgroschen kaufen", font=("Press Start 2P", 7), relief="solid",bd=3, width=27, height=2, bg="#A67C52")
        Btn_Item2.place(x=510, y=510)

# Item 3
        Munze_toilette = Image.open("assets/Munze_toilette.png")  # Datei: PNG, JPG, etc.
        Munze_toilette = Munze_toilette.resize((250, 250))  # Optional: Größe anpassen
        bild_tk = ImageTk.PhotoImage(Munze_toilette)  # Konvertieren für Tkinter

        lbl_Item3 = tk.Label(self.fenster, image=bild_tk, bg="black", font=("Press Start 2P", 1), width=250, height=250)
        lbl_Item3.image = bild_tk  # WICHTIG: Referenz speichern!
        lbl_Item3.place(x=770, y=250)  # Position in Pixeln (x= Breite Y= Höhe)

        Btn_Item3 = tk.Button(self.fenster, text="25k Pissgroschen kaufen", font=("Press Start 2P", 7), relief="solid",bd=3, width=27, height=2, bg="#A67C52")
        Btn_Item3.place(x=770, y=510)

# Item 4
        Munze_boot = Image.open("assets/Munzen_boot.png")  # Datei: PNG, JPG, etc.
        Munze_boot = Munze_boot.resize((250, 250))  # Optional: Größe anpassen
        bild_tk = ImageTk.PhotoImage(Munze_boot)  # Konvertieren für Tkinter

        lbl_Item4 = tk.Label(self.fenster, image=bild_tk, bg="black", font=("Press Start 2P", 1), width=250, height=250)
        lbl_Item4.image = bild_tk  # WICHTIG: Referenz speichern!
        lbl_Item4.place(x=1030, y=250)  # Position in Pixeln (x= Breite Y= Höhe)

        Btn_Item4 = tk.Button(self.fenster, text="50k Pissgroschen kaufen", font=("Press Start 2P", 7), relief="solid",bd=3, width=27, height=2, bg="#A67C52")
        Btn_Item4.place(x=1030, y=510)









        # Button zum Zurückkehren

        Btn_zuruck = tk.Button(self.fenster, text="⬅️Menü", font=("Press Start 2P", 20),bg = "#A67C52", relief="solid",bd=3, width=7, height=1, command=self.zurück)
        Btn_zuruck.place(x=10, y=10)

    def zurück(self):
        self.fenster.destroy()  # Shop-Fenster schließen
        self.master.deiconify()  # Hauptfenster wieder sichtbar machen
        self.master.state('zoomed')


    def kaufe_punkte(self):
        print("Punkte gekauft!")  # später: Punktestand aktualisieren