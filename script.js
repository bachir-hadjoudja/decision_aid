const internships = ['Internship A', 'Internship B', 'Internship C', 'Internship D'];
const students = ['Student X', 'Student Y', 'Student Z', 'Student W'];
const prioritiesForm = document.getElementById('priorities-form');
let currentUserRole;
let selectedOptions = [];

function displayOptions() {
    currentUserRole = document.getElementById('role').value;
    const listElement = document.getElementById('list');
    listElement.innerHTML = '';
    document.getElementById('options').style.display = 'none';

    if (currentUserRole === 'student') {
        internships.forEach((internship, index) => {
            const listItem = document.createElement('li');
            listItem.textContent = internship;
            listElement.appendChild(listItem);
        });
    } else if (currentUserRole === 'recruiter') {
        students.forEach((student, index) => {
            const listItem = document.createElement('li');
            listItem.textContent = student;
            listElement.appendChild(listItem);
        });
    }

    if (currentUserRole === 'select') return;

    document.getElementById('options').style.display = 'block';
    updatePrioritiesForm();
}

function updatePrioritiesForm() {
    const priorities = prioritiesForm.querySelectorAll('input[name="priority"]');
    priorities.forEach((priority, index) => {
        priority.value = (currentUserRole === 'student' ? internships[index] : students[index]);
        priority.nextSibling.textContent = currentUserRole === 'student' ? internships[index] : students[index];
    });
}

function savePriorities() {
    const selectedPriorities = prioritiesForm.querySelectorAll('input[name="priority"]:checked');
    if (selectedPriorities.length !== 4) {
        alert('Please select exactly 4 priorities.');
        return;
    }
    
    selectedOptions = Array.from(selectedPriorities).map(priority => priority.value);
    
    let data = JSON.parse(localStorage.getItem('choices')) || {recruiters: {}, students: {}};
    
    if (currentUserRole === 'student') {
        data.students['student-1'] = selectedOptions; // Ideally, 'student-1' should be dynamic based on user identification
    } else if (currentUserRole === 'recruiter') {
        data.recruiters['recruiter-1'] = selectedOptions; // Similarly, 'recruiter-1' should be the actual recruiter's identifier
    }

    localStorage.setItem('choices', JSON.stringify(data));
    console.log('Saved choices:', data);
}

window.onload = function() {
    // Load previously saved choices if any
    let data = localStorage.getItem('choices');
    if (data) {
        console.log('Previous choices:', JSON.parse(data));
    }
};

