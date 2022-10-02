$(document).ready(function() {
    $('#like_btn').click(function() {
        var categoryIdVar;
        categoryIdVar = $(this).attr('data-categoryid');
        $.get('khoja/like_category/', {'category_id':categoryIdVar},
        function(data) {
            $('#like_count').html(data);
            $('#like_btn').hide();
        })
    });
});

// implementing search suggestion...
$('#search_input').keyup(function() {

    var query;
    query = $(this).val();
    
    $.get('/khoja/suggest', {'suggestion':query},
    function(data) {
        $('#categories-listing').html(data);
    })
})
