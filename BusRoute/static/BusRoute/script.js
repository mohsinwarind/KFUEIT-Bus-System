document.addEventListener('DOMContentLoaded', function () {
    const pickupTable = document.getElementById('pickupTable');
    const pickupRows = document.getElementById('pickupRows');
    const addPickupRowButton = document.getElementById('addPickupRow');
    const removePickupRowButton = document.getElementById('removePickupRow');
    const addPickupTimeColumnButton = document.getElementById('addPickupTimeColumn');
    const removePickupTimeColumnButton = document.getElementById('removePickupTimeColumn');

    const dropTable = document.getElementById('dropTable');
    const dropRows = document.getElementById('dropRows');
    const addDropRowButton = document.getElementById('addDropRow');
    const removeDropRowButton = document.getElementById('removeDropRow');
    const addDropTimeColumnButton = document.getElementById('addDropTimeColumn');
    const removeDropTimeColumnButton = document.getElementById('removeDropTimeColumn');



    let pickupColumnCount = 2;  // Start from 2 since we already have Time 1
    let dropColumnCount = 2;
    let pickupRowCount = 1;  // Tracks the number of rows for pickup
    let dropRowCount = 1;  // Tracks the number of rows for drop

    document.getElementById('bus_route').addEventListener('change', function () {
        const newRouteDiv = document.getElementById('newRouteDiv');
        if (this.value === 'new') {
            newRouteDiv.style.display = 'block';
        } else {
            newRouteDiv.style.display = 'none';
        }
    });

    // Add Pickup Row
    addPickupRowButton.addEventListener('click', function () {
        removePickupRowButton.style.display = '';
        const newRow = pickupRows.insertRow();
        newRow.innerHTML = `<td><input type="text" name="pickup[${pickupRowCount}][name]" class="form-control" required></td>`;
        for (let i = 0; i < pickupColumnCount - 1; i++) {
            newRow.innerHTML += `<td><input type="text" name="pickup[${pickupRowCount}][time][${i}]" class="form-control"></td>`;
        }
        pickupRowCount++;
    });

    // Remove Pickup Row
    removePickupRowButton.addEventListener('click', function () {
        if (pickupRows.rows.length > 1) {
            pickupRows.deleteRow(pickupRows.rows.length - 1);
            pickupRowCount--;
        }
        if (pickupRows.rows.length < 2) {
            removePickupRowButton.style.display = 'none';
        }
    });

    // Add Pickup Time Column
    addPickupTimeColumnButton.addEventListener('click', function () {
        removePickupTimeColumnButton.style.display = '';
        const th = document.createElement('th');
        th.innerText = `Time ${pickupColumnCount}`;
        pickupTable.rows[0].appendChild(th);
        for (let i = 0; i < pickupRows.rows.length; i++) {
            const td = document.createElement('td');
            td.innerHTML = `<input type="text" name="pickup[${i}][time][${pickupColumnCount - 1}]" class="form-control">`;
            pickupRows.rows[i].appendChild(td);
        }
        pickupColumnCount++;
    });

    // Remove Pickup Time Column
    removePickupTimeColumnButton.addEventListener('click', function () {
        if (pickupColumnCount > 2) {  // Ensure at least 1 time column exists
            pickupColumnCount--;
            // Remove the last header cell
            pickupTable.rows[0].deleteCell(-1);
            for (let i = 0; i < pickupRows.rows.length; i++) {
                pickupRows.rows[i].deleteCell(-1);
            }
        }
        if (pickupColumnCount < 3) {
            removePickupTimeColumnButton.style.display = 'none';
        }
    });

    // Add Drop Row
    addDropRowButton.addEventListener('click', function () {
        removeDropRowButton.style.display = '';
        const newRow = dropRows.insertRow();
        newRow.innerHTML = `<td><input type="text" name="drop[${dropRowCount}][name]" class="form-control" required></td>`;
        for (let i = 0; i < dropColumnCount - 1; i++) {
            newRow.innerHTML += `<td><input type="text" name="drop[${dropRowCount}][time][${i}]" class="form-control"></td>`;
        }
        dropRowCount++;
    });

    // Remove Drop Row
    removeDropRowButton.addEventListener('click', function () {
        if (dropRows.rows.length > 1) {
            dropRows.deleteRow(dropRows.rows.length - 1);
            dropRowCount--;
        }
        if (dropRows.rows.length < 2) {
            removeDropRowButton.style.display = 'none';
        }
    });

    // Add Drop Time Column
    addDropTimeColumnButton.addEventListener('click', function () {
        removeDropTimeColumnButton.style.display = '';
        const th = document.createElement('th');
        th.innerText = `Time ${dropColumnCount}`;
        dropTable.rows[0].appendChild(th);
        for (let i = 0; i < dropRows.rows.length; i++) {
            const td = document.createElement('td');
            td.innerHTML = `<input type="text" name="drop[${i}][time][${dropColumnCount - 1}]" class="form-control">`;
            dropRows.rows[i].appendChild(td);
        }
        dropColumnCount++;
    });

    // Remove Drop Time Column
    removeDropTimeColumnButton.addEventListener('click', function () {
        if (dropColumnCount > 2) {  // Ensure at least 1 time column exists
            dropColumnCount--;
            // Remove the last header cell
            dropTable.rows[0].deleteCell(-1);
            for (let i = 0; i < dropRows.rows.length; i++) {
                dropRows.rows[i].deleteCell(-1);
            }
        }
        if (dropColumnCount < 3) {
            removeDropTimeColumnButton.style.display = 'none';
        }
    });
});
