# import os
# import cmd
import random
import time
import sys
import keyboard

# Classe pour les armes
class Arme:
    def __init__(self, nom, degats):
        self.nom = nom
        self.degats = degats

# Classe pour le bouclier
class Bouclier:
    def __init__(self, nom):
        self.nom = nom
        self.reduction_degats = 0.75  # Réduit les dégâts de 75%

# Classe Joueur
class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.pv = 100
        self.attaque = 10
        self.defense = 5
        self.xp = 0
        self.niveau = 1
        self.inventaire = [Arme("Couteau", 10)] # Arme de base
        self.bouclier = None  # Le joueur peut avoir un bouclier

    # gestion des niveaux (XP)
    def monter_niveau(self):
        self.niveau += 1
        self.pv += 20
        self.attaque += 5
        self.defense += 3
        print(f"{self.nom} a monté de niveau! Niveau: {self.niveau}, PV: {self.pv}, Attaque: {self.attaque}, Défense: {self.defense}")
    # Sauvegarde des données du joueur dans un fichier texte
    def sauvegarder(self):
        with open(f"{self.nom}_sauvegarde.txt", "w") as fichier:
            fichier.write(f"{self.nom}\n")
            fichier.write(f"{self.pv}\n")
            fichier.write(f"{self.attaque}\n")
            fichier.write(f"{self.defense}\n")
            fichier.write(f"{self.xp}\n")
            fichier.write(f"{self.niveau}\n")
            for arme in self.inventaire:
                fichier.write(f"{arme.nom},{arme.degats}\n")
            if self.bouclier:
                fichier.write(f"{self.bouclier.nom}\n")
            else:
                fichier.write("Aucun\n")
        print("Sauvegarde réussie.")
    # Chargement des données du joueur depuis un fichier texte pour reprendre la partie
    def charger(self, nom):
        try:
            with open(f"{nom}_sauvegarde.txt", "r") as fichier:
                self.nom = fichier.readline().strip()
                self.pv = int(fichier.readline().strip())
                self.attaque = int(fichier.readline().strip())
                self.defense = int(fichier.readline().strip())
                self.xp = int(fichier.readline().strip())
                self.niveau = int(fichier.readline().strip())
                self.inventaire = []
                for ligne in fichier:
                    if ',' in ligne:
                        nom_arme, degats = ligne.strip().split(',')
                        self.inventaire.append(Arme(nom_arme, int(degats)))
                bouclier_nom = fichier.readline().strip()
                if bouclier_nom != "Aucun":
                    self.bouclier = Bouclier(bouclier_nom)
                else:
                    self.bouclier = None
            print("Chargement réussi.")
        except FileNotFoundError:
            print("Aucune sauvegarde trouvée.")

# Classe Monstre
class Monstre:
    def __init__(self, nom, niveau):
        self.nom = nom
        self.niveau = niveau
        self.pv = 50 + (niveau * 10)
        self.attaque = 5 + (niveau * 2)
        self.defense = 3 + niveau

        # Attribuer une arme en fonction du monstre
        if nom == "Gobelin":
            self.arme = Arme("Dague", 8)
        elif nom == "Orque":
            self.arme = Arme("Hache", 12)
        elif nom == "Troll":
            self.arme = Arme("Bâton", 10)
        elif nom == "Archer":
            self.arme = Arme("Arc et Flèches", 14)
        elif nom == "Dragon":
            self.arme = Arme("Feu", 20)
        elif nom == "Boss":
            self.arme = Arme("Coup de poing", 15) # Arme du boss

def menu_principal():
    print("1. Commencer une nouvelle partie")
    print("2. Charger une partie sauvegardée")
    print("3. Quitter")
    choix = input("Choisissez une option: ")
    return choix

