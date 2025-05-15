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

# Globale Spielvariablen
points = 1000
rows, cols = 3, 5
roll_times = 10
bet_amount = 0
spin_counter = 0
loan_taken = False
loan_due_at = None
symbol_canvases = []
symbol_items = []
line_item = None
line_canvas = None
spin_button = None

# Tkinter Hauptfenster
root = tk.Tk()
root.title("Slot Maschine")

# StringVars
result_var = tk.StringVar()
score_var = tk.StringVar()
bet_display_var = tk.StringVar()
score_var.set(f"Punkte: {points}")
bet_display_var.set("Einsatz: 0 Punkte")

# Slotfeld erstellen
def create_slot_grid(parent):
    global symbol_canvases, symbol_items
    for r in range(rows):
        row_canvases = []
        row_items = []
        for c in range(cols):
            canvas = tk.Canvas(parent, width=70, height=70, bg="white")
            canvas.grid(row=r, column=c, padx=4, pady=4)
            item = canvas.create_text(35, 35, text='❓', font=('Arial', 36))
            row_canvases.append(canvas)
            row_items.append(item)
        symbol_canvases.append(row_canvases)
        symbol_items.append(row_items)

# Symbole aktualisieren
def update_symbols(random_board):
    for r in range(rows):
        for c in range(cols):
            symbol_canvases[r][c].itemconfig(symbol_items[r][c], text=random_board[r][c])

# Spin mit Animation
def spin_with_animation():
    global line_item
    if line_item:
        line_canvas.delete(line_item)
        line_item = None

    if bet_amount == 0:
        result_var.set("Wähle dein Einsatz!")
        return
    if points < bet_amount:
        prompt_loan()
        return

    spin_button.config(state='disabled')

    def animate(count):
        temp_board = [[random.choice(symbols) for _ in range(cols)] for _ in range(rows)]
        update_symbols(temp_board)
        if count < roll_times:
            root.after(100, animate, count + 1)
        else:
            finalize_spin(temp_board)
            spin_button.config(state='normal')

    animate(0)

# Gewinnlinien prüfen
def check_win(board):
    for r in range(rows):
        if board[r][0] == board[r][1] == board[r][2]:
            return True, board[r][0], [(r, 0), (r, 1), (r, 2)]
    if board[0][0] == board[1][1] == board[2][2]:
        return True, board[0][0], [(0, 0), (1, 1), (2, 2)]
    if board[0][2] == board[1][1] == board[2][0]:
        return True, board[0][2], [(0, 2), (1, 1), (2, 0)]
    return False, '', []

# Gewinnlinie zeichnen
def draw_win_line(coords):
    global line_item
    x0 = coords[0][1] * 78 + 35
    y0 = coords[0][0] * 78 + 35
    x1 = coords[2][1] * 78 + 35
    y1 = coords[2][0] * 78 + 35
    line_item = line_canvas.create_line(x0, y0, x1, y1, fill='red', width=4)

# Risiko-Spiel: Leiter
def ask_risk(win_amount):
    def risk_try():
        nonlocal current_amount
        global points
        if random.choice([True, False]):
            current_amount *= 2
            amount_label.config(text=f"{current_amount} Punkte")
        else:
            points -= bet_amount
            update_score()
            result_var.set("❌ Verloren – -100 Punkte.")
            risk_win.destroy()

    def take_win():
        global points
        points -= bet_amount
        points += current_amount
        update_score()
        result_var.set(f"✅ {current_amount} Punkte gesichert.")
        risk_win.destroy()

    current_amount = win_amount
    risk_win = tk.Toplevel(root)
    risk_win.title("Risiko-Spiel: Leiter")

    tk.Label(risk_win, text="Risikoleiter – Versuch dein Glück!", font=("Arial", 14)).pack(pady=10)
    amount_label = tk.Label(risk_win, text=f"{current_amount} Punkte", font=("Arial", 18))
    amount_label.pack(pady=10)

    tk.Button(risk_win, text="Risiko", font=("Arial", 12), command=risk_try).pack(side='left', padx=20, pady=10)
    tk.Button(risk_win, text="Nehmen", font=("Arial", 12), command=take_win).pack(side='right', padx=20, pady=10)

# Spin-Auswertung
def finalize_spin(final_board):
    global points, bet_amount, spin_counter
    update_symbols(final_board)
    won, win_symbol, coords = check_win(final_board)
    if won:
        multiplier = symbol_multipliers.get(win_symbol, 0)
        win_amount = bet_amount * multiplier
        draw_win_line(coords)
        result_var.set(f"🎉 Gewinn! Symbol: {win_symbol} x{multiplier} → +{win_amount} Punkte")
        ask_risk(win_amount)
    else:
        points -= bet_amount
        result_var.set(f"Kein Gewinn 🚬 -{bet_amount} Punkte")

    spin_counter += 1
    check_loan_repayment()
    update_score()

# Punktezähler aktualisieren
def update_score():
    score_var.set(f"Punkte: {points}")
    bet_display_var.set(f"Einsatz: {bet_amount} Punkte")

# Kreditabfrage
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
    tk.Label(loan_window, text="Du hast keine Punkte mehr.\n1Möchtest du ein Kredit von 1k aufnehmen?", font=("Pixel", 12)).pack(pady=10)
    tk.Button(loan_window, text="Ja, Kredit", command=take_loan).pack(side='left', padx=10, pady=10)
    tk.Button(loan_window, text="Nein, Spiel beenden", command=exit_game).pack(side='right', padx=10, pady=10)

# Kreditrückzahlung
def check_loan_repayment():
    global points, loan_due_at, loan_taken
    if loan_taken and spin_counter >= loan_due_at:
        if points >= 1000:
            points -= 1000
            result_var.set("💰 Kredit zurückgezahlt.")
            loan_taken = False
        else:
            result_var.set("❌ Kredit nicht zurückgezahlt. Spiel beendet.")
            root.after(3000, root.destroy)
        update_score()

# Einsatz setzen
def set_bet(bet, window):
    global bet_amount
    bet_amount = bet
    update_score()
    window.destroy()

def open_bet_window():
    window = tk.Toplevel(root)
    window.title("Einsatz wählen")
    for i, bet in enumerate(range(10, 201, 10)):
        btn = tk.Button(window, text=f"{bet}", font=("Pixel", 12),
                        command=lambda b=bet, w=window: set_bet(b, w))
        btn.grid(row=i // 5, column=i % 5, padx=5, pady=5)

# GUI Aufbau
tk.Label(root, textvariable=score_var, font=('Pixel', 16)).pack()
frame = tk.Frame(root, width=cols*78, height=rows*78)
frame.pack()

# 1. Gewinnlinien-Canvas zuerst einfügen
line_canvas = tk.Canvas(frame, width=cols*78, height=rows*78, highlightthickness=0)
line_canvas.place(x=0, y=0)

# 2. Danach Slot-Symbole erstellen (liegen darüber)
create_slot_grid(frame)

tk.Button(root, text="Einsatz", font=('Pixel', 14), command=open_bet_window).pack()
tk.Label(root, textvariable=bet_display_var, font=('Pixel', 14)).pack()
spin_button = tk.Button(root, text="SPIN", font=('Pixel', 16), command=spin_with_animation)
spin_button.pack(pady=10)
tk.Label(root, textvariable=result_var, font=('Pixel', 14)).pack()

update_score()
root.mainloop()
