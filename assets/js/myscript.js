/**
 * Created by Gentle on 29/9/16.
 */

$(function(){
    $('#search').keyup(function () {

        $.ajax({
            type:"POST",
            url:"http://127.0.0.1:8000/search/",
            data:{
                'search_text': $('#search').val(),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success : searchSuccess,
            dataType: 'html'

        });

    });


    });

function searchSuccess(data, textStatus, jqXHR) {
    $('#search-results').html(data);
    
}




//'csrfmiddlewaretoken': '{{ csrf_token}}'