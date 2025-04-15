$(document).ready(function () {
    initTableClause()

    $('#createClauseForm').on('submit', function (event) {
        event.preventDefault();

        var url = $(this).data('url');
        var organization_id = $('#organization').val();
        var title = $('#title').val();
        var description = $('#description').val();

        if (!organization_id || !title || !description) {
            alertSwitch("error", "Todos los campos son obligatorios.");
            return;
        }

        $.ajax({
            type: 'POST',
            url: url,
            data: {
                organization_id: organization_id,
                title: title,
                description: description,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                console.log(response);

                if (response.success) {

                    $('#clauses_table').DataTable().destroy();
                    $('#clauses_table tbody').empty();

                    $('#createClauseModal').modal('hide');
                    alertSwitch('success', 'Creación éxitosa')

                    $.each(response.clauses, function (index, clause) {
                        insertClauseRow(index, clause);
                    });

                    initTableClause()
                } else {
                    alertSwitch("error", "Hubo un error al crear la cláusula: " + response.message);
                }
            }
        });
    });

});


$(document).on('click', '.delete-clause-btn', function (e) {
    e.preventDefault();
    const url = $(this).data('url');
    const csrfToken = $('input[name=csrfmiddlewaretoken]').val();

    $.ajax({
        url: url,
        type: 'POST',
        data: {
            csrfmiddlewaretoken: csrfToken
        },
        success: function (response) {

            if (response.success) {
                $('#clauses_table').DataTable().destroy();
                $('#clauses_table tbody').empty();
                alertSwitch('success', response.message);
                $.each(response.clauses, function (index, clause) {
                    insertClauseRow(index, clause);
                });

                initTableClause()

            } else {
                alertSwitch('error', response.message);
            }
        },
        error: function () {
            alertSwitch('error', 'Error al eliminar la cláusula');
        }
    });
});

$(document).on('click', '.edit-clause-btn', function (e) {
    e.preventDefault();

    const modal = $('#createClauseModal');

    // Set modal title and fill fields
    modal.find('.modal-title').text('Editar Cláusula');
    modal.find('#title').val($(this).data('title'));
    modal.find('#description').val($(this).data('description'));
    modal.find('#organization').val($(this).data('organization'));

    const form = modal.find('#createClauseForm');
    form.attr('data-url', $(this).data('url'));

    // 🔒 Deshabilitar select y aplicar clases como si no fuera superadmin
    const orgGroup = modal.find('#organization').closest('.form-group');
    const orgSelect = modal.find('#organization');
    const disabledInfo = orgGroup.find('.disabled-info');

    orgGroup.addClass('disabled-field');
    orgSelect.prop('disabled', true);
    disabledInfo.removeClass('hidden');

    modal.modal('show');
});


$(document).on('click', '#createClauseBtn', function () {
    const modal = $('#createClauseModal');

    modal.find('.modal-title').text('Crear Cláusula');
    modal.find('#title').val('');
    modal.find('#description').val('');
    modal.find('#organization').val('');


    const form = modal.find('#createClauseForm');
    form.attr('data-url', $(this).data('url'));


    const orgGroup = modal.find('#organization').closest('.form-group');
    const orgSelect = modal.find('#organization');
    const disabledInfo = orgGroup.find('.disabled-info');

    orgGroup.removeClass('disabled-field');
    orgSelect.prop('disabled', false);
    disabledInfo.addClass('hidden');

    modal.modal('show');
});




function insertClauseRow(index, clause) {
    $('#clauses_table tbody').append(
        `<tr>
            <td>
                ${index + 1}
            </td>
            <td>
                ${clause.title}
            </td>
            <td>
            ${clause.description}
            </td>
            <td>
                <span class="org-tag" style="background: #8bb8ff">
                    ${clause.organization}
                </span>
            </td>
            <td>
                ${formatDate(clause.created_at)}
            </td>
            <td>
                <div class="clause-actions">
                     <a href="#" class="edit-clause-btn" data-id="${clause.id}" data-title="${clause.title}"
                        data-description="${clause.description}" data-organization="${clause.organization_id}"
                        data-url="${clause.update_url}" title="Editar">
                        <i class="fa fa-edit"></i>
                    </a>
                    <button type="button" class="delete-clause-btn"
                        data-url="${clause.delete_url}" title="Eliminar">
                        <i class="fa fa-trash"></i>
                    </button>
                </div>
            </td>
        </tr>`
    )
}

function initTableClause() {
    $('#clauses_table').DataTable({
        "language": {
            "search": "",
            "searchPlaceholder": "Buscar usuarios...",
            "lengthMenu": "Mostrar _MENU_ registros",
            "info": "Mostrando _START_ a _END_ de _TOTAL_ registros",
            "paginate": {
                "previous": "‹",
                "next": "›"
            }
        },
        // "dom": '<"top"f>rt<"bottom"lip>',
    });
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });
}
