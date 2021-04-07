from OSINT.GetInsta import main

if __name__ == "__main__":
    
    # Sacha, la fonction loading c'est une fonction que tu vas implé dans ta GUI et tu vas ensuite la ranger
    # dans le fichier utils.py à la place de celle que j'ai mis qui pour l'isntant attend juste en ne faisant
    # rien d'autre.

    data = main(input("Username:"))

    # Exemple de comment tu accèderas aux données que je te renvoie
    
    for i in data['Stats']['TaggedUsers']:
        print(i)
