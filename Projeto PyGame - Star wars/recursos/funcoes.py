import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

def inicializarBancoDeDados():
    try:
        with open("base.atitus", "r") as banco:
            pass
    except:
        with open("base.atitus", "w") as banco:
            banco.write("{}")

def escreverDados(nome, pontos):
    try:
        with open("base.atitus", "r") as banco:
            dados = banco.read()
            dadosDict = json.loads(dados) if dados else {}
    except:
        dadosDict = {}
    data_br = datetime.now().strftime("%d/%m/%Y")
    if nome in dadosDict:
        antigo_score = dadosDict[nome][0]
        if pontos > antigo_score:
            dadosDict[nome] = (pontos, data_br)
    else:
        dadosDict[nome] = (pontos, data_br)
    melhores = sorted(dadosDict.items(), key=lambda x: x[1][0], reverse=True)[:5]
    dadosDict = {nome: valor for nome, valor in melhores}
    with open("base.atitus", "w") as banco:
        banco.write(json.dumps(dadosDict))

def lerRanking():
    try:
        with open("base.atitus", "r") as banco:
            dados = banco.read()
            if dados:
                dadosDict = json.loads(dados)
                ranking = sorted(dadosDict.items(), key=lambda x: x[1][0], reverse=True)
                return ranking
            else:
                return []
    except:
        return []

def obter_nickname_tk():
    largura_janela = 300
    altura_janela = 50
    nome = ""
    def obter_nome():
        nonlocal nome
        nome = entry_nome.get()
        if not nome:
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")
        else:
            root.destroy()
    root = tk.Tk()
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.title("Informe seu nickname")
    root.protocol("WM_DELETE_WINDOW", obter_nome)
    entry_nome = tk.Entry(root)
    entry_nome.pack()
    botao = tk.Button(root, text="Enviar", command=obter_nome)
    botao.pack()
    root.mainloop()
    return nome

def tela_derrota(win, bg_img, WIDTH, HEIGHT, score):
    import pygame
    font = pygame.font.SysFont("Arial", 50)
    small_font = pygame.font.SysFont("Arial", 30)
    selected = False
    opcao = 0
    while not selected:
        win.blit(bg_img, (0, 0))
        derrota = font.render("DERROTA!", True, (255, 0, 0))
        score_text = small_font.render(f"Seu score: {score}", True, (255,255,0))
        jogar_color = (255,255,255) if opcao == 0 else (180,180,180)
        sair_color = (255,255,255) if opcao == 1 else (180,180,180)
        jogar = small_font.render("Jogar Novamente (ENTER)", True, jogar_color)
        sair = small_font.render("Sair (ESC)", True, sair_color)
        win.blit(derrota, (WIDTH // 2 - derrota.get_width() // 2, HEIGHT // 2 - 100))
        win.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 30))
        win.blit(jogar, (WIDTH // 2 - jogar.get_width() // 2, HEIGHT // 2 + 40))
        win.blit(sair, (WIDTH // 2 - sair.get_width() // 2, HEIGHT // 2 + 90))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    opcao = 1 - opcao
                if event.key == pygame.K_RETURN and opcao == 0:
                    return True
                if event.key == pygame.K_ESCAPE or (event.key == pygame.K_RETURN and opcao == 1):
                    return False