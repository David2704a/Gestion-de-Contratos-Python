$(document).ready(function () {
    initTablePost()

    $('#createPostForm').on('submit', function (event) {
        event.preventDefault();

        var url = $(this).attr('data-url');
        var area_id = $('#area').val();
        var name_posts = $('#name_posts').val();

        if (!area_id || !name_posts ) {
            alertSwitch("error", "Todos los campos son obligatorios.");
            return;
        }

        $.ajax({
            type: 'POST',
            url: url,
            data: {
                area_id: area_id,
                name_posts: name_posts,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                console.log(response);

                if (response.success) {

                    $('#posts_table').DataTable().destroy();
                    $('#posts_table tbody').empty();

                    $('#createPostModal').modal('hide');
                    alertSwitch('success', 'Creación éxitosa')

                    $.each(response.posts, function (index, post) {
                        insertPostRow(index, post);
                    });

                    initTablePost()
                } else {
                    alertSwitch("error", "Hubo un error al crear la cláusula: " + response.message);
                }
            }
        });
    });

});


$(document).on('click', '.delete-post-btn', function (e) {
    e.preventDefault();
    var url = $(this).attr('data-url');

    const csrfToken = $('input[name=csrfmiddlewaretoken]').val();

    $.ajax({
        url: url,
        type: 'POST',
        data: {
            csrfmiddlewaretoken: csrfToken
        },
        success: function (response) {

            if (response.success) {
                $('#posts_table').DataTable().destroy();
                $('#posts_table tbody').empty();
                alertSwitch('success', response.message);
                $.each(response.posts, function (index, post) {
                    insertPostRow(index, post);
                });

                initTablePost()

            } else {
                alertSwitch('error', response.message);
            }
        },
        error: function () {
            alertSwitch('error', 'Error al eliminar la cláusula');
        }
    });
});

$(document).on('click', '.edit-post-btn', function (e) {
    e.preventDefault();

    const modal = $('#createPostModal');

    modal.find('.modal-title').text('Editar Cláusula');
    modal.find('#name_posts').val($(this).data('name'));
    modal.find('#area').val($(this).data('area'));


    const form = modal.find('#createPostForm');
    form.attr('data-url', $(this).data('url'));

    const orgGroup = modal.find('#area').closest('.form-group');
    const orgSelect = modal.find('#area');
    const disabledInfo = orgGroup.find('.disabled-info');

    orgGroup.addClass('disabled-field');
    orgSelect.prop('disabled', true);
    disabledInfo.removeClass('hidden');

    modal.modal('show');
});


$(document).on('click', '#createPostBtn', function () {
    const modal = $('#createPostModal');

    modal.find('.modal-title').text('Crear Cargo');
    modal.find('#name_posts').val('');
    modal.find('#area').val('');


    const form = modal.find('#createPostForm');
    form.attr('data-url', $(this).data('url'));

    const orgGroup = modal.find('#area').closest('.form-group');
    const orgSelect = modal.find('#area');
    const disabledInfo = orgGroup.find('.disabled-info');

    orgGroup.removeClass('disabled-field');
    orgSelect.prop('disabled', false);
    disabledInfo.addClass('hidden');

    modal.modal('show');
});




function insertPostRow(index, post) {
    $('#posts_table tbody').append(
        `<tr>
            <td>
                ${index + 1}
            </td>
            <td>
                ${post.name_posts}
            </td>
            <td>
                <span class="org-tag" style="background: #8bb8ff">
                    ${post.area}
                </span>
            </td>
            <td>
                ${formatDate(post.created_at)}
            </td>
            <td>
                <div class="post-actions">
                     <a href="#" class="edit-post-btn" data-id="${post.id}" data-name="${post.name_posts}"
                        data-area="${post.area_id}"
                        data-url="${post.update_url}" title="Editar">
                        <i class="fa fa-edit"></i>
                    </a>
                    <button type="button" class="delete-post-btn"
                        data-url="${post.delete_url}" title="Eliminar">
                        <i class="fa fa-trash"></i>
                    </button>
                </div>
            </td>
        </tr>`
    )
}

function initTablePost() {
    $('#posts_table').DataTable({
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
