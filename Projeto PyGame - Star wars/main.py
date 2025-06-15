import pygame
import random
from recursos.funcoes import (
    inicializarBancoDeDados, escreverDados, lerRanking, obter_nickname_tk, tela_derrota
)

pygame.init()
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Star Wars - Millennium Falcon")
falcon_img = pygame.image.load("assets/millennium_falcon.png")
falcon_img = pygame.transform.scale(falcon_img, (60, 60))
scrap_img = pygame.image.load("assets/scrap.png")
scrap_img = pygame.transform.scale(scrap_img, (30, 30))
asteroid_img = pygame.image.load("assets/asteroid.png")
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))
bg_img = pygame.image.load("assets/space_bg.jpg")

class Falcon:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 80
        self.vel = 7
        self.rect = pygame.Rect(self.x, self.y, 60, 60)
    def move(self, keys):
        if keys[pygame.K_a] and self.x > 0:
            self.x -= self.vel
        if keys[pygame.K_d] and self.x < WIDTH - 60:
            self.x += self.vel
        self.rect.topleft = (self.x, self.y)
    def draw(self, win):
        win.blit(falcon_img, (self.x, self.y))

class Scrap:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 30)
        self.y = random.randint(-600, -40)
        self.vel = random.randint(3, 6)
        self.rect = pygame.Rect(self.x, self.y, 30, 30)
    def move(self):
        self.y += self.vel
        self.rect.topleft = (self.x, self.y)
        if self.y > HEIGHT:
            self.reset()
    def reset(self):
        self.x = random.randint(0, WIDTH - 30)
        self.y = random.randint(-600, -40)
        self.vel = random.randint(3, 6)
        self.rect.topleft = (self.x, self.y)
    def draw(self, win):
        win.blit(scrap_img, (self.x, self.y))

class BackgroundObject:
    def __init__(self):
        self.img = pygame.image.load("assets/xwing.png")
        self.img = pygame.transform.scale(self.img, (40, 20))
        self.x = -40  # Começa fora da tela à esquerda
        self.y = random.randint(50, HEIGHT - 100)
        self.vel = random.randint(2, 4)
        self.active = False

    def start(self):
        self.x = -40  # Reinicia fora da tela à esquerda
        self.y = random.randint(50, HEIGHT - 100)
        self.vel = random.randint(2, 4)
        self.active = True

    def move(self):
        if self.active:
            self.x += self.vel
            if self.x > WIDTH:
                self.active = False

    def draw(self, win):
        if self.active:
            win.blit(self.img, (self.x, self.y))

class Asteroid:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 50)
        self.y = random.randint(-800, -50)
        self.vel = random.randint(4, 8)
        self.rect = pygame.Rect(self.x, self.y, 50, 50)
    def move(self):
        self.y += self.vel
        self.rect.topleft = (self.x, self.y)
        if self.y > HEIGHT:
            self.reset()
    def reset(self):
        self.x = random.randint(0, WIDTH - 50)
        self.y = random.randint(-800, -50)
        self.vel = random.randint(4, 8)
        self.rect.topleft = (self.x, self.y)
    def draw(self, win):
        win.blit(asteroid_img, (self.x, self.y))

class BlinkingStar:
    def __init__(self):
        self.img = pygame.image.load("assets/star.png")
        self.img = pygame.transform.scale(self.img, (24, 24))
        self.visible = True
        self.last_toggle = pygame.time.get_ticks()
        self.interval = 500  # milissegundos

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_toggle > self.interval:
            self.visible = not self.visible
            self.last_toggle = now

    def draw(self, win):
        if self.visible:
            # Agora mais ao centro, por exemplo: 300px da esquerda, 20px do topo
            win.blit(self.img, (300, 20))
            
