import random

def barrer_texte(texte):
    return ''.join([char + '\u0336' for char in texte])

def generer_captcha_data():
    code_secret = str(random.randint(1000, 9999))
    code_barre = barrer_texte(code_secret)
    return code_secret, code_barre

if __name__ == "__main__":
    while True:
        secret, barre = generer_captcha_data()
        user_input = input(f"Tapez les 4 chiffres : {barre}\n>>> ")
        if user_input == secret:
            print("Ok !")
            break
        else:
            print("Non.")