# règles du jeu + contexte
def start_game():
    nom_joueur = input("Entrez votre nom: ")
    print("Bonjour ", nom_joueur)
    joueur = Joueur(nom_joueur)
    print("Bienvenue dans le monde de Narnia, vous venez de vous réveiller au beau milieu d'une forêt.")
    time.sleep(1)
    print("Pour gagner de l'XP, vous devrez récupérer de nouvelles armes et battre des monstre pour ainsi devenir plus fort.")
    time.sleep(1)
    print("Pour vous déplacer, utilisez les commandes : Est, Nord, Ouest, Sud.")
    time.sleep(1)
    print("Pour voir votre inventaire, appuyez sur 'i'.")
    time.sleep(1)
    print("Pour sauvegarder, appuyez sur '²'.")
    time.sleep(1)
    print("Bonne chance à vous!")
    time.sleep(5)
    boucle_jeu(joueur)

class Carte:
    def __init__(self):
        self.lieux = {
            (0, 0): "Vous êtes au milieu d'une forêt dense.",  # Position du joueur fixer au début du jeu
            (1, 0): "Vous voyez une clairière ensoleillée.",
            (0, 1): "Vous trouvez un ruisseau tranquille.",
            (-1, 0): "Vous arrivez à une grotte sombre.",
            (0, -1): "Vous êtes à l'orée de la forêt.",
            (2, 0): "Vous voyez un château imposant. Le boss est ici."  # Position du boss fixer sur la carte
        }
        self.position_boss = (2, 0)

    def description_lieu(self, position):
        return self.lieux.get(position, "Il n'y a rien de spécial ici.")

def monstre_aleatoire(niveau_joueur):
    liste_monstres = [
        ("Gobelin", 1),
        ("Orque", 2),
        ("Troll", 3),
        ("Archer", 4),
        ("Dragon", 5)
    ]

    monstres_disponibles = [monstre for monstre in liste_monstres if monstre[1] <= niveau_joueur]

    monstre_choisi = random.choice(monstres_disponibles)
    nom_monstre, niveau_monstre = monstre_choisi
    return Monstre(nom_monstre, niveau_monstre)

def boucle_jeu(joueur):
    carte = Carte()
    position = (0, 0)

    keyboard.on_press_key('i', lambda _: afficher_inventaire(joueur))

    while True:
        # Vérifie si la touche '²' est pressée pour sauvegarder
        if keyboard.is_pressed('²'):
            joueur.sauvegarder()
            time.sleep(1)  # Petite pause pour éviter de sauvegarder plusieurs fois d'affilée

        print(carte.description_lieu(position))
        commande = input("Entrez une commande (Est, Nord, Ouest, Sud): ").lower()

        if commande == 'est':
            position = (position[0] + 1, position[1])
        elif commande == 'nord':
            position = (position[0], position[1] + 1)
        elif commande == 'ouest':
            position = (position[0] - 1, position[1])
        elif commande == 'sud':
            position = (position[0], position[1] - 1)
        else:
            print("Commande invalide.")
            continue

        if position == carte.position_boss:
            boss = Monstre("Boss", 10)
            combat(joueur, boss)
            if joueur.pv > 0:
                print("Félicitations! Vous avez vaincu le boss et gagné le jeu!")
                print("Vous êtes à présent sortie de la forêt.")
                print("Merci d'avoir joué!")
            else:
                print("Vous avez été vaincu par le boss.")
                print("Game Over.")
                print("Recommencer le jeu pour essayer de vraincre le boss!")
            break

        rencontre = random.choice(["monstre", "objet", "arme", "rien"])
        if rencontre == "monstre":
            monstre = monstre_aleatoire(joueur.niveau)
            combat(joueur, monstre)
        elif rencontre == "objet":
            objet = random.choice([Arme("Potion", 0), Arme("Boost d'Attaque", 0), Arme("Boost de Défense", 0)])
            joueur.inventaire.append(objet)
            print(f"Vous avez trouvé un {objet.nom}!")
        elif rencontre == "arme":
            nouvelle_arme = random.choice([
                Arme("Épée", 15),
                Arme("Arc et Flèches", 12),
                Arme("Bâton de Mage", 18)
            ])
            joueur.inventaire.append(nouvelle_arme)
            print(f"Vous avez trouvé une {nouvelle_arme.nom}!")

