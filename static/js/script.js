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