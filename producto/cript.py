import tkinter as tk
import random

ANCHO = 800
ALTO = 400

class FightGame:
    def __init__(self, root):
        self.root = root
        self.root.title("FIGHT GAME 🔥")

        self.canvas = tk.Canvas(root, width=ANCHO, height=ALTO, bg="black")
        self.canvas.pack()

        # Jugador
        self.p1 = self.crear_personaje(100, "cyan")
        self.p2 = self.crear_personaje(600, "red")

        self.p1_hp = 100
        self.p2_hp = 100

        self.p1_vel = 0
        self.p2_vel = 0

        self.p1_jumping = False
        self.p2_jumping = False

        # UI
        self.hp1_bar = self.canvas.create_rectangle(50, 20, 250, 40, fill="green")
        self.hp2_bar = self.canvas.create_rectangle(550, 20, 750, 40, fill="green")

        # Controles
        self.root.bind("<a>", lambda e: self.mover(self.p1, -10))
        self.root.bind("<d>", lambda e: self.mover(self.p1, 10))
        self.root.bind("<w>", lambda e: self.saltar(self.p1))
        self.root.bind("<j>", lambda e: self.golpe(self.p1, self.p2, 10))
        self.root.bind("<k>", lambda e: self.golpe(self.p1, self.p2, 15))

        self.loop()

    def crear_personaje(self, x, color):
        cuerpo = self.canvas.create_rectangle(x, 250, x+40, 350, fill=color)
        cabeza = self.canvas.create_oval(x, 220, x+40, 250, fill=color)
        return [cuerpo, cabeza]

    def mover(self, personaje, dx):
        for p in personaje:
            self.canvas.move(p, dx, 0)

    def saltar(self, personaje):
        if not self.p1_jumping:
            self.p1_vel = -15
            self.p1_jumping = True

    def gravedad(self):
        if self.p1_jumping:
            self.p1_vel += 1
            for p in self.p1:
                self.canvas.move(p, 0, self.p1_vel)

            if self.canvas.coords(self.p1[0])[3] >= 350:
                dy = 350 - self.canvas.coords(self.p1[0])[3]
                for p in self.p1:
                    self.canvas.move(p, 0, dy)
                self.p1_vel = 0
                self.p1_jumping = False

    def golpe(self, atacante, defensor, daño):
        ax1, ay1, ax2, ay2 = self.canvas.coords(atacante[0])
        bx1, by1, bx2, by2 = self.canvas.coords(defensor[0])

        if abs(ax1 - bx1) < 60:
            if defensor == self.p2:
                self.p2_hp -= daño
            else:
                self.p1_hp -= daño

    def ia(self):
        ax1, _, _, _ = self.canvas.coords(self.p1[0])
        bx1, _, _, _ = self.canvas.coords(self.p2[0])

        # acercarse
        if bx1 > ax1:
            self.mover(self.p2, -3)
        else:
            self.mover(self.p2, 3)

        # atacar
        if random.randint(1, 20) == 1:
            self.golpe(self.p2, self.p1, 10)

    def actualizar_ui(self):
        self.canvas.coords(self.hp1_bar, 50, 20, 50 + self.p1_hp*2, 40)
        self.canvas.coords(self.hp2_bar, 750 - self.p2_hp*2, 20, 750, 40)

    def game_over(self):
        texto = "GANASTE 🔥" if self.p2_hp <= 0 else "PERDISTE 💀"
        self.canvas.create_text(400, 200, text=texto, fill="white", font=("Arial", 30))

    def loop(self):
        if self.p1_hp <= 0 or self.p2_hp <= 0:
            self.game_over()
            return

        self.gravedad()
        self.ia()
        self.actualizar_ui()

        self.root.after(30, self.loop)

# Ejecutar
if __name__ == "__main__":
    root = tk.Tk()
    game = FightGame(root)
    root.mainloop()