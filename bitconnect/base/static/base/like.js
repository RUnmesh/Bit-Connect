function changelike( event ){
    but = $(event);
    if (but.attr('stat') == '1')
    {
        $.ajax({
            url : '/like' , 
            type : 'POST' ,
            data : {
                'post' : but.attr('post')
            },
            success: function(data){
                    but.attr('stat' , '0');
                    document.getElementById(but.attr('post')).innerHTML = data.likes;
                    but.html('<span class="glyphicon glyphicon-thumbs-down"></span>&nbsp;Dislike');
            }
        })
    }
    else
    {
        $.ajax({
            url : '/dislike' , 
            type : 'POST' ,
            data : {
                'post' : but.attr('post')
            },
            success: function(data){
                    but.attr('stat' , '1');
                    document.getElementById(but.attr('post')).innerHTML = data.likes;
                    but.html('<span class="glyphicon glyphicon-thumbs-up"></span>&nbsp;Like');
            }
        })
    }
}