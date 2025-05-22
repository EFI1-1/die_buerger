import tkinter as tk

class ShopFenster:
    def __init__(self, master):
        self.master = master
        self.fenster = tk.Toplevel(master)
        self.fenster.title("Shop")
        self.fenster.geometry("400x300")
        self.fenster.state('zoomed')

        tk.Label(self.fenster, text="🛒 Willkomen im Shop!",bg="blue", font=("Arial", 18)).pack(pady=20)

        lbl_Item1 = tk.Label(self.fenster,bg="blue", font=("Press Start 2P", 1), width= 120, height= 120)
        lbl_Item1.place(x=250, y=100)  # Position in Pixeln (x= Breite Y= Höhe)

        lbl_Item2 = tk.Label(self.fenster,bg="blue", font=("Press Start 2P", 1), width= 120, height= 120)
        lbl_Item2.place(x=500, y=100)  # Position in Pixeln (x= Breite Y= Höhe)

        lbl_Item3 = tk.Label(self.fenster,bg="blue", font=("Press Start 2P", 1), width= 260, height= 120)
        lbl_Item3.place(x=750, y=100)  # Position in Pixeln (x= Breite Y= Höhe)

        lbl_Item4 = tk.Label(self.fenster,bg="blue", font=("Press Start 2P", 1), width= 120, height= 60)
        lbl_Item4.place(x=250, y=500)  # Position in Pixeln (x= Breite Y= Höhe)

        lbl_Item5 = tk.Label(self.fenster,bg="blue", font=("Press Start 2P", 1), width= 120, height= 60)
        lbl_Item5.place(x=500, y=500)  # Position in Pixeln (x= Breite Y= Höhe)

        lbl_Item6 = tk.Label(self.fenster,bg="blue", font=("Press Start 2P", 1), width= 260, height= 60)
        lbl_Item6.place(x=750, y=500)  # Position in Pixeln (x= Breite Y= Höhe)

        # Button zum Zurückkehren
        tk.Button(self.fenster, text="Zurück zum Menü", command=self.zurück).pack(pady=20)

    def zurück(self):
        self.fenster.destroy()  # Shop-Fenster schließen
        self.master.deiconify()  # Hauptfenster wieder sichtbar machen
        self.master.state('zoomed')


    def kaufe_punkte(self):
        print("Punkte gekauft!")  # später: Punktestand aktualisieren