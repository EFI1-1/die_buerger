import tkinter as tk
import random

# Symbole und Multiplikatoren
symbols = ['🍒', '🍋', '🔔', '🍀', '⭐', '7']
symbol_multipliers = {
    '🍒': 2,
    '🍋': 4,
    '🔔': 8,
    '🍀': 12,
    '⭐': 16,
    '7': 20
}

points = 1000
rows, cols = 1, 3
roll_times = 10
bet_amount = 0
spin_counter = 0
loan_taken = False
loan_due_at = None

# Tkinter Hauptfenster
root = tk.Tk()
root.title("3x3 Slot Maschine")

score_var = tk.StringVar(value=f"Punkte: {points}")
slot_vars = [[tk.StringVar(value='❓') for _ in range(cols)] for _ in range(rows)]
result_var = tk.StringVar(value="")
bet_display_var = tk.StringVar(value="Einsatz: 0 Punkte")

# Spin Funktion mit Animation
def spin_with_animation():
    global points, bet_amount, spin_counter

    if bet_amount == 0:
        result_var.set("Bitte Einsatz wählen!")
        return
    if points < bet_amount:
        prompt_loan()
        return

    def animate(count):
        for r in range(rows):
            for c in range(cols):
                slot_vars[r][c].set(random.choice(symbols))
        if count < roll_times:
            root.after(100, animate, count + 1)
        else:
            finalize_spin()
    animate(0)

# Kreditsystem
def prompt_loan():
    def take_loan():
        global points, loan_taken, loan_due_at, spin_counter
        points += 1000
        loan_taken = True
        loan_due_at = spin_counter + 20
        update_score()
        loan_window.destroy()

    def exit_game():
        root.destroy()

    loan_window = tk.Toplevel(root)
    loan_window.title("Bankkredit")
    tk.Label(loan_window, text="Du hast zu wenig Punkte.\n1000 Punkte Kredit aufnehmen?", font=("Pixel", 12)).pack(pady=10)
    tk.Button(loan_window, text="Ja, Kredit", command=take_loan).pack(side='left', padx=10, pady=10)
    tk.Button(loan_window, text="Nein, Spiel beenden", command=exit_game).pack(side='right', padx=10, pady=10)

# Spin Ergebnis
def finalize_spin():
    global points, bet_amount, spin_counter

    final_symbols = [[random.choice(symbols) for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            slot_vars[r][c].set(final_symbols[r][c])

    won = False
    win_symbol = ''
    for row in final_symbols:
        if row[0] == row[1] == row[2]:
            win_symbol = row[0]
            won = True
            break

    if won:
        multiplier = symbol_multipliers.get(win_symbol, 0)
        win_amount = bet_amount * multiplier
        points += win_amount
        result_var.set(f"🎉 Gewinn! Symbol: {win_symbol} x{multiplier} → +{win_amount} Punkte")
        ask_risk(win_amount)
    else:
        points -= bet_amount
        result_var.set(f"Kein Gewinn 😢 -{bet_amount} Punkte")

    spin_counter += 1
    check_loan_repayment()
    update_score()

# Punktezähler aktualisieren
def update_score():
    score_var.set(f"Punkte: {points}")
    bet_display_var.set(f"Einsatz: {bet_amount} Punkte")

# Überprüfung für Kreditrückzahlung
def check_loan_repayment():
    global points, loan_due_at, loan_taken
    if loan_taken and spin_counter >= loan_due_at:
        if points >= 1000:
            points -= 1000
            result_var.set("💰 Kredit zurückgezahlt.")
            loan_taken = False
            update_score()
        else:
            result_var.set("❌ Kredit nicht zurückgezahlt. Spiel beendet.")
            root.after(3000, root.destroy)

# Einsatz setzen
def set_bet(bet, window):
    global bet_amount
    bet_amount = bet
    update_score()
    window.destroy()

# Einsatzfenster
def open_bet_window():
    window = tk.Toplevel(root)
    window.title("Einsatz wählen")
    buttons_per_row = 7

    for i, bet in enumerate(range(10, 201, 10)):
        row = i // buttons_per_row
        col = i % buttons_per_row
        btn = tk.Button(window, text=f"{bet}", font=("Pixel", 12),
                        command=lambda b=bet, w=window: set_bet(b, w))
        btn.grid(row=row, column=col, padx=5, pady=5)

# (Platzhalter) Risiko-Spiel
def ask_risk(win_amount):
    # Hier kommt später das Risiko-Spiel rein (Rot/Schwarz oder Leiter)
    pass

# GUI Aufbau
tk.Label(root, textvariable=score_var, font=('Pixel', 16)).grid(row=0, column=0, columnspan=cols)

for r in range(rows):
    for c in range(cols):
        tk.Label(root, textvariable=slot_vars[r][c], font=('Pixel', 36), width=4).grid(row=r+1, column=c, padx=5, pady=5)

tk.Button(root, text="Einsatz setzen", font=('Pixel', 14), command=open_bet_window).grid(row=rows+1, column=0, columnspan=cols)
tk.Label(root, textvariable=bet_display_var, font=('Pixel', 14)).grid(row=rows+2, column=0, columnspan=cols)
tk.Button(root, text="SPIN", font=('Pixel', 16), command=spin_with_animation).grid(row=rows+3, column=0, columnspan=cols, pady=10)
tk.Label(root, textvariable=result_var, font=('Pixel', 14)).grid(row=rows+4, column=0, columnspan=cols)

root.mainloop()
