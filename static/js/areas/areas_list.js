$(document).ready(function () {
    initTableArea()

    $('#createAreaForm').on('submit', function (event) {
        event.preventDefault();

        // var url = $(this).data('url');
        var url = $(this).attr('data-url');

        var name_area = $('#name_area').val();

        if (!name_area) {
            alertSwitch("error", "Todos los campos son obligatorios.");
            return;
        }
        console.log(name_area);


        $.ajax({
            type: 'POST',
            url: url,
            data: {
                name_area: name_area,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                if (response.success) {

                    $('#areas_table').DataTable().destroy();
                    $('#areas_table tbody').empty();

                    $('#createAreaModal').modal('hide');
                    alertSwitch('success', 'Creación éxitosa')

                    $.each(response.areas, function (index, area) {
                        insertAreaRow(index, area);
                    });

                    initTableArea()
                } else {
                    alertSwitch("error", "Hubo un error al crear la cláusula: " + response.message);
                }
            }
        });
    });

});


$(document).on('click', '.delete-area-btn', function (e) {
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
                $('#areas_table').DataTable().destroy();
                $('#areas_table tbody').empty();
                alertSwitch('success', response.message);
                $.each(response.areas, function (index, area) {
                    insertAreaRow(index, area);
                });

                initTableArea()

            } else {
                alertSwitch('error', response.message);
            }
        },
        error: function () {
            alertSwitch('error', 'Error al eliminar la cláusula');
        }
    });
});

$(document).on('click', '.edit-area-btn', function (e) {
    e.preventDefault();

    const modal = $('#createAreaModal');

    // Set modal title and fill fields
    modal.find('.modal-title').text('Editar Área');
    modal.find('#name_area').val($(this).data('name'));

    const form = modal.find('#createAreaForm');
    form.attr('data-url', $(this).data('url'));

    modal.modal('show');
});


$(document).on('click', '#createAreaBtn', function () {
    const modal = $('#createAreaModal');

    modal.find('.modal-title').text('Crear Área');
    modal.find('#name_area').val('');

    const form = modal.find('#createAreaForm');
    form.attr('data-url', $(this).data('url'));

    modal.modal('show');
});




function insertAreaRow(index, area) {
    $('#areas_table tbody').append(
        `<tr>
            <td>
                ${index + 1}
            </td>
            <td>
                ${area.name_area}
            </td>
            <td>
                ${formatDate(area.created_at)}
            </td>
            <td>
                <div class="area-actions">
                     <a href="#" class="edit-area-btn" data-id="${area.id}" data-name="${area.name_area}"
                        data-url="${area.update_url}" title="Editar">
                        <i class="fa fa-edit"></i>
                    </a>
                    <button type="button" class="delete-area-btn"
                        data-url="${area.delete_url}" title="Eliminar">
                        <i class="fa fa-trash"></i>
                    </button>
                </div>
            </td>
        </tr>`
    )
}

function initTableArea() {
    $('#areas_table').DataTable({
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
