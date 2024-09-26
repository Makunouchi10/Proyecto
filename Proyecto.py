import tkinter as tk
import random


class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Circles")
        self.root.configure(bg="black")

        self.score = 0
        self.time_limit = None
        self.time_remaining = 0
        self.scores_dict = {
            15: [],
            30: [],
            float('inf'): []
        }

        self.instructions = (
            "Instrucciones:\n"
            "1. Presiona el círculo que aparece en la pantalla.\n"
            "2. El círculo cambiará de lugar y tamaño.\n"
            "3. Cada clic exitoso incrementa tu puntaje.\n"
            "4. ¡Intenta alcanzar la mayor puntuación posible!"
        )

        self.create_main_menu()

    def create_main_menu(self):
        self.main_menu_frame = tk.Frame(self.root, bg="black")
        self.main_menu_frame.pack(pady=20)

        self.instructions_button = tk.Button(
            self.main_menu_frame, text="Instrucciones", command=self.show_instructions,
            bg="black", fg="white", highlightbackground="purple", bd=5
        )
        self.instructions_button.pack(pady=5)

        self.start_game_button = tk.Button(
            self.main_menu_frame, text="Iniciar Juego", command=self.select_game_mode,
            bg="black", fg="white", highlightbackground="purple", bd=5
        )
        self.start_game_button.pack(pady=5)

    def show_instructions(self):
        instructions_window = tk.Toplevel(self.root)
        instructions_window.title("Instrucciones")
        instructions_window.configure(bg="black")
        instructions_label = tk.Label(instructions_window, text=self.instructions, justify="left", bg="black",
                                      fg="white")
        instructions_label.pack(padx=10, pady=10)
        close_button = tk.Button(instructions_window, text="Cerrar", command=instructions_window.destroy, bg="black",
                                 fg="white", highlightbackground="purple", bd=5)
        close_button.pack(pady=5)

    def select_game_mode(self):
        self.main_menu_frame.pack_forget()  # Ocultar el menú principal

        self.mode_frame = tk.Frame(self.root, bg="black")
        self.mode_frame.pack(pady=20)

        self.label = tk.Label(self.mode_frame, text="Selecciona la duración del juego:", bg="black", fg="white")
        self.label.pack(pady=5)

        self.quick_button = tk.Button(
            self.mode_frame, text="Rápido (15 segundos)", command=lambda: self.start_game(15),
            bg="black", fg="white", highlightbackground="purple", bd=5
        )
        self.quick_button.pack(pady=5)

        self.normal_button = tk.Button(
            self.mode_frame, text="Normal (30 segundos)", command=lambda: self.start_game(30),
            bg="black", fg="white", highlightbackground="purple", bd=5
        )
        self.normal_button.pack(pady=5)

        self.infinity_button = tk.Button(
            self.mode_frame, text="Infinito", command=lambda: self.start_game(float('inf')),
            bg="black", fg="white", highlightbackground="purple", bd=5
        )
        self.infinity_button.pack(pady=5)

    def start_game(self, duration):
        self.time_limit = duration
        self.score = 0
        self.time_remaining = duration
        self.update_score()

        # Ocultar botones de duración
        self.mode_frame.pack_forget()

        self.canvas = tk.Canvas(self.root, width=300, height=300, bg="black")
        self.canvas.pack()

        self.timer_label = tk.Label(self.root, text=f"Tiempo Restante: {self.time_remaining}", bg="black", fg="white")
        self.timer_label.pack(pady=10)

        self.update_circle()
        self.change_background_color()  # Cambiar el fondo

        if self.time_limit != float('inf'):
            self.update_timer()  # Comenzar el temporizador
        else:
            self.endless_mode_buttons()  # Agregar botón para terminar el juego infinito

    def change_background_color(self):
        pastel_colors = ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF"]
        new_color = random.choice(pastel_colors)
        self.canvas.configure(bg=new_color)
        self.root.after(100, self.change_background_color)  # Cambiar color cada 0.5 segundos

    def endless_mode_buttons(self):
        self.end_game_button = tk.Button(
            self.root, text="Terminar Juego", command=self.end_game,
            bg="black", fg="white", highlightbackground="purple", bd=5
        )
        self.end_game_button.pack(pady=5)

    def update_circle(self):
        if hasattr(self, 'circle') and self.circle is not None:
            self.canvas.delete(self.circle)

        size = random.randint(30, 100)
        x = random.randint(0, 300 - size)
        y = random.randint(0, 300 - size)

        self.circle = self.canvas.create_oval(x, y, x + size, y + size, fill="beige", outline="black")
        self.canvas.tag_bind(self.circle, "<Button-1>", self.circle_clicked)

    def circle_clicked(self, event):
        self.score += 1
        self.update_score()
        self.update_circle()

    def update_score(self):
        if not hasattr(self, 'score_label'):
            self.score_label = tk.Label(self.root, text="Puntaje: 0", bg="black", fg="white")
            self.score_label.pack(pady=10)

        self.score_label.config(text=f"Puntaje: {self.score}")

    def update_timer(self):
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.timer_label.config(text=f"Tiempo Restante: {self.time_remaining}")
            self.root.after(1000, self.update_timer)  # Actualizar cada segundo
        else:
            self.end_game()

    def end_game(self):
        if hasattr(self, 'end_game_button'):
            self.end_game_button.pack_forget()  # Ocultar botón de terminar juego

        self.canvas.pack_forget()  # Ocultar el canvas
        self.timer_label.pack_forget()  # Ocultar el temporizador
        self.end_label = tk.Label(self.root, text=f"Juego Terminado!\nPuntaje Final: {self.score}", bg="black",
                                  fg="white")
        self.end_label.pack(pady=10)

        self.scores_dict[self.time_limit].append(self.score)  # Almacenar puntaje por duración
        self.scores_dict[self.time_limit].sort(reverse=True)  # Ordenar de mayor a menor

        self.restart_button = tk.Button(self.root, text="Reiniciar Partida", command=self.restart_game, bg="black",
                                        fg="white", highlightbackground="purple", bd=5)
        self.restart_button.pack(pady=5)

        self.exit_button = tk.Button(self.root, text="Salir", command=self.root.quit, bg="black", fg="white",
                                     highlightbackground="purple", bd=5)
        self.exit_button.pack(pady=5)

        self.show_scores_button = tk.Button(self.root, text="Mostrar Puntuaciones", command=self.show_scores,
                                            bg="black", fg="white", highlightbackground="purple", bd=5)
        self.show_scores_button.pack(pady=5)

    def show_scores(self):
        scores_window = tk.Toplevel(self.root)
        scores_window.title("Puntuaciones")
        scores_window.configure(bg="black")

        scores_text = tk.Text(scores_window, width=50, height=20, bg="black", fg="white")
        scores_text.pack(padx=10, pady=10)

        # Mostrar puntuaciones clasificadas por duración
        for duration in [15, 30, float('inf')]:
            scores_text.insert(tk.END, f"\nPuntuaciones para {duration} segundos:\n")
            for score in self.scores_dict[duration]:
                scores_text.insert(tk.END, f"Puntaje: {score}\n")

        close_button = tk.Button(scores_window, text="Cerrar", command=scores_window.destroy, bg="black", fg="white",
                                 highlightbackground="purple", bd=5)
        close_button.pack(pady=5)

    def restart_game(self):
        # Ocultar botones de reinicio y salida
        self.end_label.pack_forget()  # Ocultar mensaje de finalización
        self.restart_button.pack_forget()  # Ocultar botón de reinicio
        self.exit_button.pack_forget()  # Ocultar botón de salir
        self.show_scores_button.pack_forget()  # Ocultar botón de mostrar puntuaciones

        self.select_game_mode()  # Volver a seleccionar duración


if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.geometry("800x600")  # Establecer el tamaño de la ventana
    root.mainloop()
