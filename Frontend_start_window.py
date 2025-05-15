from PIL import Image, ImageTk
import tkinter as tk


fenster = tk.Tk()
fenster.title("Bürgermeisters Spielplatz") # Fenster Name
fenster.geometry("400x300")  # Fenstergröße festlegen
fenster.state('zoomed')

# Bild laden
bild = Image.open("krone.png")   # Datei: PNG, JPG, etc.
bild = bild.resize((90, 90))        # Optional: Größe anpassen
bild_tk = ImageTk.PhotoImage(bild)    # Konvertieren für Tkinter

# Label mit Bild erstellen
label2 = tk.Label(fenster, image=bild_tk)
label2.image = bild_tk  # WICHTIG: Referenz speichern!
label2.place(x=470, y=20)

#Label mit text
label = tk.Label(fenster, text=" Bürgermeisters \nSpielplatz", font=("Press Start 2P", 50))
label.place(x=250, y=80)  # Position in Pixeln (x= Breite Y= Höhe)

fenster.mainloop()