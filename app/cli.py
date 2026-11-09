# app/cli.py
import os

def limpar_tela():
    """Limpa o terminal para atualizar a imagem do jogo sem poluir o ecrã."""
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_forca(erros):
    """Desenha o boneco da forca de acordo com o número de erros (0 a 6)."""
    estagios = [
        """
           --------
           |      |
           |      
           |    
           |      
           |     
          ---
        """,
        """
           --------
           |      |
           |      O
           |    
           |      
           |     
          ---
        """,
        """
           --------
           |      |
           |      O
           |      |
           |      
           |     
          ---
        """,
        """
           --------
           |      |
           |      O
           |     /|
           |      
           |     
          ---
        """,
        """
           --------
           |      |
           |      O
           |     /|\\
           |      
           |     
          ---
        """,
        """
           --------
           |      |
           |      O
           |     /|\\
           |     / 
           |     
          ---
        """,
        """
           --------
           |      |
           |      O
           |     /|\\
           |     / \\
           |     
          ---
        """
    ]
    # Garante que não ultrapassa o último desenho mesmo se tiver muitos erros
    indice = erros if erros < len(estagios) else -1
    print(estagios[indice])

def exibir_status(palavra_secreta, letras_adivinhadas, letras_erradas):
    """Junta tudo e exibe o estado atual da partida."""
    limpar_tela()
    exibir_forca(len(letras_erradas))
    
    # Monta a palavra com as letras descobertas e underscores (_)
    palavra_oculta = ""
    for letra in palavra_secreta:
        if letra.lower() in letras_adivinhadas:
            palavra_oculta += letra + " "
        else:
            palavra_oculta += "_ "
            
    print(f"Palavra: {palavra_oculta}\n")
    
    if letras_erradas:
        print(f"Letras erradas: {', '.join(letras_erradas)}")
    print("-" * 30)

def obter_chute():
    """Pede ao jogador para digitar uma letra e garante que é uma entrada válida."""
    while True:
        chute = input("\nDigite uma letra (ou 'sair' para encerrar): ").strip().lower()
        
        if chute == 'sair':
            return chute
            
        if len(chute) == 1 and chute.isalpha():
            return chute
        else:
            print("Entrada inválida! Por favor, digite apenas uma letra do alfabeto.")
