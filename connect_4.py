from pygame import display, draw, event, mouse, time, quit, QUIT, MOUSEBUTTONDOWN, gfxdraw
import random
import math

pire = -math.inf
meilleur = math.inf

line, col = 6,7
N = 1000
espace_entre_cercles = 10
couleur_joueur1, couleur_joueur2 = (255, 0, 0), (255, 255, 0)
minceure_bordure = 5


class Grille:
    def __init__(self, lignes=line, colonnes=col, taille_fenetre=N):
        self.lignes = lignes
        self.colonnes = colonnes
        self.taille_fenetre = taille_fenetre
        self.cell_size = taille_fenetre //  max(lignes, colonnes)
        self.radius = self.cell_size // 2 - (espace_entre_cercles // 2)
        self.grille = [[0 for _ in range(colonnes)] for _ in range(lignes)]
        display.init()
        self.fenetre = display.set_mode((taille_fenetre, taille_fenetre))
        display.set_caption("Puissance 4")


    def draw_circle(self, x, y, couleur, no_bordue = True):
        if no_bordue:
            gfxdraw.aacircle(self.fenetre, x, y, self.radius - minceure_bordure, couleur)
            gfxdraw.filled_circle(self.fenetre, x, y, self.radius - minceure_bordure, couleur)
        else:
            gfxdraw.aacircle(self.fenetre, x, y, self.radius, couleur)
            gfxdraw.filled_circle(self.fenetre, x, y, self.radius, couleur)


    def dessiner_grille(self, color=(255, 255, 255), background_color=(0, 0, 255), couleur_bordure = (0, 0, 0)):
        self.fenetre.fill(background_color)
        for i in range(self.lignes):
            for j in range(self.colonnes):
                x = j * self.cell_size + self.cell_size // 2
                y = i * self.cell_size + self.cell_size // 2
                self.draw_circle(x, y, couleur_bordure, False)    # Dessine les bordures du cercle
                if self.grille[i][j] == 1:
                    self.draw_circle(x, y, couleur_joueur1)   # Dessine les pions du joueur 1
                elif self.grille[i][j] == 2:
                    self.draw_circle(x, y, couleur_joueur2)   # Dessine les pions du joueur 2
                else:
                    self.draw_circle(x, y, color)     # Dessine les cercles
        display.flip()

    def col_is_full(self, col):
            for k in range(self.lignes):
                if self.grille[k][col] == 0:
                    return False
            if k == self.lignes - 1:
                return True


    def play(self, ia_included=True):
        if not ia_included:
            running = True
            joueur_actuel = 1
            while running:
                for ev in event.get():
                    if ev.type == QUIT:
                        running = False
                    elif ev.type == MOUSEBUTTONDOWN:
                        x, y = mouse.get_pos()
                        colonne = x // self.cell_size
                        #print(f"Clic détecté à la position ({x}, {y}) dans la colonne {colonne}")
                        if not self.col_is_full(colonne):  # Vérifier si la colonne n'est pas pleine
                            self.animer_pion(colonne, joueur_actuel)  # Animer la chute du pion
                            if self.poser_un_pion(colonne, joueur_actuel, False):
                                if self.verifier_alignement(joueur_actuel):
                                    print(f"Le joueur {joueur_actuel} a gagné")
                                    self.recommencer_jeu()
                                else:
                                    joueur_actuel = 3 - joueur_actuel
                        else:
                            print(f"Impossible de placer un pion dans la colonne {colonne}")
                
                self.dessiner_grille()
                time.delay(100)  # Ajoute un delai pour réduire l'utilisation du CPU
            quit()
        else:
            running = True
            joueur_actuel = 2
            
            while running:
                #print(self.donne_la_grille())
                
                for ev in event.get():
                    if ev.type == QUIT:
                        running = False
                    elif ev.type == MOUSEBUTTONDOWN:
                        x, y = mouse.get_pos()
                        colonne = x // self.cell_size
                        #print(f"Clic détecté à la position ({x}, {y}) dans la colonne {colonne}")
                        if joueur_actuel == 2:
                            if not self.col_is_full(colonne):
                                self.animer_pion(colonne, joueur_actuel)
                                if self.poser_un_pion(colonne, joueur_actuel):
                                    if self.verifier_alignement(joueur_actuel):
                                        print(f"Le joueur {joueur_actuel} a gagné")
                                        self.recommencer_jeu()
                                    joueur_actuel = 1

                if joueur_actuel == 1:
                    ia = IA_de_Précieux(2, self.donne_la_grille())
                    colonne = ia.trouver_le_bon_deplacement()
                    self.animer_pion(colonne, joueur_actuel)
                    if self.poser_un_pion(colonne, joueur_actuel):
                        if self.verifier_alignement(joueur_actuel):
                            print(f"Le joueur {joueur_actuel} a gagné")
                            self.recommencer_jeu()
                        joueur_actuel = 2

                self.dessiner_grille()
                time.delay(100)  # Ajoute un delai pour réduire l'utilisation du CPU
            quit()

                        


    def poser_un_pion(self, colonne, joueur):
        if colonne < 0 or colonne >= self.colonnes:
            return False  
        for i in range(self.lignes - 1, -1, -1):
            if self.grille[i][colonne] == 0:
                self.grille[i][colonne] = joueur
                return True
        return False
    
    def animer_pion(self, colonne, joueur):
        couleur_pion = couleur_joueur1 if joueur == 1 else couleur_joueur2
        for i in range(self.lignes):
            if self.grille[i][colonne] != 0:
                break
            self.dessiner_grille()
            x = colonne * self.cell_size + self.cell_size // 2
            y = i * self.cell_size + self.cell_size // 2
            self.draw_circle(x, y, couleur_pion)
            display.flip()
            time.delay(30)
        # Animation de rebond
        for _ in range(3):
            y -= 10
            self.dessiner_grille()
            self.draw_circle(x, y, couleur_pion)
            display.flip()
            time.delay(50)
            y += 10
            self.dessiner_grille()
            self.draw_circle(x, y, couleur_pion)
            display.flip()
            time.delay(50)
    
    def donne_la_grille(self):
        return self.grille
    
    def verifier_alignement(self, joueur):
        # Vérifier les alignements horizontaux
        for row in range(self.lignes):
            for col in range(self.colonnes - 3):
                if self.grille[row][col] == joueur and self.grille[row][col + 1] == joueur and self.grille[row][col + 2] == joueur and self.grille[row][col + 3] == joueur:
                    return True

        # Vérifier les alignements verticaux
        for col in range(self.colonnes):
            for row in range(self.lignes - 3):
                if self.grille[row][col] == joueur and self.grille[row + 1][col] == joueur and self.grille[row + 2][col] == joueur and self.grille[row + 3][col] == joueur:
                    return True

        # Vérifier les alignements diagonaux (de gauche à droite)
        for row in range(self.lignes - 3):
            for col in range(self.colonnes - 3):
                if self.grille[row][col] == joueur and self.grille[row + 1][col + 1] == joueur and self.grille[row + 2][col + 2] == joueur and self.grille[row + 3][col + 3] == joueur:
                    return True

        # Vérifier les alignements diagonaux (de droite à gauche)
        for row in range(self.lignes - 3):
            for col in range(3, self.colonnes):
                if self.grille[row][col] == joueur and self.grille[row + 1][col - 1] == joueur and self.grille[row + 2][col - 2] == joueur and self.grille[row + 3][col - 3] == joueur:
                    return True

        return False
    
    def recommencer_jeu(self):
        self.grille = [[0 for _ in range(self.colonnes)] for _ in range(self.lignes)]
        self.dessiner_grille()
        print("Le jeu a été recommencé")
    






