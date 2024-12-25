import tkinter as tk
from tkinter import simpledialog, messagebox
from typing import List
from PIL import Image, ImageTk

class PenaltyTimer:
    def __init__(self, parent, delete_callback, player_number):
        self.time_left = 120  # 2 minutes in seconds
        self.frame = tk.Frame(parent, bg="black")
        self.frame.pack(pady=2)
        
        self.label = tk.Label(self.frame, text="2:00", font=("Digital-7", 20), fg="red", bg="black")
        self.label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.player_label = tk.Label(self.frame, text=f"Jogador {player_number}", font=("Arial", 20), fg="white", bg="black")
        self.player_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.delete_button = tk.Button(self.frame, text="❌", command=delete_callback, bg="red", fg="white")
        self.delete_button.pack(side=tk.LEFT)
        
    def update(self):
        if self.time_left > 0:
            self.time_left -= 1
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            self.label.config(text=f"{minutes}:{seconds:02d}")
            return True
        else:
            self.frame.destroy()
            return False

class HandballScoreboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Placar de Handebol")
        self.root.configure(bg='black')
        
        # Set full screen
        self.root.attributes('-fullscreen', True)

        # Variáveis do placar
        self.score_team1 = 0
        self.score_team2 = 0
        self.game_time = 0  # Começa em 0 segundos
        self.timer_running = False
        self.current_period = 1
        self.penalties_team1: List[PenaltyTimer] = []
        self.penalties_team2: List[PenaltyTimer] = []
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='black')
        main_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.logo_image = Image.open("logo.png")
        self.logo_image = self.logo_image.resize((250, 250))
        self.logo = ImageTk.PhotoImage(self.logo_image)
        
        self.logo_label = tk.Label(self.root, image=self.logo, bg='black')
        self.logo_label.place(relx=1.0, rely=0.0, anchor='ne')
        
        # Timer principal e controles
        self.setup_timer_and_controls(main_frame)
        
        # Configuração dos times
        self.setup_team_names(main_frame)
        
        # Placar e áreas de penalidade
        self.setup_scoreboard_and_penalties(main_frame)
        
        # Controles adicionais
        self.setup_additional_controls(main_frame)
        
    def setup_timer_and_controls(self, parent):
        timer_frame = tk.Frame(parent, bg="black")
        timer_frame.pack(pady=20)
        
        # Botão de pausa
        self.start_button = tk.Button(
            timer_frame,
            text="▶",
            command=self.toggle_timer,
            font=("Arial", 30),
            bg="white"
        )
        self.start_button.pack(side=tk.LEFT, padx=20)
        
        # Timer principal
        self.timer_label = tk.Label(
            timer_frame, 
            text="00:00",
            font=("Digital-7", 80),
            fg="red",
            bg="black"
        )
        self.timer_label.pack(side=tk.LEFT, padx=20)
        
        # Período
        self.period_label = tk.Label(
            timer_frame,
            text="1º",
            font=("Arial", 60),
            fg="white",
            bg="black"
        )
        self.period_label.pack(side=tk.LEFT, padx=20)
        
        # Botão de opções
        self.options_button = tk.Button(
            timer_frame,
            text=" ...",
            command=self.show_options,
            font=("Arial", 30),
            bg="white"
        )
        self.options_button.pack(side=tk.LEFT, padx=20)
        
    def setup_team_names(self, parent):
        team_names_frame = tk.Frame(parent, bg="black")
        team_names_frame.pack(pady=20) # Time 1
        self.team1_label = tk.Label(
            team_names_frame,
            text="Time 1",
            font=("Arial", 36),
            bg="black",
            fg="white"
        )
        self.team1_label.pack(side=tk.LEFT, padx=40)
        
        # X between team names
        tk.Label(
            team_names_frame,
            text="X",
            font=("Arial", 36, "bold"),
            bg="black",
            fg="white"
        ).pack(side=tk.LEFT, padx=20)
        
        # Time 2
        self.team2_label = tk.Label(
            team_names_frame,
            text="Time 2",
            font=("Arial", 36),
            bg="black",
            fg="white"
        )
        self.team2_label.pack(side=tk.RIGHT, padx=40)
        
    def setup_scoreboard_and_penalties(self, parent):
        scoreboard_frame = tk.Frame(parent, bg="black")
        scoreboard_frame.pack(pady=20)
        
        # Área de penalidades do Time 1
        self.penalty_frame1 = tk.Frame(scoreboard_frame, bg="black")
        self.penalty_frame1.pack(side=tk.LEFT, padx=20)
        
        tk.Button(
            self.penalty_frame1,
            text="+ 2min",
            command=lambda: self.add_penalty(1),
            font=("Arial", 20),
            bg="red",
            fg="white"
        ).pack(pady=10)
        
        # Placar Time 1
        self.score1_label = tk.Label(
            scoreboard_frame,
            text="0",
            font=("Digital-7", 150),
            fg="#00ff00",
            bg="black"
        )
        self.score1_label.pack(side=tk.LEFT, padx=40)
        
        # X entre os placares
        tk.Label(
            scoreboard_frame,
            text="X",
            font=("Arial", 100, "bold"),
            fg="white",
            bg="black"
        ).pack(side=tk.LEFT, padx=40)
        
        # Placar Time 2
        self.score2_label = tk.Label(
            scoreboard_frame,
            text="0",
            font=("Digital-7", 150),
            fg="#00ff00",
            bg="black"
        )
        self.score2_label.pack(side=tk.LEFT, padx=40)
        
        # Área de penalidades do Time 2
        self.penalty_frame2 = tk.Frame(scoreboard_frame, bg="black")
        self.penalty_frame2.pack(side=tk.LEFT, padx=20)
        
        tk.Button(
            self.penalty_frame2,
            text="+ 2min",
            command=lambda: self.add_penalty(2),
            font=("Arial", 20),
            bg="red",
            fg="white"
        ).pack(pady=10)
        
    def setup_additional_controls(self, parent):
        control_frame = tk.Frame(parent, bg="black")
        control_frame.pack(pady=20)
        
        # Botões de controle do placar Time 1
        tk.Button(
            control_frame,
            text="+",
            command=lambda: self.update_score(1, 1),
            font=("Arial", 30),
            bg="white"
        ).pack(side=tk.LEFT, padx=20)
        
        tk.Button(
            control_frame,
            text="-",
            command=lambda: self.update_score(1, -1),
            font=("Arial", 30),
            bg="white"
        ).pack(side=tk.LEFT, padx=20)
        
        # Botões de controle do placar Time 2
        tk.Button(
            control_frame,
            text="+",
            command=lambda: self.update_score(2, 1),
            font=("Arial", 30),
            bg="white"
        ).pack(side=tk.LEFT, padx=20)
        
        tk.Button(
            control_frame,
            text="-",
            command=lambda: self.update_score(2, -1),
            font=("Arial", 30),
            bg="white"
        ).pack(side=tk.LEFT, padx=20)

    def change_team_name(self, team_number):
        current_name = self.team1_label.cget("text") if team_number == 1 else self.team2_label.cget("text")
        new_name = simpledialog.askstring("Mudar Nome", f"Digite o novo nome para o {current_name}")
        if new_name:
            if team_number == 1:
                self.team1_label.config(text=new_name)
            else:
                self.team2_label.config(text=new_name)
    
    def update_score(self, team: int, value: int):
        if team == 1:
            self.score_team1 = max(0, self.score_team1 + value)
            self.score1_label.config(text=str (self.score_team1))
        else:
            self.score_team2 = max(0, self.score_team2 + value)
            self.score2_label.config(text=str(self.score_team2))
        
    def add_penalty(self, team: int):
        if (team == 1 and len(self.penalties_team1) < 4) or (team == 2 and len(self.penalties_team2) < 4):
            player_number = simpledialog.askinteger("Número do Jogador", "Digite o número do jogador que tomou a penalidade")
            if player_number is not None:
                if team == 1:
                    penalty = PenaltyTimer(self.penalty_frame1, lambda: self.remove_penalty(1, penalty), player_number)
                    self.penalties_team1.append(penalty)
                else:
                    penalty = PenaltyTimer(self.penalty_frame2, lambda: self.remove_penalty(2, penalty), player_number)
                    self.penalties_team2.append(penalty)
        else:
            messagebox.showinfo("Limite de Penalidades", "Já existem 4 penalidades em contagem. Para adicionar uma nova, finalize uma ou mais penalidades.")

    def remove_penalty(self, team: int, penalty: PenaltyTimer):
        if team == 1:
            self.penalties_team1.remove(penalty)
        else:
            self.penalties_team2.remove(penalty)
        penalty.frame.destroy()
            
    def toggle_timer(self):
        self.timer_running = not self.timer_running
        self.start_button.config(text="⏸" if self.timer_running else "▶")
        
        if self.timer_running:
            self.update_timer()
            
    def update_timer(self):
        if self.timer_running:
            self.game_time += 1  # Adiciona 1 segundo ao tempo do jogo
            minutes = self.game_time // 60
            seconds = self.game_time % 60
            self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
            
            # Verifica se atingiu 30 minutos no primeiro período
            if self.current_period == 1 and self.game_time >= 30 * 60:
                self.current_period = 2
                self.period_label.config(text="2º")
                self.game_time = 0  # Reseta para 0 segundos
                self.timer_running = False  # Pausa o temporizador
                self.timer_label.config(text="00:00")
                self.start_button.config(text="▶")
            
            # Verifica se atingiu 30 minutos no segundo período
            elif self.current_period == 2 and self.game_time >= 30 * 60:
                self.timer_running = False  # Pausa o temporizador
                self.timer_label.config(text="30:00")
            
            # Atualiza todos os temporizadores de penalidade
            self.penalties_team1 = [p for p in self.penalties_team1 if p.update()]
            self.penalties_team2 = [p for p in self.penalties_team2 if p.update()]
            
            self.root.after(1000, self.update_timer)

    def reset_timer(self):
        self.timer_running = False
        self.game_time = 0  # Reseta para 0 segundos
        self.timer_label.config(text="00:00")
        self.start_button.config(text="▶")
        
    def change_period(self):
        if self.current_period == 1:
            self.current_period = 2
            self.period_label.config(text="2º")
        else:
            self.current_period = 1
            self.period_label.config(text="1º")
        
    def toggle_fullscreen(self):
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))

    def set_custom_time(self):
        custom_time = simpledialog.askstring("Tempo Personalizado", "Digite o tempo no formato MM:SS:")
        if custom_time:
            try:
                minutes, seconds = map(int, custom_time.split(':'))
                total_seconds = minutes * 60 + seconds
                if 0 <= total_seconds <= 30 * 60:
                    self.game_time = total_seconds
                    self.timer_label.config(text=custom_time)
                else:
                    messagebox.showerror("Erro", "O tempo deve estar entre 00:00 e 30:00.")
            except:
                messagebox.showerror("Erro", "Formato inválido. Use MM:SS.")

    def show_options(self):
        if hasattr(self, 'options_window') and self.options_window.winfo_exists():
            self.options_window.lift()
            return

        self.options_window = tk.Toplevel(self.root)
        self.options_window.title("Opções")
        self.options_window.configure(bg="black")
        
        tk.Button(
            self.options_window,
            text="Reiniciar Tempo",
            command=self.reset_timer,
            font=("Arial", 20),
            bg="white"
        ).pack(pady=10)
        
        tk.Button(
            self.options_window,
            text="Trocar Período",
            command=self.change_period,
            font=("Arial", 20),
            bg="white"
        ).pack(pady=10)
        
        tk.Button(
            self.options_window,
            text="Tela Cheia",
            command=self.toggle_fullscreen,
            font=("Arial", 20),
            bg="white"
        ).pack(pady=10)
        
        tk.Button(
            self.options_window,
            text="Definir Tempo",
            command=self.set_custom_time,
            font=("Arial", 20),
            bg="white"
        ).pack(pady=10)

        tk.Button(
            self.options_window,
            text="Mudar Nome Time 1",
            command=lambda: self.change_team_name(1),
            font=("Arial", 20),
            bg="white"
        ).pack(pady=10)

        tk.Button(
            self.options_window,
            text="Mudar Nome Time 2",
            command=lambda: self.change_team_name(2),
            font=("Arial", 20),
            bg="white"
        ).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = HandballScoreboard(root)
    root.mainloop()
