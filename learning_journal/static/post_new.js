$(document).ready(function(){

    $('#index_form').hide();

    hideAndShowForm = function() {
        $('#new_form').on('click', '.show_form', function() {
            event.preventDefault();
            $('#index_form').show();
            $(this).html('Go away form').removeClass('show_form').addClass('hide_form');
        })

        $('#new_form').on('click', '.hide_form', function() {
            event.preventDefault();
            $('#index_form').hide();
            $(this).html('come back form').removeClass('hide_form').addClass('show_form');
        })
    }

    postNewEntry = function() {
        $('#submit_new').on('click', function() {
            $.ajax({
                url: 'journal/new-entry',
                data: {
                    'csrf_token': $("[name='csrf_token']").val(),
                    'title': $("[name='title']").val(),
                    'body': $("[name='body']").val()
                    },
            method: 'POST' 
        });
            console.log("worked!")

        });
        event.preventDefault();
    }



hideAndShowForm();
postNewEntry();
})