class IA_de_Précieux:
    def __init__(self, ia_num, grill):
        self.grille = grill
        self.score_ia = pire
        self.score_adversaire = meilleur
        self.ia = ia_num
        self.joueur = 3 - ia_num

    def verifier_alignement(self, joueur, tab):
        # Vérifier les alignements horizontaux
        for row in range(line):
            for cl in range(col - 3):
                if tab[row][cl] == joueur and tab[row][cl + 1] == joueur and tab[row][cl + 2] == joueur and tab[row][cl + 3] == joueur:
                    return True

        # Vérifier les alignements verticaux
        for cl in range(col):
            for row in range(line - 3):
                if tab[row][cl] == joueur and tab[row + 1][cl] == joueur and tab[row + 2][cl] == joueur and tab[row + 3][cl] == joueur:
                    return True

        # Vérifier les alignements diagonaux (de gauche à droite)
        for row in range(line - 3):
            for cl in range(col - 3):
                if tab[row][cl] == joueur and tab[row + 1][cl + 1] == joueur and tab[row + 2][cl + 2] == joueur and tab[row + 3][cl + 3] == joueur:
                    return True

        # Vérifier les alignements diagonaux (de droite à gauche)
        for row in range(line - 3):
            for cl in range(3, col):
                if tab[row][cl] == joueur and tab[row + 1][cl - 1] == joueur and tab[row + 2][col - 2] == joueur and tab[row + 3][cl - 3] == joueur:
                    return True

        return False

    def enlever_pion(self, col, joueur):
            for i in range(line):
                if self.grille[i][col] == joueur:
                    self.grille[i][col] = 0
                    break

    def poser_un_pion(self, colonne, joueur):  
        for i in range(line - 1, -1, -1):
            if self.grille[i][colonne] == 0:
                self.grille[i][colonne] = joueur
                break

    def col_is_full(self, col):
            for k in range(line):
                if self.grille[k][col] == 0:
                    return False
            if k == line - 1:
                return True       

    def trouver_le_bon_deplacement(self, profondeur=6):
        meilleure_colonne = None
        meilleur_score = pire

        for colone in range(col):
            if not self.col_is_full(colone):
                self.poser_un_pion(colone, self.ia)
                score = self.minimax(profondeur - 1, False)
                self.enlever_pion(colone, self.ia)

                if score > meilleur_score:
                    meilleur_score = score
                    meilleure_colonne = colone

        if meilleure_colonne is not None:
            return meilleure_colonne
        else:
            print("ICI")
            list_of_columns = []
            for c in range(len(self.grille[0])):
                if not self.col_is_full(c):
                    list_of_columns.append(c)
            return random.choice(list_of_columns)

    def minimax(self, profondeur, maximiser, alpha=pire, beta=meilleur):
        if profondeur == 0: 
            return self.evaluer(self.grille)
        """elif self.verifier_alignement(self.ia, self.grille):
            return meilleur
        elif self.verifier_alignement(3 - self.ia, self.grille):
            return pire"""

        if maximiser:
            meilleur_score = pire
            for col in range(len(self.grille[0])):
                if not self.col_is_full(col):
                    self.poser_un_pion(col, self.ia)
                    score = self.minimax(profondeur - 1, False)
                    self.enlever_pion(col, self.ia)
                    meilleur_score = max(meilleur_score, score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
            return meilleur_score
        else:
            pire_score = meilleur
            for col in range(len(self.grille[0])):
                if not self.col_is_full(col):
                    self.poser_un_pion(col, 3 - self.ia)
                    score = self.minimax(profondeur - 1, True)
                    self.enlever_pion(col, 3 - self.ia)
                    pire_score = min(pire_score, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
            return pire_score

        

    def evaluer(self, grille):
        score = 0

        # Scores pour les alignements
        alignement_2 = 10
        alignement_3 = 100
        alignement_4 = 1000

        # Évaluer les alignements horizontaux
        for row in range(len(grille)):
            for col in range(len(grille[0]) - 3):
                alignement = [grille[row][col + i] for i in range(4)]
                score += self.evaluer_alignement(alignement)

        # Évaluer les alignements verticaux
        for col in range(len(grille[0])):
            for row in range(len(grille) - 3):
                alignement = [grille[row + i][col] for i in range(4)]
                score += self.evaluer_alignement(alignement)

        # Évaluer les alignements diagonaux (haut-gauche à bas-droit)
        for row in range(len(grille) - 3):
            for col in range(len(grille[0]) - 3):
                alignement = [grille[row + i][col + i] for i in range(4)]
                score += self.evaluer_alignement(alignement)

        # Évaluer les alignements diagonaux (bas-gauche à haut-droit)
        for row in range(3, len(grille)):
            for col in range(len(grille[0]) - 3):
                alignement = [grille[row - i][col + i] for i in range(4)]
                score += self.evaluer_alignement(alignement)

        # Évaluer la position centrale
        centre_col = len(grille[0]) // 2
        centre_count = sum([1 for row in range(len(grille)) if grille[row][centre_col] == self.ia])
        score += centre_count * 3

        return score

    def evaluer_alignement(self, alignement):
        score = 0
        if alignement.count(self.ia) == 4:
            score += 1000
        elif alignement.count(self.ia) == 3 and alignement.count(0) == 1:
            score += 100
        elif alignement.count(self.ia) == 2 and alignement.count(0) == 2:
            score += 10

        if alignement.count(self.joueur) == 3 and alignement.count(0) == 1:
            score -= 80
        elif alignement.count(self.joueur) == 2 and alignement.count(0) == 2:
            score -= 5

        return score

if __name__ == "__main__":
    grille_de_jeu = Grille()
    grille_de_jeu.play()