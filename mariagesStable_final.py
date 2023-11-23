import json
import copy
from turtle import distance
import sys
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

#function to read and return data from a json file
def retrieve_data(filename):
    with open(filename, "r") as json_file:
        data = json.load(json_file)
    return data

def gale_shapley(proposers, students):
    proposer_engagements = {}
    student_engagements = {}
    student_queue = list(students.keys())  # Utilisez la liste des étudiants comme file initiale

    while student_queue:
        student = student_queue.pop(0)
        #print("student", student)
        student_preferences = students[student]
        #print("student_prefe", student_preferences)

        if student_preferences:
            proposer = student_preferences.pop(0)

            if proposer not in proposer_engagements:
                proposer_engagements[proposer] = student
                student_engagements[student] = proposer
            else:
                current_partner = proposer_engagements[proposer]
                current_partner_preferences = proposers[proposer]

                if current_partner_preferences.index(student) < current_partner_preferences.index(current_partner):
                    proposer_engagements[proposer] = student
                    student_engagements[student] = proposer
                    student_queue.append(current_partner)
                else:
                    student_queue.append(student)
        else:
            print("student_preferences is empty for student", student)

    return proposer_engagements, student_engagements





def is_stable_match(proposer_preferences, student_preferences, matching):
    proposer_match = matching[0]
    student_match = matching[1]
    # Create a dictionary to store the current engagements
    current_engagements = {}
    #print(proposer_preferences , student_preferences)
    # Populate the current engagements based on the matching
    for proposer, student in proposer_match.items():
        current_engagements[proposer] = student
    nb_blocking_matches = 0
    # Iterate through each proposeur
    for proposer, preferences in proposer_preferences.items():
        #print("#####testing for : "+ proposer)
        for student in preferences:
            #print("##testing for : "+ student)
            #condition d'arret: aucun des students itérés percedemment ne prefere l'offre courrante
            if student == current_engagements.get(proposer):
                break  # The current engagement is already stable
            #si etudiant courrant prefere cette offre a l'offre qu'il a eu:
            if student_preferences[student].index(proposer) < student_preferences[student].index(list(current_engagements.keys())[list(current_engagements.values()).index(student)]):
                #si l'offre prefere cet atudiant mais a eu un autre:
                if proposer_preferences[proposer].index(student) < proposer_preferences[proposer].index(current_engagements.get(proposer)):
                    print("matching pas stable")
                    print(str(student) + "  prefere  " + str(proposer) + "  mais a eu  " + str(list(current_engagements.keys())[list(current_engagements.values()).index(student)]))
                    nb_blocking_matches = nb_blocking_matches + 1   # A pair prefers each other over their current partners

    if nb_blocking_matches == 0:
        # If no instability is found, the matching is stable
        print("The Match is Stable:))))")
        return True
    else:
        print("number of blocking matches si:: ", nb_blocking_matches)
        return False


#La moyenne des positions des étudiants et des établissements
def analyse_moyenne(stable_matches, proposers_preferences, students_preferences):
    proposer_match = stable_matches[0]
    print("proposer_match", proposer_match)
    print("len(proposer_match)", len(proposer_match))
    student_match = stable_matches[1]
    nb_participants = len(proposer_match) + len(student_match)

    distance_student = 0
    distance_etablissement = 0
    moyennes_students = []  # Liste pour stocker les moyennes à chaque itération
    moyennes_etablissements = []

    students = list(student_match.keys())  # Obtenez une liste des étudiants
    proposals = list(proposer_match.values())  # Liste des établissements

    for p, s in proposer_match.items():
        # get proposer and student priorities
        p_preferences = proposers_preferences[p]
        s_preferences = students_preferences[s]

        # calculate distances and store them
        assigned_student = p_preferences.index(s)
        assigned_proposal = s_preferences.index(p)
        distance_student += assigned_student
        distance_etablissement += assigned_proposal

    moyenne_students = distance_student / len(proposer_match) * 100
    moyenne_proposers = distance_etablissement / len(student_match) * 100

    return moyenne_proposers, moyenne_students

