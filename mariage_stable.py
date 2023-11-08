import random

def generer_preferences(keys, values):
    preferences = {}
    for i in range(keys):
        preferences[i] = random.sample(range(values), values)
    return preferences

# Gale-Shapley
def mariage_stable(etudiants_pref, etablissements_pref):

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

#couplage = mariage_stable(etudiants_pref, etablissements_pref)
couplage = mariage_stable({0: [2, 1, 4, 5, 3, 0], 1: [3, 4, 2, 1, 5, 0], 2: [3, 1, 0, 5, 2, 4], 3: [0, 1, 3, 5, 2, 4]},
                           {0: [0, 2, 1, 3], 1: [2, 1, 0, 3], 2: [3, 0, 1, 2], 3: [3, 1, 2, 0], 4: [1, 0, 3, 2], 5: [1, 2, 0, 3]})

print("Mariage stable final:", couplage)
