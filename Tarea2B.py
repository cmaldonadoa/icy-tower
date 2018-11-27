import pygame as pg
import random as r

# ---- Colores
black = (0, 0, 0)
white = (255, 255, 255)
gray = (150, 150, 150)
red = (255, 0, 0)
green = (0, 255, 50)
green2 = (0, 180, 0)
blue = (45, 120, 210)
yellow = (255, 255, 0)
brown = (110, 70, 20)
brown1 = (99, 60, 35)
lbrown = (130, 100, 50)
dbrown = (85, 30, 0)
ddbrown = (60, 30, 8)

vector = pg.math.Vector2

# ---- Clases de cada Sprite
class Jugador(pg.sprite.Sprite):
    def __init__(self, pos, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size

        self.image = pg.Surface((4*self.size, 3*self.size))
        self.image.fill(white)
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.pos = self.rect.midbottom
        self.vel = vector(0, 0)
        self.acc = vector(0, 0)
        self.puntaje = 0
        self.hi_score = 0

        # Dibujar al personaje
        pg.draw.rect(self.image, green, (0, 5 * self.size // 2, 3 * self.size // 2, self.size // 2), 0)
        pg.draw.rect(self.image, green, (5 * self.size//2, 5 * self.size // 2, 3 * self.size // 2, self.size // 2), 0)
        pg.draw.ellipse(self.image, green, (0, self.size // 2, 4 * self.size - 1, 2 * self.size - 1), 0)
        pg.draw.line(self.image, black, (0, 3 * self.size // 2), (4 * self.size, 3 * self.size // 2), 2)
        pg.draw.circle(self.image, yellow, (self.size, self.size // 2), self.size // 2, 0)
        pg.draw.circle(self.image, yellow, (3 * self.size, self.size // 2), self.size // 2, 0)
        pg.draw.circle(self.image, black, (self.size, self.size // 2), self.size // 4, 0)
        pg.draw.circle(self.image, black, (3 * self.size, self.size // 2), self.size // 4, 0)

    def update(self):
        # ---- Moviemiento del jugador
        self.acc = vector(0, 0.8)
        if pg.key.get_pressed()[pg.K_LEFT]:
            self.acc.x = -0.7
        if pg.key.get_pressed()[pg.K_RIGHT]:
            self.acc.x = 0.7
        if pg.key.get_pressed()[pg.K_SPACE]:
            self.rect.y += 1
            choque = pg.sprite.spritecollide(self, plataformas, False)
            self.rect.y -= 1
            # Saltar solo si esta parado en una plataforma; salto depende de la velocidad en x
            if choque:
                self.vel.y = -12 - abs(self.vel.x)

        # ---- Desaceleracion por friccion
        self.acc.x -= self.vel.x * 0.1

        # ---- Cambios de velocidad y posicion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

class Plataforma(pg.sprite.Sprite):
    def __init__(self, pos, dim, n):
        pg.sprite.Sprite.__init__(self)
        self.x = int(pos[0])
        self.y = int(pos[1])
        self.alto = dim[1]
        self.ancho = dim[0]

        self.image = pg.Surface((self.ancho, self.alto))
        self.image.fill(red)
        self.image.set_colorkey(red)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # Dibujar diseño
        if n == 1:
            i = 1
            while self.alto // 2 + i*self.alto < self.ancho:
                pg.draw.circle(self.image, (0, 100, 51), (self.alto // 2 + i * self.alto, 0), self.alto, 0)
                pg.draw.line(self.image, (0, 60, 16), (self.alto // 2 + i * self.alto, 0), (self.alto // 2 + i * self.alto, self.alto - 5), 2)
                i += 1
            pg.draw.circle(self.image, (0, 100, 51), (self.alto // 2 + (i+1) * self.alto, 0), self.alto, 0)

            i = 0
            while self.alto // 2 + i * self.alto < self.ancho:
                pg.draw.circle(self.image, (0, 185, 142), (self.alto // 2 + 2 * i * self.alto, 0), self.alto, 0)
                pg.draw.line(self.image, (0, 117, 76), (self.alto // 2 + 2 * i * self.alto, 0), (self.alto // 2 + 2 * i * self.alto, self.alto - 5), 2)
                i += 1

        if n == 2:
            i = 0
            while self.alto // 2 + i * self.alto <= self.ancho:
                pg.draw.circle(self.image, (200, 200, 240), (self.alto // 2 + i * self.alto, self.alto // 2), self.alto // 2, 0)
                pg.draw.circle(self.image, white, (self.alto // 2 + self.alto // 5 + i * self.alto, self.alto // 2), self.alto // 2, 0)
                i += 1

        if n == 3:
            pg.draw.rect(self.image, brown, (0, 0, self.ancho, self.alto), 0)
            for i in range(20):
                R = r.randint(self.alto // 7, self.alto // 4)
                pg.draw.circle(self.image, r.choice([dbrown, lbrown]), ((2 * (i+1) // 3) * self.ancho // 10, r.randint(R, self.alto - R)), R, 0)
            pg.draw.rect(self.image, (50, 120, 70), (0, 0, self.ancho, self.alto // 5), 0)
            v = self.ancho // 10
            for n in range(10):
                pg.draw.polygon(self.image, (50, 120, 70), ((n * v, self.alto // 5), ((n + 1) * v, self.alto // 5), ((2 * n + 1) * v // 2,  self.alto // 3)), 0)

class Muro(pg.sprite.Sprite):
    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((70, 200))
        self.image.fill(brown1)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        # Dibujar diseño
        pg.draw.aaline(self.image, ddbrown, (22, 0), (21, 200), 1)
        pg.draw.aaline(self.image, lbrown, (3, 0), (4, 200), 1)
        pg.draw.aaline(self.image, lbrown, (10, 0), (8, 200), 1)
        pg.draw.aaline(self.image, dbrown, (15, 0), (14, 200), 1)
        pg.draw.aaline(self.image, lbrown, (26, 0), (28, 200), 1)
        pg.draw.aaline(self.image, dbrown, (33, 0), (32, 200), 1)
        pg.draw.aaline(self.image, ddbrown, (30, 0), (31, 200), 1)
        pg.draw.aaline(self.image, dbrown, (50, 0), (47, 200), 1)
        pg.draw.aaline(self.image, dbrown, (57, 0), (57, 200), 1)
        pg.draw.aaline(self.image, dbrown, (66, 0), (65, 200), 1)
        pg.draw.aaline(self.image, lbrown, (48, 0), (53, 200), 1)
        pg.draw.aaline(self.image, dbrown, (41, 0), (42, 200), 1)
        pg.draw.aaline(self.image, lbrown, (60, 0), (63, 200), 1)
        pg.draw.aaline(self.image, lbrown, (54, 0), (59, 200), 1)
        pg.draw.aaline(self.image, lbrown, (38, 0), (37, 200), 1)

        pg.draw.rect(self.image, gray, [0, 0, 100, 9], 0)
        pg.draw.rect(self.image, gray, [0, 191, 100, 9], 0)
        pg.draw.rect(self.image, black, [0, 0, 100, 1], 0)
        pg.draw.rect(self.image, black, [0, 199, 100, 1], 0)

        pg.draw.ellipse(self.image, brown1, (30, 60, 30, 53), 0)
        pg.draw.ellipse(self.image, (90,50,7), (33, 64, 26, 47), 0)
        pg.draw.ellipse(self.image, brown, (36, 67, 23, 38), 0)
        pg.draw.ellipse(self.image, (90,61,18), (40, 70, 16, 32), 0)
        pg.draw.ellipse(self.image, brown, (43, 74, 12, 26), 0)
        pg.draw.ellipse(self.image, (90,50,7), (45, 77, 8, 19), 0)
        pg.draw.ellipse(self.image, brown, (47, 78, 5, 14), 0)

class Enemigo(pg.sprite.Sprite):
    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((60, 20))
        self.image.fill(blue)
        self.image.set_colorkey(blue)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.dir = "i"

        # Dibujar diseño
        pg.draw.rect(self.image, gray, (0, 0, 60, 14), 0)
        for n in range(10):
            pg.draw.polygon(self.image, white, ((6 * n, 14),(6 + 6 * n, 14),(3 + 6 * n, 20)), 0)
        pg.draw.ellipse(self.image, yellow, (10, 4, 10, 6), 0)
        pg.draw.ellipse(self.image, yellow, (40, 4, 10, 6), 0)
        pg.draw.line(self.image, black, (15, 4), (15, 10), 2)
        pg.draw.line(self.image, black, (45, 4), (45, 10), 2)

    def update(self):
        if self.dir == "i" and self.rect.left <= 50:
            self.dir = "d"
            self.rect.left = 50
        elif self.dir == "d" and self.rect.right >= 500:
            self.dir = "i"
            self.rect.right = 500

        if self.dir == "i":
            self.rect.x -= 5

        else:
            self.rect.x += 5

class Indicador(pg.sprite.Sprite):
    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((60, 20))
        self.image.fill(blue)
        self.image.set_colorkey(blue)
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0], 5)
        self.dir = "i"

        # Dibujar diseño
        pg.draw.polygon(self.image, red, ((30, 0), (23, 17), (38, 17)), 3)

    def update(self):
        if self.dir == "i" and self.rect.left <= 50:
            self.dir = "d"
            self.rect.left = 50
        elif self.dir == "d" and self.rect.right >= 500:
            self.dir = "i"
            self.rect.right = 500

        if self.dir == "i":
            self.rect.x -= 5

        else:
            self.rect.x += 5

# ---- Muros
muros_lista = []
for x in [-20, 500]:
    for y in range(5):
        M = Muro((x, 200 * (2 - y)))
        muros_lista.append(M)

# ---- Plataformas y jugador
j = Jugador((275,500), 9)
suelo = Plataforma([50, 570], [450, 30], 3)
plataformas_lista = [suelo]
# Crear 5 plataformas iniciales
for n in range(5):
    A = r.randint(100, 200)
    d = r.randint(1, 3)
    p = Plataforma([r.randint(50, 550 - A - 50), 20 + 110 * n], [A, 20], d)
    plataformas_lista.append(p)

# ---- Añadir sprites
sprites = pg.sprite.Group()
plataformas = pg.sprite.Group()
muros = pg.sprite.Group()
enemigos = pg.sprite.Group()
indicador_enemigos = pg.sprite.Group()

sprites.add(j)
for muro in muros_lista:
    sprites.add(muro)
    muros.add(muro)
for plataforma in plataformas_lista:
    sprites.add(plataforma)
    plataformas.add(plataforma)

# ---- Pantalla
dimensiones = (550, 600)
screen = pg.display.set_mode(dimensiones)
pg.display.set_caption("Icy Tower")

# ---- Variables
pg.init()
fps = 60
font = pg.font.SysFont("arial black", 20)
reloj = pg.time.Clock()
jugar = True
reiniciar = False

# ---- Ciclo principal
while jugar:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            jugar = False

    # ---- Limite de fps
    reloj.tick(fps)

    # ---- Limpiar la pantalla
    screen.fill(blue)

    # ---- Rehacer la escena inicial si termina el juego
    if reiniciar:
        reiniciar = False

        # Reestablecer posicion inicial
        j.pos.x = 275
        j.pos.y = 500
        j.vel.x = 0
        j.vel.y = 0
        ptj_anterior = j.puntaje
        j.puntaje = 0

        # Reiniciar plataformas
        for plataforma in plataformas:
            plataforma.kill()

        suelo = Plataforma([50, 570], [450, 30], 3)
        sprites.add(suelo)
        plataformas.add(suelo)
        for n in range(5):
            A = r.randint(100, 200)
            d = r.randint(1, 3)
            p = Plataforma([r.randint(50, 550 - A - 50), 20 + 110 * n], [A, 20], d)
            sprites.add(p)
            plataformas.add(p)

        # Reiniciar muros
        for muro in muros:
            muro.kill()

        for x in [-20, 500]:
            for y in range(5):
                M = Muro((x, 200 * (2 - y)))
                sprites.add(M)
                muros.add(M)

        # Quitar enemigos
        for enemigo in enemigos:
            enemigo.kill()

        # Comprar puntaje maximo
        if ptj_anterior > j.hi_score:
            j.hi_score = ptj_anterior

    # ---- Actualizar la pantalla
    sprites.update()
    sprites.draw(screen)

    # ---- Visualizar puntaje actual y maximo
    ptj = font.render("Score: " + str(int(j.puntaje)), 1, white)
    screen.blit(ptj, (400, 20))
    hs = font.render("Hi-Score: " + str(int(j.hi_score)), 1, white)
    screen.blit(hs, (369, 40))

    # ---- Moviemiento de la camara
    if j.rect.top < 200:
        if j.vel.y < 0:
            j.puntaje += abs(j.vel.y)
            j.pos.y += abs(j.vel.y)
            for plataforma in plataformas:
                plataforma.rect.y += abs(j.vel.y)
                if plataforma.rect.top > 600:
                    plataforma.kill()
            for muro in muros:
                muro.rect.y += abs(j.vel.y)
                if muro.rect.top > 800:
                    muro.kill()
            for enemigo in enemigos:
                enemigo.rect.y += abs(j.vel.y)
                if enemigo.rect.bottom > 0:
                    for indicador in indicador_enemigos:
                        indicador.kill()
                if enemigo.rect.top > 800:
                    enemigo.kill()

    # ---- Generar plataformas a medida que desaparecen
    while len(plataformas) < 6:
        # Largo disminuye con el puntaje
        A = r.randint(100, 150) - int(j.puntaje / 200)
        B = r.randint(40, 85)
        d = r.randint(1, 3)
        p = Plataforma([r.randint(50, 550 - max(A, B) - 50), -90], [max(A, B), 20], d)
        plataformas.add(p)
        sprites.add(p)

    # ---- Crear enemigos a partir de los 7 000 puntos
    if j.puntaje >= 7000:
        while len(enemigos) < 1:
            pos_e = (r.randint(50, 550 - 60 - 50), r.randint(-300, -100))
            e = Enemigo(pos_e)
            ind = Indicador(pos_e)
            sprites.add(e)
            sprites.add(ind)
            enemigos.add(e)
            indicador_enemigos.add(ind)

    # ---- Crear muros sobre los existentes
    while len(muros) < 10:
        M1 = Muro((-20, -200))
        M2 = Muro((500, -200))
        sprites.add(M1)
        sprites.add(M2)
        muros.add(M1)
        muros.add(M2)

    # ---- Verificar choques
    # Chocar con las plataformas solo cuando cae
    choque = pg.sprite.spritecollide(j, plataformas, False)
    if choque and j.vel.y > 0:
        j.pos.y = choque[0].rect.top
        j.vel.y = 0

    # Chocar con los muros
    if j.pos.x - 2 * j.size < 50:
        j.pos.x = 50 + 2 * j.size
        j.vel.x = 0

    if j.pos.x + 2 * j.size > 500:
        j.pos.x = 500 - 2 * j.size
        j.vel.x = 0

    # ---- Fin del juego
    # Chocar con los enemigos
    choque = pg.sprite.spritecollide(j, enemigos, False)
    if choque:
        reiniciar = True

    # Caer fuera de pantalla
    if j.rect.top > 600:
        for sprite in sprites:
            sprite.rect.y -= j.vel.y * 2
        if j.rect.top > 900:
            reiniciar = True

    # ---- Mostrar en pantalla
    pg.display.flip()

pg.quit()
