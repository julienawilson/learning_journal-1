$(document).ready(function(){
    var deleters = $(".delete");
    deleters.on("click", function(){
        // send ajax request to delete this expense
        event.preventDefault();
        $.ajax({
            url: '/' + $(this).attr("data") + '/delete',
            success: function(){
                console.log("deleted");
            }
        });        
        this_row = $(this.parentNode);
        // delete the entry
        this_row.animate({
            opacity: 0
        }, 500, function(){
            $(this).remove();
        })
    });
});
