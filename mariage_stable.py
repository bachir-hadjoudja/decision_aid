import random

def generer_preferences(keys, values):
    preferences = {}
    for i in range(keys):
        preferences[i] = random.sample(range(values), values)
    return preferences

# Gale-Shapley
def gale_shapley(etudiants_pref, etablissements_pref):

    etudiants_libres = list(etudiants_pref.keys())
    print(etudiants_libres)
    couplage = {}

    while etudiants_libres:
        etudiant = etudiants_libres.pop(0)
        preferences_etudiant = etudiants_pref[etudiant]

        for etablissement in preferences_etudiant:

            if etablissement not in couplage:
                couplage[etablissement] = etudiant
                break
            else:
                etudiant_couple = couplage[etablissement]
                # L'établissement compare les préférences
                if etablissements_pref[etablissement].index(etudiant) < \
                        etablissements_pref[etablissement].index(etudiant_couple):
                    # L'établissement préfère le nouvel étudiant
                    couplage[etablissement] = etudiant
                    if etudiant_couple not in etudiants_libres:
                        etudiants_libres.append(etudiant_couple)
                    break

    return couplage

nb_etudiants = 4
nb_etablissements = 6
etudiants_pref = generer_preferences(nb_etudiants, nb_etablissements)
etablissements_pref = generer_preferences(nb_etablissements, nb_etudiants)

print("Pref des étudiants:", etudiants_pref)
print("Pref des établissements:", etablissements_pref)


couplage = gale_shapley(etudiants_pref, etablissements_pref)
print("Mariage stable final:", couplage)


#######TODO : choix de metrique :
####TODO satisfaction pondérée: chaque choix d'un étudiant a un poids, par ex le premier : 1 le deuxième : 0.75 le troisième : 0.5 ... et selon le choix attribué, on multiplie
# fois le poids associé, et on divise sur la somme des poids totaux (genre 1+1+1+1+1+1..)
####TODO calcul de la distance : la distance entre le choix obtenu et le meilleur choix (premier choix)
####TODO Variance de la satisfaction : Calculer la variance ou l'écart-type des scores de satisfaction pour évaluer l'équité du couplage. 
# Une faible variance indiquerait une distribution plus équitable de la satisfaction.
####TODO Approche utilitariste vs égalitariste : L’approche utilitariste maximiserait la satisfaction totale, tandis que l’approche égalitariste chercherait à égaliser la satisfaction autant que possible. 
#Vous pouvez implémenter les deux et comparer les résultats.

