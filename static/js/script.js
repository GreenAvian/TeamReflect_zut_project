// Hides/shows the for_target fields in feedback creation
document.addEventListener('DOMContentLoaded', function() {
    const targetFieldDropdown = document.getElementById('target_field');
    const targer_user_field = document.getElementById('feedback-form-target-user');
    const targer_group_field = document.getElementById('feedback-form-target-group');
    const targer_post_field = document.getElementById('feedback-form-target-post');
    

    if (!targetFieldDropdown) {
        return;
    }

    // Function to show the selected field and hide others
    function updateVisibleField() {
        const selectedValue = targetFieldDropdown.value;
        const userValue = document.getElementById('id_for_user').value;
        const groupValue = document.getElementById('id_for_group').value;
        const postValue = document.getElementById('id_for_post').value;
        // Hide all fields
        targer_user_field.style.display = 'none';
        targer_group_field.style.display = 'none';
        targer_post_field.style.display = 'none';


        // Show the selected field
        if (selectedValue === 'user') {
            targer_user_field.style.display = 'block';
        } else if (selectedValue === 'group') {
            targer_group_field.style.display = 'block';
        } else if (selectedValue === 'post') {
            targer_post_field.style.display = 'block';
        }

        if (userValue !== undefined  && userValue !== "") {
            targer_user_field.style.display = 'block';
        }
        if (groupValue !== undefined  && groupValue !== "") {
            targer_group_field.style.display = 'block';
        }
        if (postValue !== undefined  &&  postValue !== "") {
            targer_post_field.style.display = 'block';
        }
    }

    // Update the visible field when the dropdown selection changes
    targetFieldDropdown.addEventListener('change', updateVisibleField);

    // Initial field display based on the default dropdown value
    updateVisibleField();
});


document.addEventListener('DOMContentLoaded', function() {//Function that allows to save all profile fields at once
    document.getElementById('profileAllForm').addEventListener('submit', function(e) {  
        // const avatar = document.getElementById('displayedImageForm').textContent;
        const firstName = document.getElementById('displayedNameForm').value;
        const lastName = document.getElementById('displayedSurnameForm').value;
        const phone = document.getElementById('displayedPhoneForm').value;
        const description = document.getElementById('displayedDescForm').value;

        
        // document.getElementById('hiddenImageForm').value = avatar;
        document.getElementById('hiddenNameForm').value = firstName;
        document.getElementById('hiddenSurnameForm').value = lastName;
        document.getElementById('hiddenPhoneForm').value = phone;
        document.getElementById('hiddenDescForm').value = description;
        
    });
});
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

function hide_or_show(divId) {
    var element = document.getElementById(divId)
    if (element.style.display === 'none')
    {element.style.display = 'block'}
    else if ( element.style.display === 'block')
    {element.style.display = 'none'}
}


//      Alias for comments
function postComment(formId) {
    editField(formId);
}

function cancelComment(formId) {
    cancelEdit(formId);
}

document.addEventListener('DOMContentLoaded', function () {
    const addOptionBtn = document.getElementById('addPollOptionBtn');
    var pollCounter = 1;

    if (addOptionBtn) {
        addOptionBtn.addEventListener('click', function () {
            addPollOptionFunc('pollOptionsContainer'); // Change to your actual container ID
        });
    }

function addPollOptionFunc(pollOptionsContainer) {
    const newOption = document.createElement('div');
    newOption.className = 'group-poll-option';
    newOption.innerHTML = `<input type="text" placeholder="Opcja ${pollCounter}" name="pollOption[]">`;
    pollCounter += 1;
    document.getElementById(pollOptionsContainer).appendChild(newOption);
    }
});