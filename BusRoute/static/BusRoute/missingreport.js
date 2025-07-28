document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM is loaded");

    // IIFE to handle form validation
    (() => {
        'use strict';
        const forms = document.querySelectorAll('.needs-validation');
        console.log("Forms found: ", forms.length);

        Array.prototype.slice.call(forms)
            .forEach((form) => {
                form.addEventListener('submit', (event) => {
                    if (!form.checkValidity()) {
                        event.preventDefault();
                        event.stopPropagation();
                    }
                    form.classList.add('was-validated');
                }, false);
            });
    })();

    // CSRF Token Handling
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log("CSRF Token: ", csrfToken);

    // Delete Complaint
    document.querySelectorAll('.delete-complaint').forEach(button => {
        console.log("Delete button found");
        button.addEventListener('click', function() {
            console.log("Deleting Complaint");
            const complaintId = this.getAttribute('data-id');
            console.log("Complaint ID: ", complaintId);

            if (confirm('Are you sure you want to delete this complaint?')) {
                fetch(`/delete-missing-item/${complaintId}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    }
                })
                .then(response => response.json())
                .then(data => {
                    console.log("Delete response data: ", data);
                    if (data.success) {
                        location.reload();
                    } else {
                        alert('Failed to delete the complaint.');
                    }
                })
                .catch(error => console.error('Error:', error));
            }
        });
    });

    // Edit Complaint
    document.querySelectorAll('.edit-complaint').forEach(button => {
        console.log("Edit button found");
        button.addEventListener('click', function() {
            console.log("Editing Complaint");
            const complaintId = this.getAttribute('data-id');
            console.log("Complaint ID: ", complaintId);
            window.location.href = `/edit-missing-item/${complaintId}/`;
        });
    });

    // Update Status Form
    document.querySelectorAll('.update-status-form').forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            console.log("Updating Status Form");
            const complaintId = this.getAttribute('data-id');
            const formData = new FormData(this);

            fetch(`/update-missing-item-status/${complaintId}/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log("Update status response data: ", data);
                if (data.success) {
                    alert('Status updated successfully.');
                    location.reload();
                } else {
                    alert('Failed to update status.');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // Submit Complaint Form
    document.getElementById('complaint-form').addEventListener('submit', function(event) {
        event.preventDefault();
        
        const form = event.target;
        const formData = new FormData(form);

        console.log("FormData: ", Array.from(formData.entries()));

        fetch(window.urls.reportMissingItems, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            }
        })    
        .then(response => response.json())
        .then(data => {
            console.log("Complaint submitted successfully: ", data);
            const complaintsList = document.getElementById('complaints-list');

            const complaintBox = document.createElement('div');
            complaintBox.classList.add('complaint-box', 'mb-3', 'p-3', 'border', 'rounded');
            complaintBox.setAttribute('data-id', data.id);

            complaintBox.innerHTML = `
                <h4>${data.item_name}</h4>
                <p><strong>Location:</strong> ${data.location}</p>
                <p><strong>Missing Since:</strong> ${data.date_lost}</p>
                <p><strong>Reported At:</strong> ${data.date_reported}</p>
                <p><strong>Status:</strong> ${data.status}</p>
                ${data.image_url ? `<img src="${data.image_url}" alt="${data.item_name}" class="img-fluid" style="max-width: 100px;">` : ''}
                <p>${data.description}</p>
                <p><strong>Contact Email:</strong> ${data.contact_email}</p>
                <p><strong>Contact Phone:</strong> ${data.contact_phone}</p>
            `;

            complaintsList.prepend(complaintBox);
            form.reset();
            alert("Complain Added")
        })
        .catch(error => console.error('Error:', error));
    });

    // Tab Switcher
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.form-container').forEach(container => container.classList.remove('active'));

            tab.classList.add('active');
            document.getElementById(tab.getAttribute('data-target')).classList.add('active');
        });
    });
});