#Positionnement par rapport au pire des cas -- une autre approche
def analyse_ratio_satisfaction(stable_matches, proposers_preferences, students_preferences):
    proposer_match = stable_matches[0]
    student_match = stable_matches[1]

    # Calcul de la distance totale actuelle et du pire des cas pour les proposers
    proposer_distance_actuelle = sum(proposers_preferences[p].index(proposer_match[p]) for p in proposer_match)
    proposer_pire_distance = sum(len(proposers_preferences[p]) for p in proposer_match)

    # Calcul de la distance totale actuelle et du pire des cas pour les students
    student_distance_actuelle = sum(students_preferences[s].index(student_match[s]) for s in student_match)
    student_pire_distance = sum(len(students_preferences[s]) for s in student_match)
    # Calcul des ratios
    ratio_proposers = 1 - (proposer_distance_actuelle / proposer_pire_distance)
    ratio_students = 1 - (student_distance_actuelle / student_pire_distance)

    return ratio_proposers, ratio_students

#Ceux qui ont eu leur premier choix 
def analyse_utilitariste(stable_matches, proposers_preferences, students_preferences):
    proposer_match = stable_matches[0]
    student_match = stable_matches[1]
    proposer_first_choice = 0
    student_first_choice = 0
    for p,s in proposer_match.items(): 
        #get proposer prprecision_rangiorities
        p_preferences = proposers_preferences[p]
        #get student priorities
        s_preferences = students_preferences[s]
        if proposer_match[p] == p_preferences[0]:
            proposer_first_choice=proposer_first_choice+1
        if student_match[s] == s_preferences[0]:
            student_first_choice = student_first_choice +1
    #total = len(proposers_preferences) + len(students_preferences)
    ratio_students = student_first_choice / len(students_preferences)
    ratio_etablissements = proposer_first_choice / len(proposers_preferences)
    print("ratio premier_choix students / total students == " + str(ratio_students))
    print("ratio premier_choix etablissements / total etablissements == " + str(ratio_etablissements))


def analyse_pour_chaque_choix(stable_matches, proposers_preferences, students_preferences):
    proposer_match = stable_matches[0]
    student_match = stable_matches[1]
    max_preference = max(len(proposers_preferences[p]) for p in proposers_preferences)
    
    score_proposers = {i: 0 for i in range(1, max_preference + 1)}
    score_students = {i: 0 for i in range(1, max_preference + 1)}

    for p, s in proposer_match.items():
        p_preferences = proposers_preferences[p]
        s_preferences = students_preferences[s]

        p_choice_index = p_preferences.index(proposer_match[p]) + 1
        s_choice_index = s_preferences.index(student_match[s]) + 1

        score_proposers[p_choice_index] += 1
        score_students[s_choice_index] += 1

    return score_proposers, score_students



def analyse_egalitariste_variance(stable_matches, proposers_preferences, students_preferences):
    distances_proposers = []
    distances_students = []

    proposer_match = stable_matches[0]
    student_match = stable_matches[1]

    # Calcul des distances pour proposers et students
    for p, s in proposer_match.items():
        p_preferences = proposers_preferences[p]
        s_preferences = students_preferences[s]

        proposer_distance = p_preferences.index(s) + 1
        student_distance = s_preferences.index(p) + 1

        distances_proposers.append(proposer_distance)
        distances_students.append(student_distance)

    # Calcul des moyennes pour chaque groupe
    moyenne_proposers = sum(distances_proposers) / len(distances_proposers)
    moyenne_students = sum(distances_students) / len(distances_students)

    # Calcul des variances pour chaque groupe
    variance_proposers = sum(pow((distance - moyenne_proposers), 2) for distance in distances_proposers) / len(distances_proposers)
    variance_students = sum(pow((distance - moyenne_students), 2) for distance in distances_students) / len(distances_students)

    return variance_proposers, variance_students

def gaussienne(x, moyenne, variance):
    return (1 / np.sqrt(2 * np.pi * variance)) * np.exp(- (x - moyenne) ** 2 / (2 * variance))


def calculer_poids(rang, nombre_total):
    # Exemple : poids décroissant linéairement
    return 1 - (rang - 1) / nombre_total

