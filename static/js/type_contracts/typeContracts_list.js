$(document).ready(function () {
    initTabletypeC()

    $('#createTypeCForm').on('submit', function (event) {
        event.preventDefault();

        var url = $(this).attr('data-url');

        var type_contract = $('#type_contract').val();

        if (!type_contract) {
            alertSwitch("error", "Todos los campos son obligatorios.");
            return;
        }

        $.ajax({
            type: 'POST',
            url: url,
            data: {
                type_contract: type_contract,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                if (response.success) {

                    $('#typeContracts_table').DataTable().destroy();
                    $('#typeContracts_table tbody').empty();

                    $('#createTypeCModal').modal('hide');
                    alertSwitch('success', response.message)

                    $.each(response.typeContracts, function (index, typeC) {
                        inserttypeCRow(index, typeC);
                    });

                    initTabletypeC()
                } else {
                    alertSwitch("error", "Hubo un error al crear el Tipo de Contrato: " + response.message);
                }
            }
        });
    });

});


$(document).on('click', '.delete-typeC-btn', function (e) {
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
                $('#typeContracts_table').DataTable().destroy();
                $('#typeContracts_table tbody').empty();
                alertSwitch('success', response.message);
                $.each(response.typeContracts, function (index, typeC) {
                    inserttypeCRow(index, typeC);
                });

                initTabletypeC()

            } else {
                alertSwitch('error', response.message);
            }
        },
        error: function () {
            alertSwitch('error', 'Error al eliminar el Tipo de Contrato');
        }
    });
});

$(document).on('click', '.edit-typeC-btn', function (e) {
    e.preventDefault();

    const modal = $('#createTypeCModal');

    // Set modal title and fill fields
    modal.find('.modal-title').text('Editar Tipo de Contrato');
    modal.find('#type_contract').val($(this).data('name'));

    const form = modal.find('#createTypeCForm');
    form.attr('data-url', $(this).data('url'));

    console.log(form.attr('data-url'));

    modal.modal('show');
});


$(document).on('click', '#createTypeCBtn', function () {
    const modal = $('#createTypeCModal');

    modal.find('.modal-title').text('Crear Tipo de Contrato');
    modal.find('#type_contract').val('');

    const form = modal.find('#createTypeCForm');
    form.attr('data-url', $(this).data('url'));

    modal.modal('show');
});




function inserttypeCRow(index, typeC) {
    $('#typeContracts_table tbody').append(
        `<tr>
            <td>
                ${index + 1}
            </td>
            <td>
                ${typeC.type_contract}
            </td>
            <td>
                ${formatDate(typeC.created_at)}
            </td>
            <td>
                <div class="typeC-actions">
                     <a href="#" class="edit-typeC-btn" data-id="${typeC.id}" data-name="${typeC.type_contract}"
                        data-url="${typeC.update_url}" title="Editar">
                        <i class="fa fa-edit"></i>
                    </a>
                    <button type="button" class="delete-typeC-btn"
                        data-url="${typeC.delete_url}" title="Eliminar">
                        <i class="fa fa-trash"></i>
                    </button>
                </div>
            </td>
        </tr>`
    )
}

function initTabletypeC() {
    $('#typeContracts_table').DataTable({
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
