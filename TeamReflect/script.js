// 1. Nawigacja mobilna
const menuIcon = document.querySelector('.menu-icon');
const navLinks = document.querySelector('.nav-links');

menuIcon.addEventListener('click', () => {
    navLinks.classList.toggle('active');
});

// 2. Tworzenie grupy
const groupForm = document.getElementById('create-group-form');
const membersContainer = document.getElementById('members-container');
const addMemberBtn = document.getElementById('add-member-btn');

if (groupForm && membersContainer && addMemberBtn) {
    let memberCount = 1;

    // Dodaj kolejnego członka
    addMemberBtn.addEventListener('click', () => {
        memberCount++;

        // Tworzenie etykiety i pola tekstowego dla nowego członka
        const newMemberLabel = document.createElement('label');
        newMemberLabel.setAttribute('for', `member-${memberCount}`);
        newMemberLabel.textContent = `Członek ${memberCount}`;

        const newMemberInput = document.createElement('input');
        newMemberInput.setAttribute('type', 'text');
        newMemberInput.setAttribute('id', `member-${memberCount}`);
        newMemberInput.setAttribute('name', 'members[]');
        newMemberInput.setAttribute('placeholder', `Podaj Imię`);

        // Dodanie nowego pola do kontenera
        membersContainer.appendChild(newMemberLabel);
        membersContainer.appendChild(newMemberInput);
    });

    // Obsługa przesyłania formularza
    groupForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const groupName = document.getElementById('group-name').value;
        const memberInputs = document.querySelectorAll('#members-container input');
        const members = Array.from(memberInputs).map(input => input.value).filter(Boolean);

        alert(`Grupa "${groupName}" została stworzona z członkami: ${members.join(', ')}`);

        // Resetowanie formularza
        e.target.reset();
        membersContainer.innerHTML = `
      <label for="member-1">Członek 1</label>
      <input type="text" id="member-1" name="members[]" placeholder="Podaj Imię" required>
    `;
        memberCount = 1;
    });
}

// 3. Dodawanie feedbacku
const feedbackForm = document.getElementById('feedback-form');
const feedbackData = []; // Przechowuje wszystkie feedbacki

if (feedbackForm) {
    feedbackForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const name = document.getElementById('name').value;
        const comment = document.getElementById('comment').value;
        const rating = document.querySelectorAll('#rating span.selected').length;

        if (!name || !rating) {
            alert('Proszę wypełnić wszystkie wymagane pola i dodać ocenę.');
            return;
        }

        // Dodaj nowy feedback
        feedbackData.push({ name, comment, rating });
        alert(`Feedback dodany! Ocena: ${rating} dla ${name}`);

        // Zresetuj formularz
        feedbackForm.reset();
        document.querySelectorAll('#rating span').forEach((s) => s.classList.remove('selected'));
    });
}

// Obsługa gwiazdek ocen
const ratingStars = document.querySelectorAll('#rating span');

if (ratingStars.length > 0) {
    ratingStars.forEach((star, index) => {
        star.addEventListener('click', () => {
            // Usuń zaznaczenie z wszystkich gwiazdek
            ratingStars.forEach((s) => s.classList.remove('selected'));

            // Zaznacz gwiazdkę i wszystkie wcześniejsze
            for (let i = 0; i <= index; i++) {
                ratingStars[i].classList.add('selected');
            }
        });
    });
}

// 4. Przegląd Feedbacku
const feedbackList = document.getElementById('feedback-list');
const filterNameInput = document.getElementById('filter-name');
const sortFeedbackSelect = document.getElementById('sort-feedback');

if (feedbackList) {
    // Funkcja generująca HTML dla opinii
    function renderFeedback(data) {
        feedbackList.innerHTML = '';
        data.forEach(feedback => {
            const feedbackItem = document.createElement('div');
            feedbackItem.classList.add('feedback');
            feedbackItem.innerHTML = `
        <p><strong>Imię:</strong> ${feedback.name}</p>
        <p><strong>Komentarz:</strong> ${feedback.comment}</p>
        <p><strong>Ocena:</strong> ${'★'.repeat(feedback.rating)}${'☆'.repeat(5 - feedback.rating)}</p>
      `;
            feedbackList.appendChild(feedbackItem);
        });
    }

    // Filtrowanie po imieniu
    function filterFeedback() {
        const filterValue = filterNameInput.value.toLowerCase();
        const filteredData = feedbackData.filter(feedback =>
            feedback.name.toLowerCase().includes(filterValue)
        );
        renderFeedback(filteredData);
    }

    // Sortowanie opinii
    function sortFeedback() {
        const sortValue = sortFeedbackSelect.value;
        const sortedData = [...feedbackData].sort((a, b) => {
            return sortValue === 'asc' ? a.rating - b.rating : b.rating - a.rating;
        });
        renderFeedback(sortedData);
    }

    // Event Listeners
    if (filterNameInput) filterNameInput.addEventListener('input', filterFeedback);
    if (sortFeedbackSelect) sortFeedbackSelect.addEventListener('change', sortFeedback);

    // Inicjalne renderowanie opinii
    renderFeedback(feedbackData);
}

// 5. Dashboard
const feedbackCountElement = document.getElementById('feedback-count');
const averageRatingElement = document.getElementById('average-rating');
const mostRatedPersonElement = document.getElementById('most-rated-person');

function calculateDashboardStats() {
    const feedbackCount = feedbackData.length;
    const averageRating =
        feedbackCount > 0
            ? (feedbackData.reduce((sum, feedback) => sum + feedback.rating, 0) / feedbackCount).toFixed(2)
            : 0;

    const mostRatedPerson = feedbackData
        .map(feedback => feedback.name)
        .reduce((acc, name) => {
            acc[name] = (acc[name] || 0) + 1;
            return acc;
        }, {});

    const mostRatedPersonName = Object.keys(mostRatedPerson).reduce((a, b) =>
        mostRatedPerson[a] > mostRatedPerson[b] ? a : b, "Brak danych"
    );

    if (feedbackCountElement) feedbackCountElement.textContent = feedbackCount;
    if (averageRatingElement) averageRatingElement.textContent = averageRating;
    if (mostRatedPersonElement) mostRatedPersonElement.textContent = mostRatedPersonName;
}

// Wywołanie funkcji przy starcie
if (feedbackCountElement && averageRatingElement && mostRatedPersonElement) {
    calculateDashboardStats();
}

// 6. Panel Administratora
const manageUsersBtn = document.getElementById('manage-users-btn');
const viewStatsBtn = document.getElementById('view-stats-btn');
const adminContent = document.getElementById('admin-content');

if (manageUsersBtn) {
    manageUsersBtn.addEventListener('click', () => {
        adminContent.innerHTML = '<h3>Lista użytkowników</h3><ul>' +
            feedbackData
                .map(feedback => `<li>${feedback.name}</li>`)
                .join('') +
            '</ul>';
    });
}

if (viewStatsBtn) {
    viewStatsBtn.addEventListener('click', () => {
        adminContent.innerHTML = '<h3>Statystyki</h3><p>Zobacz Dashboard, aby poznać szczegóły.</p>';
    });
}
