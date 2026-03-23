import tkinter as tk

ANCHO = 800
ALTO = 400

class MarioGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Mario Bonito 🍄")

        self.canvas = tk.Canvas(root, width=ANCHO, height=ALTO, bg="#5c94fc")
        self.canvas.pack()

        # Suelo
        self.suelo = self.canvas.create_rectangle(0, 350, 2000, 400, fill="#8B4513")

        # Mario (grupo de figuras)
        self.mario_parts = []
        self.crear_mario(100, 300)

        # Bloques
        self.blocks = []
        for x in range(300, 900, 100):
            b = self.crear_bloque(x, 260)
            self.blocks.append(b)

        # Monedas
        self.coins = []
        for x in range(350, 900, 150):
            c = self.crear_moneda(x, 200)
            self.coins.append(c)

        # Goombas
        self.goombas = []
        for x in range(600, 1200, 300):
            g = self.crear_goomba(x, 320)
            self.goombas.append({"id": g, "dir": -2})

        # Física
        self.vel_y = 0
        self.en_suelo = False

        # Score
        self.score = 0
        self.label = tk.Label(root, text="Puntos: 0", font=("Arial", 14))
        self.label.pack()

        # Controles
        self.root.bind("<Left>", self.left)
        self.root.bind("<Right>", self.right)
        self.root.bind("<space>", self.jump)

        self.loop()

    # ===== CREAR FIGURAS =====

    def crear_mario(self, x, y):
        cabeza = self.canvas.create_oval(x, y, x+20, y+20, fill="#ffcc99")
        gorra = self.canvas.create_rectangle(x, y-5, x+20, y+5, fill="red")
        cuerpo = self.canvas.create_rectangle(x, y+20, x+20, y+40, fill="blue")
        pierna1 = self.canvas.create_rectangle(x, y+40, x+8, y+55, fill="brown")
        pierna2 = self.canvas.create_rectangle(x+12, y+40, x+20, y+55, fill="brown")

        self.mario_parts = [cabeza, gorra, cuerpo, pierna1, pierna2]

    def crear_bloque(self, x, y):
        base = self.canvas.create_rectangle(x, y, x+50, y+40, fill="#c97e2a")
        detalle = self.canvas.create_rectangle(x+5, y+5, x+45, y+35, outline="#8b5a2b")
        return base

    def crear_moneda(self, x, y):
        return self.canvas.create_oval(x, y, x+20, y+20, fill="gold", outline="orange")

    def crear_goomba(self, x, y):
        cuerpo = self.canvas.create_oval(x, y, x+30, y+30, fill="#8B4513")
        ojos = self.canvas.create_oval(x+5, y+5, x+10, y+10, fill="white")
        ojos2 = self.canvas.create_oval(x+20, y+5, x+25, y+10, fill="white")
        return cuerpo

    # ===== MOVIMIENTO =====

    def mover_mario(self, dx, dy):
        for part in self.mario_parts:
            self.canvas.move(part, dx, dy)

    def left(self, e):
        self.mover_mario(-10, 0)

    def right(self, e):
        self.mover_mario(10, 0)

    def jump(self, e):
        if self.en_suelo:
            self.vel_y = -15
            self.en_suelo = False

    def gravedad(self):
        self.vel_y += 1
        self.mover_mario(0, self.vel_y)

        x1, y1, x2, y2 = self.canvas.bbox(self.mario_parts[0])

        if y2 >= 350:
            dy = 350 - y2
            self.mover_mario(0, dy)
            self.vel_y = 0
            self.en_suelo = True

    # ===== GOOMBAS =====

    def mover_goombas(self):
        for g in self.goombas:
            self.canvas.move(g["id"], g["dir"], 0)
            x1, _, x2, _ = self.canvas.coords(g["id"])

            if x1 < 0 or x2 > 2000:
                g["dir"] *= -1

    # ===== COLISIONES =====

    def colision_bbox(self, bbox1, bbox2):
        return not (
            bbox1[2] < bbox2[0] or
            bbox1[0] > bbox2[2] or
            bbox1[3] < bbox2[1] or
            bbox1[1] > bbox2[3]
        )

    def check_colisiones(self):
        mario_box = self.canvas.bbox(self.mario_parts[0])

        # Monedas
        for c in self.coins[:]:
            if self.colision_bbox(mario_box, self.canvas.coords(c)):
                self.canvas.delete(c)
                self.coins.remove(c)
                self.score += 10

        # Goombas
        for g in self.goombas[:]:
            if self.colision_bbox(mario_box, self.canvas.coords(g["id"])):
                self.game_over()

    # ===== GAME =====

    def game_over(self):
        self.canvas.create_text(400, 200, text="GAME OVER", font=("Arial", 30))
        self.root.unbind("<Left>")
        self.root.unbind("<Right>")
        self.root.unbind("<space>")

    def loop(self):
        self.gravedad()
        self.mover_goombas()
        self.check_colisiones()

        self.label.config(text=f"Puntos: {self.score}")

        self.root.after(30, self.loop)

# Ejecutar
if __name__ == "__main__":
    root = tk.Tk()
    game = MarioGame(root)
    root.mainloop()