function ajaxEdit(id, new_title, new_body) {
    $.ajax({
        url: '/journal/' + id + '/edit-entry',
        data: {
            'title': new_title,
            'body': new_body,
            'id': id
                    },
        method: 'POST'
    });
}