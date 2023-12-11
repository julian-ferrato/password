import hashlib
import json
import random
import string

def verifier_mot_de_passe(mot_de_passe):
    longueur_min = 8
    majuscule = False
    minuscule = False
    chiffre = False
    special = False

    for caractere in mot_de_passe:
        if caractere.isupper():
            majuscule = True
        elif caractere.islower():
            minuscule = True
        elif caractere.isdigit():
            chiffre = True
        elif caractere in string.punctuation:
            special = True
    
    return (
        len(mot_de_passe) >= longueur_min and
        majuscule and
        minuscule and
        chiffre and
        special
    )

def hasher_mot_de_passe(mot_de_passe):
    mot_de_passe_bytes = mot_de_passe.encode('utf-8')
    hachage = hashlib.sha256()
    hachage.update(mot_de_passe_bytes)
    mot_de_passe_hash = hachage.hexdigest()
    return mot_de_passe_hash

def enregistrer_mots_de_passe(mots_de_passe):
    with open('mots_de_passe.json', 'w') as fichier:
        json.dump(mots_de_passe, fichier)

def generer_mot_de_passe_aleatoire():
    longueur = random.randint(8, 12)
    caracteres = string.ascii_letters + string.digits + string.punctuation
    mot_de_passe = ''.join(random.choice(caracteres) for _ in range(longueur))
    return mot_de_passe

def ajouter_mot_de_passe():
    mots_de_passe = {}
    try:
        with open('mots_de_passe.json', 'r') as fichier:
            mots_de_passe = json.load(fichier)
    except FileNotFoundError:
        pass
    
    while True:
        choix = input("Souhaitez-vous choisir votre mot de passe ? (oui/non) : ").lower()
        
        if choix == 'oui':
            mot_de_passe = input("Entrez votre mot de passe : ")
            if not verifier_mot_de_passe(mot_de_passe):
                print("Le mot de passe ne respecte pas les critères de sécurité.")
                continue
            mot_de_passe_hash = hasher_mot_de_passe(mot_de_passe)
        elif choix == 'non':
            mot_de_passe = generer_mot_de_passe_aleatoire()
            mot_de_passe_hash = hasher_mot_de_passe(mot_de_passe)
        else:
            print("Choix non valide. Veuillez répondre par 'oui' ou 'non'.")
            continue
        
        if mot_de_passe_hash not in mots_de_passe.values():
            nom_utilisateur = input("Entrez le nom d'utilisateur : ")
            mots_de_passe[nom_utilisateur] = mot_de_passe_hash
            enregistrer_mots_de_passe(mots_de_passe)
            print("Mot de passe ajouté avec succès.")
            break
        else:
            print("Ce mot de passe est déjà utilisé. Veuillez en choisir un autre.")

def afficher_mots_de_passe():
    try:
        with open('mots_de_passe.json', 'r') as fichier:
            mots_de_passe = json.load(fichier)
            print("Mots de passe enregistrés :")
            for nom_utilisateur, mot_de_passe_hash in mots_de_passe.items():
                print(f"Nom d'utilisateur: {nom_utilisateur}, Mot de passe haché: {mot_de_passe_hash}")
    except FileNotFoundError:
        print("Aucun mot de passe enregistré.")

def supprimer_mot_de_passe():
    try:
        with open('mots_de_passe.json', 'r') as fichier:
            mots_de_passe = json.load(fichier)
    except FileNotFoundError:
        print("Aucun mot de passe enregistré.")
        return

    nom_utilisateur = input("Entrez le nom d'utilisateur à supprimer : ")
    if nom_utilisateur in mots_de_passe:
        del mots_de_passe[nom_utilisateur]
        enregistrer_mots_de_passe(mots_de_passe)
        print(f"Le mot de passe pour '{nom_utilisateur}' a été supprimé avec succès.")
    else:
        print("Ce nom d'utilisateur n'existe pas.")

def gestionnaire_mots_de_passe():
    while True:
        choix = input("Que souhaitez-vous faire ? (ajouter/afficher/supprimer/quitter) : ").lower()
        
        if choix == 'ajouter':
            ajouter_mot_de_passe()
        elif choix == 'afficher':
            afficher_mots_de_passe()
        elif choix == 'supprimer':
            supprimer_mot_de_passe()
        elif choix == 'quitter':
            break
        else:
            print("Choix non valide. Veuillez choisir parmi les options disponibles.")


def main():
    print("Bienvenue dans le gestionnaire de mots de passe !")
    gestionnaire_mots_de_passe()

if __name__ == "__main__":
    main()