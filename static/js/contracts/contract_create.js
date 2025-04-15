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
// Contador para IDs de nuevas cláusulas
let clauseCounter = 1;

// Función para agregar cláusula existente
document.getElementById('addExistingClauseBtn').addEventListener('click', function () {
    const select = document.getElementById('existing_clauses');
    const selectedOption = select.options[select.selectedIndex];

    if (!selectedOption.value) {
        alert('Por favor seleccione una cláusula');
        return;
    }

    // Aquí normalmente harías una petición al servidor para obtener los detalles
    // de la cláusula seleccionada. Por ahora usaremos datos de ejemplo.
    const clauseData = {};

    $('#existing_clauses option').each(function () {
        const id = $(this).val();
        const title = $(this).data('title');
        const description = $(this).data('description');

        if (id) {
            clauseData[id] = {
                title: title,
                description: description
            };
        }
    });

    const clause = clauseData[selectedOption.value];

    const newClause = document.createElement('div');
    newClause.className = 'clause-item';
    newClause.dataset.id = selectedOption.value;
    newClause.innerHTML = `
    <div>
        <div class="clause-title">${clause.title}</div>
        <div class="clause-description">${clause.description}</div>
    </div>
    <div class="clause-actions">
        <button class="btn btn-danger btn-sm" onclick="removeClause(this)">
            <i class="fas fa-trash"></i>
        </button>
    </div>
`;

    document.getElementById('clausesContainer').appendChild(newClause);
    select.selectedIndex = 0;
});

// Función para agregar nueva cláusula (original)
document.getElementById('addClauseBtn').addEventListener('click', function () {
    const title = document.getElementById('clause_title').value.trim();
    const description = document.getElementById('clause_description').value.trim();

    if (!title) {
        alert('Por favor ingrese un título para la cláusula');
        return;
    }

    const newClause = document.createElement('div');
    newClause.className = 'clause-item';
    newClause.dataset.id = 'new-' + clauseCounter++;
    newClause.innerHTML = `
    <div>
        <div class="clause-title">${title}</div>
        <div class="clause-description">${description || 'Sin descripción'}</div>
    </div>
    <div class="clause-actions">
        <button class="btn btn-danger btn-sm" onclick="removeClause(this)">
            <i class="fas fa-trash"></i>
        </button>
    </div>
`;

    document.getElementById('clausesContainer').appendChild(newClause);

    // Limpiar campos y ocultar formulario
    document.getElementById('clause_title').value = '';
    document.getElementById('clause_description').value = '';
    document.getElementById('newClauseForm').style.display = 'none';
    document.getElementById('showNewClauseFormBtn').style.display = 'inline-flex';

});
window.removeClause = function (button) {
    if (confirm('¿Está seguro que desea eliminar esta cláusula?')) {
        button.closest('.clause-item').remove();
    }
};
// Función para guardar el orden de las cláusulas
document.getElementById('saveClausesBtn').addEventListener('click', function () {
    const clauses = Array.from(document.querySelectorAll('.clause-item')).map((item, index) => ({
        id: item.dataset.id,
        title: item.querySelector('.clause-title').textContent,
        description: item.querySelector('.clause-description').textContent,
        position: index + 1
    }));

    // Aquí puedes enviar las cláusulas al servidor
    console.log('Cláusulas a guardar:', clauses);
    alert('Orden de cláusulas guardado correctamente');

    // En un entorno real, aquí harías una llamada AJAX para guardar en el servidor
    // fetch('/api/contract-clauses/', {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify({ clauses })
    // })
    // .then(response => response.json())
    // .then(data => alert('Cláusulas guardadas correctamente'))
    // .catch(error => alert('Error al guardar cláusulas'));
});

// Manejar el envío del formulario de contrato
document.getElementById('contractForm').addEventListener('submit', function (e) {
    e.preventDefault();
    // Aquí puedes agregar la lógica para enviar el formulario
    alert('Formulario de contrato enviado');
});
new Sortable(document.getElementById('clausesContainer'), {
    animation: 150,
    ghostClass: 'sortable-ghost',
    onChoose: function (evt) {
        evt.item.classList.add('dragging');
    },
    onUnchoose: function (evt) {
        evt.item.classList.remove('dragging');
    }
});