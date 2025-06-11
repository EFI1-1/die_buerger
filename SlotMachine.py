import tkinter as tk
import random
from PIL import Image, ImageTk

def SlotMachineFenster(master):
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

    font_game = ("Press Start 2P", 18)

    fenster = tk.Toplevel(master)
    fenster.state('zoomed')
    fenster.title("Slot Maschine")


    try:
        bg = Image.open("assets/slotmachinebackground.png")
        screen_width = fenster.winfo_screenwidth()
        screen_height = fenster.winfo_screenheight()
        bg = bg.resize((screen_width, screen_height), Image.LANCZOS)
        bild_tk = ImageTk.PhotoImage(bg)

        lbl_bg = tk.Label(fenster, image=bild_tk)
        lbl_bg.image = bild_tk
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Fehler beim Laden des Hintergrunds:", e)

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
                canvas = tk.Canvas(parent, width=120, height=120, bg="white")
                canvas.grid(row=r, column=c, padx=10, pady=10)
                item = canvas.create_text(60, 60, text='❓', font=("Arial", 60))
                row_canvases.append(canvas)
                row_items.append(item)
            symbol_canvases.append(row_canvases)
            symbol_items.append(row_items)

    def update_symbols(random_board):
        for r in range(rows):
            for c in range(cols):
                symbol = random_board[r][c]
                font = ("Arial", 60) if symbol == '7' else ("Segoe UI Emoji", 60)
                symbol_canvases[r][c].itemconfig(symbol_items[r][c], text=symbol, font=font)

    def draw_win_line(coords):
        nonlocal line_item
        x0 = coords[0][1] * 190 + 90
        y0 = coords[0][0] * 190 + 90
        x1 = coords[2][1] * 190 + 90
        y1 = coords[2][0] * 190 + 90
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
            result_var.set(f"{win_symbol} x{multiplier} → +{win_amount} Punkte")
            ask_risk(win_amount)
        else:
            points -= bet_amount
            result_var.set(f"-{bet_amount} Punkte")

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
            result_var.set("Einsatz wählen!")
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
        global blink_state, win_step, lose_step
        blink_state = 0
        win_step = None
        lose_step = None

        steps = [win_amount * (2 ** i) for i in range(6)]  # 40, 80, 160, ...
        steps.append(0)  # 0 Punkte unten

        display_steps = steps[:-1][::-1] + [0]  # für Anzeige: größter Gewinn oben, 0 unten

        # Map: Display-Index zu echtem Steps-Index
        display_to_step = list(range(len(steps) - 2, -1, -1)) + [len(steps) - 1]
        # z.B. [5,4,3,2,1,0,6] für 6 Stufen + 0

        current_display_step = len(display_steps) - 2  # Start auf 40 (zweitunterste Stufe!)

        current_step = display_to_step[current_display_step]
        current_amount = steps[current_step]

        risk_win = tk.Toplevel(fenster)
        risk_win.title("Risiko-Spiel: Leiter")

        tk.Label(risk_win, text="Risikoleiter – Versuch dein Glück!", font=("Arial", 28)).pack(pady=20)
        amount_label = tk.Label(risk_win, text=f"{current_amount} Punkte", font=("Arial", 32))
        amount_label.pack(pady=20)

        ladder_frame = tk.Frame(risk_win)
        ladder_frame.pack(pady=20)
        step_labels = []

        for val in display_steps:
            lbl = tk.Label(ladder_frame, text=f"{val} Punkte", width=25, font=("Arial", 20), bg="gray")
            lbl.pack()
            step_labels.append(lbl)

        def update_lights():
            global blink_state, win_step, lose_step
            for i, lbl in enumerate(step_labels):
                lbl.config(bg="lightgray")  # Reset all

            # Aktuelle Stufe GELB
            step_labels[current_display_step].config(bg="yellow")

            win_step = None
            lose_step = None

            if current_display_step > 0:
                win_step = current_display_step - 1

            if current_display_step <= len(display_steps) - 3:
                lose_step = current_display_step + 2
            else:
                lose_step = len(display_steps) - 1

            amount_label.config(text=f"{steps[display_to_step[current_display_step]]} Punkte")

        def blink_current():
            global blink_state, win_step, lose_step
            if current_display_step < len(step_labels):
                # Erst ALLES außer aktuelle Stufe zurücksetzen
                for i, lbl in enumerate(step_labels):
                    if i != current_display_step:
                        lbl.config(bg="lightgray")

                # Dann Gewinn oder Verlust blinken lassen
                if blink_state == 0 and win_step is not None:
                    step_labels[win_step].config(bg="yellow")
                elif blink_state == 1 and lose_step is not None:
                    step_labels[lose_step].config(bg="yellow")

                # Wechsel den Blink-Zustand
                blink_state = 1 - blink_state

                risk_win.after(500, blink_current)

        def risk_try():
            nonlocal current_display_step, current_step, current_amount, points
            if current_display_step == 0:  # Oben -> kein höherer Gewinn
                return

            if random.choice([True, False]):
                current_display_step -= 1  # eine Stufe nach oben
            else:
                if current_display_step <= len(display_steps) - 3:
                    current_display_step += 2  # zwei Stufen zurück
                else:
                    current_display_step = len(display_steps) - 1  # auf 0 Punkte

            current_step = display_to_step[current_display_step]
            current_amount = steps[current_step]
            update_lights()

            if current_step == len(steps) - 1:  # 0 Punkte erreicht
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
            spin_button.config(state='normal')
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
        spin_button.config(state='disabled')
        tk.Label(loan_window, text="Du hast keine Punkte mehr.\nMöchtest du ein Kredit von 1k aufnehmen?", font=font_game).pack(pady=20)
        tk.Button(loan_window, text="Ja", font=font_game, command=take_loan).pack(side='left', padx=20, pady=20)
        tk.Button(loan_window, text="Exit", font=font_game, command=exit_game).pack(side='right', padx=20, pady=20)

    def check_loan_repayment():
        nonlocal points, loan_due_at, loan_taken
        if loan_taken and spin_counter >= loan_due_at:
            if points >= 1000:
                points -= 1000
                result_var.set("Kredit zurückgezahlt.")
                loan_taken = False
            else:
                result_var.set("Kredit nicht zurückgezahlt.")
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
            btn = tk.Button(window, text=f"{bet}", font=font_game, command=lambda b=bet, w=window: set_bet(b, w))
            btn.grid(row=i // 7, column=i % 7, padx=10, pady=10)

    def zuruck_zum_menu():
        master.deiconify()
        master.state('zoomed')
        fenster.after(25, fenster.destroy)

    zuruck_button = tk.Button(fenster, text="⬅️Menü", font=font_game, command=zuruck_zum_menu)
    zuruck_button.pack(side='top', anchor='nw', padx=10, pady=10)
    # GUI Aufbau
    tk.Label(fenster, textvariable=score_var, font=font_game).pack(pady=10)
    frame = tk.Frame(fenster, width=cols * 190, height=rows * 190)
    frame.pack()
    line_canvas = tk.Canvas(frame, width=cols * 190, height=rows * 190, highlightthickness=0)
    line_canvas.place(x=0, y=0)
    create_slot_grid(frame)

    tk.Button(fenster, text="Einsatz", font=font_game, command=open_bet_window).pack(pady=5)
    tk.Label(fenster, textvariable=bet_display_var, font=font_game).pack(pady=5)
    spin_button = tk.Button(fenster, text="SPIN", font=font_game, command=spin_with_animation)
    spin_button.pack(pady=20)
    tk.Label(fenster, textvariable=result_var, font=font_game).pack(pady=10)

    update_score()