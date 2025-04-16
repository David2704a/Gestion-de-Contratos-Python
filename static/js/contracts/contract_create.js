function switchTab(tab) {
    if (tab === 'select') {
        document.getElementById('tabSelect').classList.add('active');
        document.getElementById('tabCreate').classList.remove('active');
        document.getElementById('selectTabContent').style.display = 'block';
        document.getElementById('createTabContent').style.display = 'none';
    } else {
        document.getElementById('tabSelect').classList.remove('active');
        document.getElementById('tabCreate').classList.add('active');
        document.getElementById('selectTabContent').style.display = 'none';
        document.getElementById('createTabContent').style.display = 'block';
    }
}

new Sortable(document.getElementById('clausesContainer'), {
    animation: 150,
    ghostClass: 'sortable-ghost'
});

const addedClauses = new Set();

document.getElementById('addExistingClauseBtn').addEventListener('click', function () {
    const select = document.getElementById('existing_clauses');
    const selectedOption = select.options[select.selectedIndex];

    const id = selectedOption.value;
    const title = selectedOption.dataset.title;
    const description = selectedOption.dataset.description;

    if (!id) {
        alert('Por favor seleccione una cláusula');
        return;
    }

    if (addedClauses.has(id)) {
        alert('Esta cláusula ya ha sido agregada.');
        return;
    }

    const newClause = document.createElement('div');
    newClause.className = 'clause-item';
    newClause.dataset.id = id;
    newClause.innerHTML = `
        <div>
            <div class="clause-title"><strong>${title}</strong></div>
            <div class="clause-description">${description}</div>
        </div>
        <div class="clause-actions">
            <button class="btn btn-danger btn-sm" onclick="removeClause(this)">
                <i class="fas fa-trash"></i> Eliminar
            </button>
        </div>
    `;

    document.getElementById('clausesContainer').appendChild(newClause);
    addedClauses.add(id);
});

document.getElementById('addClauseBtn').addEventListener('click', function () {
    const title = document.getElementById('clause_title').value.trim();
    const description = document.getElementById('clause_description').value.trim();

    if (!title || !description) {
        alert('Debe completar título y descripción de la cláusula.');
        return;
    }

    const uniqueId = `new-${Date.now()}`;

    const newClause = document.createElement('div');
    newClause.className = 'clause-item';
    newClause.dataset.id = uniqueId;
    newClause.innerHTML = `
        <div>
            <div class="clause-title"><strong>${title}</strong></div>
            <div class="clause-description">${description}</div>
        </div>
        <div class="clause-actions">
            <button class="btn btn-danger btn-sm" onclick="removeClause(this)">
                <i class="fas fa-trash"></i> Eliminar
            </button>
        </div>
    `;

    document.getElementById('clausesContainer').appendChild(newClause);
    addedClauses.add(uniqueId);

    document.getElementById('clause_title').value = '';
    document.getElementById('clause_description').value = '';
});

function removeClause(button) {
    const clause = button.closest('.clause-item');
    const id = clause.dataset.id;
    clause.remove();
    addedClauses.delete(id);
}

document.getElementById('saveClausesBtn').addEventListener('click', function () {
    const clauseItems = document.querySelectorAll('.clause-item');

    if (clauseItems.length === 0) {
        alertSwitch('error', 'Debe agregar al menos una cláusula antes de guardar.');
        return;
    }

    const clauseOrder = [];

    clauseItems.forEach((item, index) => {
        clauseOrder.push({
            id: item.dataset.id,
            title: item.querySelector('.clause-title').innerText,
            description: item.querySelector('.clause-description').innerText,
            position: index + 1
        });
    });

    alertSwitch('success', 'Las cláusulas se guardaron correctamente.');
});


document.getElementById('contractForm').addEventListener('submit', function (e) {
    const clauseItems = document.querySelectorAll('.clause-item');
    const clauseOrder = [];

    clauseItems.forEach((item, index) => {
        clauseOrder.push({
            title: item.querySelector('.clause-title').innerText,
            description: item.querySelector('.clause-description').innerText,
            position: index + 1
        });
    });

    document.getElementById('clausesInput').value = JSON.stringify(clauseOrder);

});

$('#contractForm').on('submit', function (event) {
    event.preventDefault();

    let formData = new FormData(this);
    var url = $(this).attr('data-url');
    $.ajax({
        url: url,
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            if (response.success) {
                alertSwitch('success', response.message);
                setTimeout(function () {
                    window.location.href = response.redirect_url;
                }, 2000);
            } else {
                alertSwitch('error', response.message || 'Error desconocido');
            }
        },
        error: function (xhr, status, error) {
            alertSwitch('error', 'Ocurrió un error inesperado.');
            console.error('Error AJAX:', error);
        }
    });
});
