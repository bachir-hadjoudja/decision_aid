import json
import copy
from turtle import distance
import sys
import matplotlib.pyplot as plt

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
        print("student", student)
        student_preferences = students[student]
        print("student_prefe", student_preferences)

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
        print("#####testing for : "+ proposer)
        for student in preferences:
            print("##testing for : "+ student)
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


# import matplotlib.pyplot as plt

# def analyse_moyenne(stable_matches, proposers_preferences, students_preferences):
#     proposer_match = stable_matches[0]
#     student_match = stable_matches[1]
#     nb_participants = len(proposer_match) + len(student_match)
#     print("proposer_matches == ", proposer_match)
#     distance_count = 0
#     distance_student = 0
#     distance_etablissement = 0
#     moyennes = []
#     moyennes_students = []  # Liste pour stocker les moyennes à chaque itération
#     moyennes_etablissements=[]


#     students = list(student_match.keys())  # Obtenez une liste des étudiants
#     proposals = list(student_match.values())
#     for p, s in proposer_match.items():
#         # get proposer priorities
#         p_preferences = proposers_preferences[p]
#         # get student priorities
#         s_preferences = students_preferences[s]
#         # get proposer index in student priorities
#         assigned_student = p_preferences.index(s)
#         # get student index in proposer priorities
#         assigned_proposal = s_preferences.index(p)

#         distance_student = distance_student + assigned_student
#         distance_etablissement = distance_etablissement + assigned_proposal
#         # add found indices
#         distance_count = distance_count + assigned_proposal + assigned_student
        
#         moyenne_student = (distance_student / len(student_match))*100
#         moyenne_etablissement = (distance_etablissement / len(proposer_match))*100

#         # calculate moyenne and store it
#         moyenne = (distance_count / nb_participants)*100
#         moyennes.append(moyenne)
#         moyennes_students.append(moyenne_student)
#         moyennes_etablissements.append(moyenne_etablissement)
#     print("distance totale == " + str(distance_count))
#     print("moyenne == " + str(moyenne))

#     # Plotting the moyennes
#     plt.plot(students, moyennes, marker='o', linestyle='-')
#     #plt.plot(range(1, len(moyennes)+1), moyennes)
#     #plt.plot(students, moyennes_students, marker='o', linestyle='-')
#     #plt.plot(range(1, len(moyennes_etablissements)+1), moyennes_etablissements)
#     #plt.plot(proposals, moyennes_etablissements, marker='o', linestyle='-')
#     #plt.plot(range(1, len(moyennes_students)+1), moyennes_students)
#     plt.xlabel('Les etudiants/etablissements')
#     plt.ylabel('Moyenne des distances')
#     plt.title('Évolution de la moyenne des distances')
#     plt.show()

#     return moyenne


def analyse_moyenne(stable_matches, proposers_preferences, students_preferences):
    proposer_match = stable_matches[0]
    student_match = stable_matches[1]
    nb_participants = len(proposer_match) + len(student_match)
    print("proposer_matches == ", proposer_match)
    distance_count = 0
    distance_student = 0
    distance_etablissement = 0
    moyennes = []
    moyennes_students = []  # Liste pour stocker les moyennes à chaque itération
    moyennes_etablissements = []

    students = list(student_match.keys())  # Obtenez une liste des étudiants
    proposals = list(student_match.values())

    for p, s in proposer_match.items():
        # get proposer priorities
        p_preferences = proposers_preferences[p]
        # get student priorities
        s_preferences = students_preferences[s]
        # get proposer index in student priorities
        assigned_student = p_preferences.index(s)
        # get student index in proposer priorities
        assigned_proposal = s_preferences.index(p)

        distance_student += assigned_student
        distance_etablissement += assigned_proposal
        # add found indices
        distance_count += assigned_proposal + assigned_student
        
        # calculate moyenne and store it
        moyenne_student = (distance_student / len(proposer_match)) * 100
        moyenne_etablissement = (distance_etablissement / len(student_match)) * 100
        moyenne = (distance_count / nb_participants) * 100


        moyennes.append(moyenne)
        moyennes_students.append(moyenne_student)
        moyennes_etablissements.append(moyenne_etablissement)

    print("distance totale == " + str(distance_count))
    print("moyenne == " + str(moyenne))

    # Plotting the moyennes
    plt.plot(students, moyennes_students, label='Moyenne par étudiant', marker='o', linestyle='-')
    plt.plot(proposals, moyennes_etablissements, label='Moyenne par établissement', marker='o', linestyle='-')
    plt.plot(students, moyennes, label='Moyenne totale', marker='o', linestyle='-')

    plt.xlabel('Les étudiants/établissements')
    plt.ylabel('Moyenne des distances (%)')
    plt.title('Évolution de la moyenne des distances')
    plt.legend()
    plt.show()

    return moyenne


