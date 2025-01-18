//      Renders the add feedback button
document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname.includes('/feedback/') && !window.location.pathname.includes('/feedback/form')) {
        console.log('The URL is in the feedback subfolder.');

        // Create the button element
        const feedbackButton = document.createElement('button');
        feedbackButton.classList.add('generic_button');
        feedbackButton.textContent = 'Dodaj feedback';
        feedbackButton.onclick = () => {
            window.location.href = '/feedback/form';
        };

        // Insert the button below the header
        const header = document.querySelector('header'); // Assuming you have a <header> element
        if (header) {
            header.insertAdjacentElement('afterend', feedbackButton);
        }
    }
});

//      Displays the edit fields on the user profile
function editField(formId) {
    document.getElementById(formId).style.display = 'block';
}

function cancelEdit(formId) {
    document.getElementById(formId).style.display = 'none';
}


const addOptionBtn = document.getElementById('addPollOptionBtn');
var pollCounter = 1;

function addPollOptionFunc(pollOptionsContainer) {
    const newOption = document.createElement('div');
    newOption.className = 'group-poll-option';
    newOption.innerHTML = `<input type="text" placeholder="Opcja ${pollCounter}" name="pollOption[]">`;
    pollCounter += 1;
    document.getElementById(pollOptionsContainer).appendChild(newOption);
}