def mostrar_ranking_menu():
    font = pygame.font.SysFont("Arial", 32)
    small_font = pygame.font.SysFont("Arial", 26)
    ranking = lerRanking()
    waiting = True
    while waiting:
        win.blit(bg_img, (0, 0))
        title = font.render("TOP 5 RANKING", True, (0, 255, 255))
        win.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 120))
        if ranking:
            for i, (nome, (pontos, data)) in enumerate(ranking[:5]):
                rank_line = small_font.render(f"{i+1}. {nome} - {pontos} pts ({data})", True, (255,255,255))
                win.blit(rank_line, (WIDTH // 2 - rank_line.get_width() // 2, HEIGHT // 2 - 40 + i*35))
        else:
            no_score = small_font.render("Nenhum score registrado ainda.", True, (255,255,255))
            win.blit(no_score, (WIDTH // 2 - no_score.get_width() // 2, HEIGHT // 2))
        sair = small_font.render("Pressione ESC para voltar", True, (200,200,200))
        win.blit(sair, (WIDTH // 2 - sair.get_width() // 2, HEIGHT // 2 + 160))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False

def menu():
    font = pygame.font.SysFont("Arial", 50)
    small_font = pygame.font.SysFont("Arial", 30)
    selected = False
    mostrar_mensagem = False
    mensagem_timer = 0
    while not selected:
        win.blit(bg_img, (0, 0))
        title = font.render("Star Wars: Millennium Falcon", True, (255, 255, 0))
        win.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 140))
        jogar = small_font.render("Pressione ENTER para jogar", True, (255,255,255))
        ranking = small_font.render("Pressione R para ver o ranking", True, (255,255,255))
        win.blit(jogar, (WIDTH // 2 - jogar.get_width() // 2, HEIGHT // 2 + 20))
        win.blit(ranking, (WIDTH // 2 - ranking.get_width() // 2, HEIGHT // 2 + 70))
        if mostrar_mensagem:
            mensagem = small_font.render("Prepare-se para a aventura!", True, (0, 255, 255))
            win.blit(mensagem, (WIDTH // 2 - mensagem.get_width() // 2, HEIGHT // 2 + 120))
            if pygame.time.get_ticks() - mensagem_timer > 2000:
                selected = True
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if not mostrar_mensagem:
                    if event.key == pygame.K_r:
                        mostrar_ranking_menu()
                    if event.key == pygame.K_RETURN:
                        mostrar_mensagem = True
                        mensagem_timer = pygame.time.get_ticks()
    nickname = obter_nickname_tk()
    return nickname

def main():
    inicializarBancoDeDados()
    nickname = menu()
    pygame.mixer.music.load("assets/game_music.mp3")
    pygame.mixer.music.play(-1)
    run = True
    paused = False
    clock = pygame.time.Clock()
    falcon = Falcon()
    scraps = [Scrap() for _ in range(5)]
    asteroids = [Asteroid() for _ in range(4)]
    bg_object = BackgroundObject()
    star = BlinkingStar()  # <-- instancie a estrela aqui
    bg_timer = 0
    bg_interval = random.randint(4000, 8000)
    score = 0
    font = pygame.font.SysFont("Arial", 30)
    while run:
        clock.tick(60)
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                paused = not paused
        if paused:
            pause_font = pygame.font.SysFont("Arial", 60)
            pause_text = pause_font.render("PAUSADO", True, (255, 255, 0))
            win.blit(bg_img, (0, 0))
            star.update()
            star.draw(win)
            win.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 100))
            ranking = lerRanking()
            rank_font = pygame.font.SysFont("Arial", 32)
            rank_title = rank_font.render("TOP 5 RANKING", True, (0, 255, 255))
            win.blit(rank_title, (WIDTH // 2 - rank_title.get_width() // 2, HEIGHT // 2))
            for i, (nome, (pontos, data)) in enumerate(ranking[:5]):
                rank_line = font.render(f"{i+1}. {nome} - {pontos} pts ({data})", True, (255,255,255))
                win.blit(rank_line, (WIDTH // 2 - rank_line.get_width() // 2, HEIGHT // 2 + 40 + i*35))
            pygame.display.update()
            continue
        if not bg_object.active and now - bg_timer > bg_interval:
            bg_object.start()
            bg_timer = now
            bg_interval = random.randint(4000, 8000)
        bg_object.move()
        keys = pygame.key.get_pressed()
        falcon.move(keys)
        for scrap in scraps:
            scrap.move()
            if falcon.rect.colliderect(scrap.rect):
                score += 10
                scrap.reset()
        for asteroid in asteroids:
            asteroid.move()
            if falcon.rect.colliderect(asteroid.rect):
                run = False
        win.blit(bg_img, (0, 0))
        bg_object.draw(win)
        star.update()
        star.draw(win)
        falcon.draw(win)
        for scrap in scraps:
            scrap.draw(win)
        for asteroid in asteroids:
            asteroid.draw(win)
        score_text = font.render(f"Score: {score}", True, (255,255,0))
        win.blit(score_text, (10, 10))
        pause_hint = font.render("Aperte ESPAÇO para pausar", True, (200, 200, 200))
        win.blit(pause_hint, (WIDTH - pause_hint.get_width() - 20, HEIGHT - 40))
        pygame.display.update()
    pygame.mixer.music.stop()
    escreverDados(nickname, score)
    jogar_novamente = tela_derrota(win, bg_img, WIDTH, HEIGHT, score)
    if jogar_novamente:
        main()
    else:
        pygame.quit()

if __name__ == "__main__":
    main()