import random
import json
import sys
import matplotlib.pyplot as plt
def generate_test_data_to_json(num_proposers, num_students, filename):
    proposers = {}
    students = {}

    for proposer in range(num_proposers):
        proposer_name = f"Proposer-{proposer + 1}"
        proposer_preferences = random.sample(range(1, num_students + 1), num_students)
        proposers[proposer_name] = [f"Student-{student}" for student in proposer_preferences]

    for student in range(num_students):
        student_name = f"Student-{student + 1}"
        student_preferences = random.sample(range(1, num_proposers + 1), num_proposers)
        students[student_name] = [f"Proposer-{proposer}" for proposer in student_preferences]

    data = {
        "Proposers' Preferences": proposers,
        "Students' Preferences": students
    }

    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <num_proposers> <num_students>")
    else:
        num_proposers = int(sys.argv[1])
        num_students = int(sys.argv[2])
        filename = f"test_data_{num_proposers}_{num_students}.json"
        generate_test_data_to_json(num_proposers, num_students, filename)
        print(f"Generated data and saved to {filename}")