import time
import random
import os

def barrer_texte(texte):
    """Ajoute un trait de rature sur chaque chiffre pour faire l'effet captchas."""
    return ''.join([char + '\u0336' for char in texte])

def effacer_ecran():
    os.system('cls' if os.name == 'nt' else 'clear')

def captcha_terminal():
    est_valide = False

    while not est_valide:
        effacer_ecran()
        
        # 1. Attente du déclenchement
        print("Scratch CAPTCHA")
        input("\nAppuyez sur [ENTRÉE] pour démarrer...")

        # 2. Le truc qui tourne (Spinner)
        effacer_ecran()
        symboles_tournants = ["|", "/", "-", "\\"]
        for _ in range(3):  # 3 tours de spinner
            for sym in symboles_tournants:
                effacer_ecran()
                print(f"Chargement {sym}")
                time.sleep(0.1)

        # 3. Génération des chiffres barrés
        code_secret = str(random.randint(1000, 9999))
        code_barre = barrer_texte(code_secret)

        effacer_ecran()
        print(f"Code : {code_barre}\n")

        # 4. Saisie (uniquement des chiffres)
        saisie = ""
        while not saisie.isdigit() or len(saisie) != 4:
            saisie = input("Entrez les 4 chiffres : ").strip()
            if not saisie.isdigit() or len(saisie) != 4:
                print("❌ Entrez 4 chiffres uniquement !\n")

        # 5. Résultat
        effacer_ecran()
        if saisie == code_secret:
            est_valide = True
            print("✔ Validé !")
        else:
            print("❌ Échec, réessayez...")
            time.sleep(1.2)

if __name__ == "__main__":
    captcha_terminal()
