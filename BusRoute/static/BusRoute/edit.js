document.addEventListener('DOMContentLoaded', function () {
    const editButton = document.getElementById('editButton');
    let isEditMode = false;

    editButton.addEventListener('click', function () {
        isEditMode = !isEditMode;
        toggleEditMode(isEditMode);
        editButton.textContent = isEditMode ? 'Save' : 'Edit';
    });

    function toggleEditMode(isEditMode) {
        console.log('Edit Mode:', isEditMode);
        const routeTitle = document.getElementById('routeTitle');
        const editableElements = document.querySelectorAll('.editable');

        if (isEditMode) {
            // Enter edit mode
            if (routeTitle) {
                const titleInput = document.createElement('input');
                titleInput.type = 'text';
                titleInput.value = routeTitle.textContent.trim();
                titleInput.id = 'titleInput';
                routeTitle.innerHTML = '';
                routeTitle.appendChild(titleInput);
            }

            editableElements.forEach(element => {
                const input = document.createElement('input');
                input.type = 'text';
                input.value = element.textContent.trim();
                element.innerHTML = '';
                element.appendChild(input);
            });
        } else {
            // Exit edit mode and save changes
            const titleInput = document.getElementById('titleInput');
            if (titleInput && routeTitle) {
                routeTitle.textContent = titleInput.value.trim();
            }

            editableElements.forEach(element => {
                const input = element.querySelector('input');
                if (input) {
                    element.textContent = input.value.trim();
                }
            });

            saveChanges();
        }
    }

    function saveChanges() {
        const routeIdElement = document.getElementById('routeId');
        const routeTitleElement = document.getElementById('routeTitle');
        const tableData = getTableData();

        if (!routeIdElement || !routeTitleElement) {
            console.error('Route ID or title element not found.');
            return;
        }

        const routeId = routeIdElement.textContent.trim();
        let routeTitle = '';

        const titleInput = document.getElementById('titleInput');
        if (titleInput) {
            routeTitle = titleInput.value.trim();
        } else {
            routeTitle = routeTitleElement.textContent.trim();
        }

        // Get CSRF token from the cookie
        const csrfToken = getCookie('csrftoken');

        const formData = new FormData();
        formData.append('id', routeId);
        formData.append('title', routeTitle);
        formData.append('pickup_data', JSON.stringify(tableData.pickupData));
        formData.append('drop_data', JSON.stringify(tableData.dropData));

        fetch('/update_route/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Success:', data);
                console('Success: ' + JSON.stringify(data));
            })
            .catch(error => {
                console.error('Error:', error);
                console('Error: ' + error.message);
            });
    }

    function getTableData() {
        const pickupTable = document.getElementById('pickupTable');
        const dropTable = document.getElementById('dropTable');

        if (!pickupTable || !dropTable) {
            console.error('One or both tables not found.');
            return { pickupData: [], dropData: [] };
        }

        const pickupData = Array.from(pickupTable.querySelectorAll('tbody tr')).map(row => {
            return {
                name: row.querySelector('td[data-type="stop"]').textContent.trim(),
                times: Array.from(row.querySelectorAll('td[data-type="time"]')).map(cell => cell.textContent.trim())
            };
        });

        const dropData = Array.from(dropTable.querySelectorAll('tbody tr')).map(row => {
            return {
                name: row.querySelector('td[data-type="stop"]').textContent.trim(),
                times: Array.from(row.querySelectorAll('td[data-type="time"]')).map(cell => cell.textContent.trim())
            };
        });

        return { pickupData, dropData };
    }

    // Utility function to get the CSRF token from the cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    //Confirming before deleting

    document.getElementById('deleteForm').addEventListener('submit',function(event){
        if(!confirm('Are you sure you want to delete this bus route? ')){
            event.preventDefault();
        }
    })
});
