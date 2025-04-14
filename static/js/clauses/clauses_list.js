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
                    <a href="#" class="edit-clause-btn" title="Editar">
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