# Exemple d'utilisation
# Supposons que vous avez des données appropriées pour stable_matches, proposers_preferences, et students_preferences
# analyse_moyenne(stable_matches, proposers_preferences, students_preferences)

#Positionnement par rapport au pire des cas
def analyse_ratio_satisfaction(stable_matches, proposers_preferences, students_preferences, moyenne):
    proposer_match = stable_matches[0]
    student_match = stable_matches[1]
    print("proposer_matches == ",proposer_match)
    nb_participants = len(proposer_match)+len(student_match)
    distance_totale=0
    for p,s in proposer_match.items(): 
        #get proposer priorities
        p_preferences = proposers_preferences[p]
        distance_totale += len(p_preferences)
        #get student priorities
        s_preferences = students_preferences[s]
        distance_totale += len(s_preferences)
    #print("pire distance possible == " + str(distance_totale))
    ratio = (distance_totale - (moyenne*nb_participants)) / distance_totale # TODO : ?????
    print("ratio == "+ str(ratio))
    return ratio

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
    print("ratio premier_choix etablissements / total etablissements == " + str(ratio_etablissementss))


#TODO: define

def analyse_egalitariste(stable_matches, proposers_preferences, students_preferences):
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
    total = len(proposers_preferences) + len(students_preferences)
    ratio = (student_first_choice + proposer_first_choice) / total
    print("ratio premier_choix / total == " + str(ratio))



def analyse_ponderee(stable_matches, proposers_preferences, students_preferences):
    proposer_match = stable_matches[0]
    student_match = stable_matches[1]
    nb_participants = len(proposer_match)+len(student_match) 
    total_scores_ponderes = 0
    for p,s in proposer_match.items(): 
        #get proposer priorities
        p_preferences = proposers_preferences[p]
        #get student priorities
        s_preferences = students_preferences[s]
        #get proposer index in student priorities
        assigned_student = p_preferences.index(s)
        #gte student index in proposer  priorities
        assigned_proposal = s_preferences.index(p)
        p_score_pondere = 1 - (assigned_student/len(p_preferences))
        s_score_pondere = 1 - (assigned_proposal/len(s_preferences))
        #add found indeces
        total_scores_ponderes = total_scores_ponderes + s_score_pondere + p_score_pondere
    #print("pire distance possible == " + str(distance_totale))
    print("distance totale == " + str(total_scores_ponderes))
    moyenne =  total_scores_ponderes / nb_participants #moyenne des distances
    print("moyenne scores ponderes == "+ str(moyenne))
    return moyenne



def analyse_variance(stable_matches, proposers_preferences, students_preferences, moyenne):
    #retrieve priorityh of assigned match
    sigma = 0
    proposer_match = stable_matches[0]
    student_match = stable_matches[1]
    for p,s in proposer_match.items(): 
        #get proposer prprecision_rangiorities
        p_preferences = proposers_preferences[p]
        #get student priorities
        s_preferences = students_preferences[s]
        #get proposer index in student priorities
        assigned_student_priority = p_preferences.index(s)
        #gte student index in proposer  priorities
        assigned_proposal_priority = s_preferences.index(p)
        sigma = sigma + pow((assigned_student_priority - moyenne),2)
        sigma = sigma + pow((assigned_proposal_priority - moyenne),2)
        variance = sigma/8
    print("variance = ", variance)











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

    stable_matches = gale_shapley(proposers, students)

    isStable = is_stable_match(proposersX, studentsX, stable_matches)
    print("\n::stable_matches :: ")
    print(stable_matches)

    moyenne = analyse_moyenne(stable_matches, proposersX, studentsX)
    analyse_ratio_satisfaction(stable_matches, proposersX, studentsX, moyenne)
    analyse_utilitariste(stable_matches, proposersX, studentsX)
    analyse_variance(stable_matches, proposersX, studentsX, moyenne)
    analyse_ponderee(stable_matches, proposersX, studentsX)

    # gini_proposers = calculate_gini_coefficient(proposersX)
    # gini_students = calculate_gini_coefficient(studentsX)

    # print(f"Gini coefficient for proposers: {gini_proposers}")
    # print(f"Gini coefficient for students: {gini_students}")