def combat(joueur, monstre):
    print(f"Un {monstre.nom} (Niveau {monstre.niveau}) sauvage apparaît avec une {monstre.arme.nom}!")
    while joueur.pv > 0 and monstre.pv > 0:
        action = input("Choisissez une action (attaquer, utiliser objet, fuir): ").lower()

        if action == "attaquer":
            # Chance de manquer ou de faire un coup critique
            chance = random.randint(1, 100)
            if chance <= 10:  # 10% de chance de manquer
                print("Votre attaque a manqué!")
            else:
                coup_critique = chance <= 20  # 10% de chance de faire un coup critique
                degats = max(0, joueur.attaque + joueur.inventaire[0].degats - monstre.defense)
                if coup_critique:
                    degats *= 2  # Doubler les dégâts en cas de coup critique
                    print("Coup critique!")
                monstre.pv -= degats
                print(f"Vous avez infligé {degats} dégâts au {monstre.nom}.")
                if monstre.pv <= 0:
                    print(f"Vous avez vaincu le {monstre.nom}!")
                    joueur.xp += 10 * monstre.niveau
                    # Ajustement de l'XP requis pour le niveau suivant
                    xp_requis = joueur.niveau * 20
                    if joueur.xp >= xp_requis:
                        joueur.monter_niveau()
                    break

            # Attaque du monstre
            if monstre.pv > 0:  # Assurer que le monstre attaque seulement s'il est encore vivant
                # Variation de l'attaque du boss
                if isinstance(monstre, Monstre) and monstre.nom == "Boss":
                    if monstre.pv < (50 + (monstre.niveau * 10)) / 2:  # Si PV inférieur à 50%
                        monstre.attaque += 5  # Augmente l'attaque du boss
                        print("Le Boss devient plus fort!")

                degats = max(0, monstre.attaque + monstre.arme.degats - (joueur.defense * (1 - joueur.bouclier.reduction_degats) if joueur.bouclier else 1))
                joueur.pv -= degats
                print(f"Le {monstre.nom} vous a infligé {degats} dégâts.")
                if joueur.pv <= 0:
                    print("Vous avez été vaincu!")
                    break

        elif action == "utiliser objet":
            if not joueur.inventaire:
                print("Votre inventaire est vide.")
                continue
            print("Inventaire:", [item.nom for item in joueur.inventaire])
            objet_nom = input("Choisissez un objet à utiliser: ").title()
            objet = next((item for item in joueur.inventaire if item.nom == objet_nom), None)
            if objet:
                if objet.nom == "Potion":
                    joueur.pv += 20
                    print("Vous avez utilisé une Potion et regagné 20 PV.")
                elif objet.nom == "Boost d'Attaque":
                    joueur.attaque += 5
                    print("Vous avez utilisé un Boost d'Attaque. Votre attaque augmente de 5.")
                elif objet.nom == "Boost de Défense":
                    joueur.defense += 5
                    print("Vous avez utilisé un Boost de Défense. Votre défense augmente de 5.")
                joueur.inventaire.remove(objet)
            else:
                print("Objet invalide.")
        elif action == "fuir":
            print("Vous avez fui!")
            break
        else:
            print("Action invalide.")

def afficher_inventaire(joueur):
    print("Inventaire :")
    if not joueur.inventaire:
        print("L'inventaire est vide.")
    else:
        for item in joueur.inventaire:
            print(f"- {item.nom} (Dégâts: {item.degats if isinstance(item, Arme) else 'N/A'})")
        if joueur.bouclier:
            print(f"- {joueur.bouclier.nom} (Réduction des dégâts: {joueur.bouclier.reduction_degats * 100}%)")

if __name__ == "__main__":
    while True:
        choix = menu_principal()
        if choix == "1":
            start_game()
        elif choix == "2":
            nom_joueur = input("Entrez votre nom pour charger la sauvegarde: ")
            joueur = Joueur(nom_joueur)
            joueur.charger(nom_joueur)
            print(f"Chargement du joueur {joueur.nom} terminé.")
            boucle_jeu(joueur)
        elif choix == "3":
            sys.exit()
        else:
            print("Choix invalide.")
