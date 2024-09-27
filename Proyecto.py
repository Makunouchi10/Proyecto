import tkinter as tk
import random
from tkinter import messagebox


class JuegoDeBarcos:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Juego de Barcos")

        # Mostrar mensaje al usuario
        self.mostrar_aviso()

        self.barco_posiciones = []
        self.intentos = []
        self.nivel_actual = 0
        self.puntaje_por_nivel = []
        self.intentos_maximos = [7, 12, 19]  # Intentos por nivel
        self.limite_numeros = [9, 16, 25]  # Límites de números por nivel
        self.juegos_jugados = []  # Guarda todas las partidas jugadas

        self.menu_principal()
        self.ventana.mainloop()

    def mostrar_aviso(self):
        messagebox.showinfo("Aviso", "Por favor, agranda la ventana del juego para una mejor experiencia.")

    def menu_principal(self):
        self.limpiar_ventana()
        tk.Label(self.ventana, text="Bienvenido al Juego de Barcos").pack(pady=10)

        tk.Button(self.ventana, text="Comenzar Nuevo Juego", command=self.comenzar_juego).pack(pady=5)
        tk.Button(self.ventana, text="Instrucciones", command=self.mostrar_instrucciones).pack(pady=5)
        tk.Button(self.ventana, text="Ver Puntaje", command=self.mostrar_puntaje).pack(pady=5)
        tk.Button(self.ventana, text="Salir", command=self.ventana.quit).pack(pady=5)

    def limpiar_ventana(self):
        for widget in self.ventana.winfo_children():
            widget.destroy()

    def comenzar_juego(self):
        self.limpiar_ventana()
        self.nivel_actual = 0
        self.intentos = []
        self.iniciar_nivel()

    def iniciar_nivel(self):
        self.intentos = []
        self.barco_posiciones = [random.randint(1, self.limite_numeros[self.nivel_actual]) for _ in range(3)]
        tk.Label(self.ventana, text=f"Nivel {self.nivel_actual + 1}").pack(pady=10)
        tk.Label(self.ventana, text=f"Realiza tiros del {1} al {self.limite_numeros[self.nivel_actual]}").pack(pady=5)
        self.entrada = tk.Entry(self.ventana)
        self.entrada.pack(pady=5)
        tk.Button(self.ventana, text="Adivinar", command=self.adivinar).pack(pady=5)
        self.resultado_label = tk.Label(self.ventana, text="")
        self.resultado_label.pack(pady=5)
        self.intentos_label = tk.Label(self.ventana, text="")
        self.intentos_label.pack(pady=5)
        self.intentos_restantes_label = tk.Label(self.ventana,
                                                 text=f"Intentos restantes: {self.intentos_maximos[self.nivel_actual]}")
        self.intentos_restantes_label.pack(pady=5)

        tk.Button(self.ventana, text="Reiniciar Juego", command=self.reiniciar_juego).pack(pady=5)

    def adivinar(self):
        try:
            intento = int(self.entrada.get())

            # Verificar si el intento está dentro del rango permitido
            if intento < 1 or intento > self.limite_numeros[self.nivel_actual]:
                self.resultado_label.config(
                    text=f"Por favor, ingresa un número entre 1 y {self.limite_numeros[self.nivel_actual]}.")
                return

            # Verificar si el número ya fue intentado
            if intento in self.intentos:
                self.resultado_label.config(text=f"Ya has intentado el número {intento}. Elige otro.")
                return

            self.intentos.append(intento)

            if intento in self.barco_posiciones:
                self.barco_posiciones.remove(intento)
                self.resultado_label.config(text=f"¡Acertaste en {intento}!")

                if not self.barco_posiciones:
                    tiros_utilizados = len(self.intentos)
                    puntaje = max(0, 10 - tiros_utilizados)  # Puntaje mínimo de 0
                    self.puntaje_por_nivel.append((self.nivel_actual + 1, puntaje))  # Guarda nivel y puntaje
                    self.juegos_jugados.append((self.nivel_actual + 1, puntaje))  # Guarda solo para la tabla

                    if self.nivel_actual < 2:
                        tk.Button(self.ventana, text="Siguiente Nivel", command=self.siguiente_nivel).pack(pady=5)
                    else:
                        tk.Label(self.ventana, text="¡Felicidades, has ganado el juego!").pack(pady=5)
            else:
                self.resultado_label.config(text=f"Fallaste en {intento}.")

            self.intentos_label.config(text=f"Realizaste tiros en: {', '.join(map(str, self.intentos))}")
            intentos_restantes = self.intentos_maximos[self.nivel_actual] - len(self.intentos)
            self.intentos_restantes_label.config(text=f"Intentos restantes: {intentos_restantes}")

            if len(self.intentos) >= self.intentos_maximos[self.nivel_actual]:
                tiros_utilizados = len(self.intentos)
                puntaje = max(0, 10 - tiros_utilizados)  # Puntaje mínimo de 0
                self.juegos_jugados.append((self.nivel_actual + 1, puntaje))  # Guarda el resultado aunque pierda
                self.resultado_label.config(text="Se acabaron los intentos. ¡Juego terminado!")
                self.intentos_restantes_label.config(text="")

        except ValueError:
            self.resultado_label.config(text="Por favor, ingresa un número válido.")

    def siguiente_nivel(self):
        self.nivel_actual += 1
        self.limpiar_ventana()
        self.iniciar_nivel()

    def reiniciar_juego(self):
        self.limpiar_ventana()
        self.menu_principal()

    def mostrar_instrucciones(self):
        self.limpiar_ventana()
        instrucciones = (
            "Instrucciones:\n"
            "1. Adivina la posición de los barcos en los niveles.\n"
            "2. Nivel 1: Adivina del 1 al 9 (7 intentos).\n"
            "3. Nivel 2: Adivina del 1 al 16 (12 intentos).\n"
            "4. Nivel 3: Adivina del 1 al 25 (19 intentos).\n"
            "5. Por cada acierto, avanzas al siguiente nivel."
        )
        tk.Label(self.ventana, text=instrucciones).pack(pady=10)
        tk.Button(self.ventana, text="Regresar", command=self.menu_principal).pack(pady=5)

    def mostrar_puntaje(self):
        self.limpiar_ventana()
        if not self.juegos_jugados:
            tk.Label(self.ventana, text="No has jugado ningún juego todavía.").pack(pady=10)
        else:
            tk.Label(self.ventana, text="Detalles de los Juegos Jugados:").pack(pady=10)
            tk.Label(self.ventana, text="Nivel | Puntaje").pack(pady=5)
            tk.Label(self.ventana, text="-------------------").pack(pady=5)
            for nivel, puntaje in self.juegos_jugados:
                tk.Label(self.ventana, text=f"{nivel}    | {puntaje}").pack(pady=2)

        tk.Button(self.ventana, text="Regresar", command=self.menu_principal).pack(pady=5)


if __name__ == "__main__":
    JuegoDeBarcos()
