import tkinter as tk
import random

def SlotMachineFenster(master):
    # Variablen
    symbols = ['🍒', '🍋', '🔔', '🍀', '⭐', '7']
    symbol_multipliers = {'🍒': 2, '🍋': 4, '🔔': 8, '🍀': 12, '⭐': 16, '7': 20}
    points = 1000
    rows, cols = 3, 3
    roll_times = 10
    bet_amount = 0
    spin_counter = 0
    loan_taken = False
    loan_due_at = None
    symbol_canvases = []
    symbol_items = []
    line_item = None

    # Fenster
    fenster = tk.Toplevel(master)
    fenster.state('zoomed')
    fenster.title("Slot Maschine")

    result_var = tk.StringVar()
    score_var = tk.StringVar()
    bet_display_var = tk.StringVar()
    score_var.set(f"Punkte: {points}")
    bet_display_var.set("Einsatz: 0 Punkte")

    def update_score():
        score_var.set(f"Punkte: {points}")
        bet_display_var.set(f"Einsatz: {bet_amount} Punkte")

    def create_slot_grid(parent):
        for r in range(rows):
            row_canvases = []
            row_items = []
            for c in range(cols):
                canvas = tk.Canvas(parent, width=140, height=140, bg="white")
                canvas.grid(row=r, column=c, padx=8, pady=8)
                item = canvas.create_text(70, 70, text='❓', font=('Arial', 72))
                row_canvases.append(canvas)
                row_items.append(item)
            symbol_canvases.append(row_canvases)
            symbol_items.append(row_items)

    def update_symbols(random_board):
        for r in range(rows):
            for c in range(cols):
                symbol_canvases[r][c].itemconfig(symbol_items[r][c], text=random_board[r][c])

    def draw_win_line(coords):
        nonlocal line_item
        x0 = coords[0][1] * 156 + 70
        y0 = coords[0][0] * 156 + 70
        x1 = coords[2][1] * 156 + 70
        y1 = coords[2][0] * 156 + 70
        line_item = line_canvas.create_line(x0, y0, x1, y1, fill='red', width=6)

    def check_win(board):
        for r in range(rows):
            if board[r][0] == board[r][1] == board[r][2]:
                return True, board[r][0], [(r, 0), (r, 1), (r, 2)]
        if board[0][0] == board[1][1] == board[2][2]:
            return True, board[0][0], [(0, 0), (1, 1), (2, 2)]
        if board[0][2] == board[1][1] == board[2][0]:
            return True, board[0][2], [(0, 2), (1, 1), (2, 0)]
        return False, '', []

    def finalize_spin(final_board):
        nonlocal points, bet_amount, spin_counter
        update_symbols(final_board)
        won, win_symbol, coords = check_win(final_board)
        if won:
            multiplier = symbol_multipliers.get(win_symbol, 0)
            win_amount = bet_amount * multiplier
            draw_win_line(coords)
            result_var.set(f"🎉 Gewinn! {win_symbol} x{multiplier} → +{win_amount} Punkte")
            ask_risk(win_amount)
        else:
            points -= bet_amount
            result_var.set(f"Kein Gewinn 🚬 -{bet_amount} Punkte")

        spin_counter += 1
        check_loan_repayment()
        update_score()

    def spin_with_animation():
        nonlocal line_item
        result_var.set("")
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
                fenster.after(100, animate, count + 1)
            else:
                finalize_spin(temp_board)
                spin_button.config(state='normal')

        animate(0)

    def ask_risk(win_amount):
        steps = [win_amount * (2 ** i) for i in range(6)]
        current_step = 0
        current_amount = steps[current_step]

        risk_win = tk.Toplevel(fenster)
        risk_win.title("Risiko-Spiel: Leiter")

        tk.Label(risk_win, text="Risikoleiter – Versuch dein Glück!", font=("Arial", 28)).pack(pady=20)
        amount_label = tk.Label(risk_win, text=f"{current_amount} Punkte", font=("Arial", 32))
        amount_label.pack(pady=20)

        ladder_frame = tk.Frame(risk_win)
        ladder_frame.pack(pady=20)
        step_labels = []
        for i, val in enumerate(reversed(steps)):
            lbl = tk.Label(ladder_frame, text=f"{val} Punkte", width=25, font=("Arial", 20), bg="gray")
            lbl.pack()
            step_labels.insert(0, lbl)

        def update_lights():
            for i, lbl in enumerate(step_labels):
                lbl.config(bg="yellow" if i == current_step else "lightgray")
            amount_label.config(text=f"{current_amount} Punkte")

        def blink_current():
            if current_step < len(step_labels):
                lbl = step_labels[current_step]
                current_color = lbl.cget("bg")
                lbl.config(bg="yellow" if current_color == "lightgray" else "lightgray")
                risk_win.after(500, blink_current)

        def risk_try():
            nonlocal current_step, current_amount, points
            if current_step >= len(steps) - 1:
                return
            if random.choice([True, False]):
                current_step += 1
                current_amount *= 2
                update_lights()
            else:
                points -= bet_amount
                update_score()
                result_var.set(f"❌ Verloren -{bet_amount} Punkte.")
                risk_win.destroy()

        def take_win():
            nonlocal points
            points -= bet_amount
            points += current_amount
            update_score()
            result_var.set(f"✅ {current_amount} Punkte.")
            risk_win.destroy()

        update_lights()
        blink_current()

        button_frame = tk.Frame(risk_win)
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Risiko", font=("Arial", 18), command=risk_try).pack(side='left', padx=40)
        tk.Button(button_frame, text="Nehmen", font=("Arial", 18), command=take_win).pack(side='right', padx=40)

    def prompt_loan():
        def take_loan():
            nonlocal points, loan_taken, loan_due_at, spin_counter
            points += 1000
            loan_taken = True
            loan_due_at = spin_counter + 20
            update_score()
            loan_window.destroy()

        def exit_game():
            fenster.destroy()

        loan_window = tk.Toplevel(fenster)
        loan_window.title("Bankkredit")
        tk.Label(loan_window, text="Du hast keine Punkte mehr.\nMöchtest du ein Kredit von 1k aufnehmen?", font=("Arial", 20)).pack(pady=20)
        tk.Button(loan_window, text="Ja", font=("Arial", 16), command=take_loan).pack(side='left', padx=20, pady=20)
        tk.Button(loan_window, text="Exit", font=("Arial", 16), command=exit_game).pack(side='right', padx=20, pady=20)

    def check_loan_repayment():
        nonlocal points, loan_due_at, loan_taken
        if loan_taken and spin_counter >= loan_due_at:
            if points >= 1000:
                points -= 1000
                result_var.set("💰 Kredit zurückgezahlt.")
                loan_taken = False
            else:
                result_var.set("❌ Kredit nicht zurückgezahlt.")
                fenster.after(3000, fenster.destroy)
            update_score()

    def set_bet(bet, window):
        nonlocal bet_amount
        bet_amount = bet
        update_score()
        window.destroy()

    def open_bet_window():
        window = tk.Toplevel(fenster)
        window.title("Einsatz wählen")
        for i, bet in enumerate(range(10, 201, 10)):
            btn = tk.Button(window, text=f"{bet}", font=("Arial", 16), command=lambda b=bet, w=window: set_bet(b, w))
            btn.grid(row=i // 7, column=i % 7, padx=10, pady=10)

    # GUI Aufbau
    tk.Label(fenster, textvariable=score_var, font=('Arial', 28)).pack(pady=10)
    frame = tk.Frame(fenster, width=cols * 156, height=rows * 156)
    frame.pack()
    line_canvas = tk.Canvas(frame, width=cols * 156, height=rows * 156, highlightthickness=0)
    line_canvas.place(x=0, y=0)
    create_slot_grid(frame)

    tk.Button(fenster, text="Einsatz", font=('Arial', 24), command=open_bet_window).pack(pady=5)
    tk.Label(fenster, textvariable=bet_display_var, font=('Arial', 24)).pack(pady=5)
    spin_button = tk.Button(fenster, text="SPIN", font=('Arial', 32), command=spin_with_animation)
    spin_button.pack(pady=20)
    tk.Label(fenster, textvariable=result_var, font=('Arial', 24)).pack(pady=10)

    update_score()