def analyse_ponderee(stable_matches, proposers_preferences, students_preferences):
    score_total = 0

    proposer_match = stable_matches[0]
    student_match = stable_matches[1]

    for p, s in proposer_match.items():
        p_preferences = proposers_preferences[p]
        s_preferences = students_preferences[s]

        rang_proposer = p_preferences.index(s)
        rang_student = s_preferences.index(p)

        poids_proposer = calculer_poids(rang_proposer + 1, len(p_preferences))
        poids_student = calculer_poids(rang_student + 1, len(s_preferences))

        score_total += poids_proposer + poids_student

    return score_total






if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <num_proposers> <num_students>")
    num_proposers = int(sys.argv[1])
    num_students = int(sys.argv[2])
    filename = f"test_data_{num_proposers}_{num_students}.json"
    # Read data from the JSON file
    data = retrieve_data(filename)
    proposers = data["Proposers' Preferences"]
    students = data["Students' Preferences"]

    #keeping an intact copy of the data, cuz for some reason gale_shapley() alters the original x(
    proposersX=copy.deepcopy(proposers)
    studentsX = copy.deepcopy(students)
    print("\n "+ str(proposers))
    print("\n "+str(students))

    stable_matches = gale_shapley(proposers, students)




    isStable = is_stable_match(proposersX, studentsX, stable_matches)
    print("\n::stable_matches :: ")
    print(stable_matches)


    # Utilisez cette fonction avec vos données
    score_proposers, score_students = analyse_pour_chaque_choix(stable_matches, proposersX, studentsX)

    # Générer une palette de couleurs
    colors_proposers = list(mcolors.TABLEAU_COLORS.values())
    colors_students = list(mcolors.CSS4_COLORS.values())

    # Assurez-vous d'avoir assez de couleurs
    if len(colors_proposers) < len(score_proposers):
        colors_proposers += list(mcolors.CSS4_COLORS.values())[:len(score_proposers) - len(colors_proposers)]
    if len(colors_students) < len(score_students):
        colors_students += list(mcolors.TABLEAU_COLORS.values())[:len(score_students) - len(colors_students)]

    # Création des histogrammes
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    axes[0].bar(score_proposers.keys(), score_proposers.values(), color=colors_proposers)
    axes[0].set_title('Établissements')
    axes[0].set_xlabel('Choix')
    axes[0].set_ylabel('Nombre de Correspondances')

    axes[1].bar(score_students.keys(), score_students.values(), color=colors_students)
    axes[1].set_title('Étudiants')
    axes[1].set_xlabel('Choix')

    plt.tight_layout()
    plt.show()


    # Exemple d'utilisation
    ratio_proposers, ratio_students = analyse_ratio_satisfaction(stable_matches, proposersX, studentsX)
    print("Ratio de satisfaction pour les proposers :", ratio_proposers)
    print("Ratio de satisfaction pour les étudiants :", ratio_students)


    moyenne_students, moyenne_proposers = analyse_moyenne(stable_matches, proposersX, studentsX)
    #analyse_ratio_satisfaction(stable_matches, proposersX, studentsX, moyenne)
    analyse_utilitariste(stable_matches, proposersX, studentsX)
    
    
    # Exemple d'utilisation
    variance_proposers, variance_students = analyse_egalitariste_variance(stable_matches, proposersX, studentsX)
    print("Variance pour les proposers :", variance_proposers)
    print("Variance pour les étudiants :", variance_students)



    # Calcul des variances et des moyennes (Utilisez votre fonction ici)
    variance_proposers, variance_students = analyse_egalitariste_variance(stable_matches, proposersX, studentsX)

    # Plage de x autour des moyennes
    x = np.linspace(0, max(moyenne_proposers, moyenne_students) + 3, 100)

    # Calcul des y pour les gaussiennes
    y_proposers = gaussienne(x, moyenne_proposers, variance_proposers)
    y_students = gaussienne(x, moyenne_students, variance_students)

    # Tracer les courbes
    plt.plot(x, y_proposers, label='Proposers')
    plt.plot(x, y_students, label='Students')
    plt.title('Distribution de Satisfaction (Gaussienne)')
    plt.xlabel('Rang des Choix')
    plt.ylabel('Densité de Probabilité')
    plt.legend()
    plt.show()

    # Exemple d'utilisation
    score_pondere = analyse_ponderee(stable_matches, proposersX, studentsX)
    print("Score pondéré total :", score_pondere)