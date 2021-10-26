
$(document).ready(function(){
    $('.search-box').on('input', function(e){
        $('.search-box').empty();
        text = $('.search-box').val();
        if ($('.search-box').val()){
            $.ajax({
                method:'post',
                data:{aim: text},
                success: function(res){
                    result = '<hr>';
                    if (res['title']){
                        result += '<a href="posts/'+res['id']+'">'+res['title']+'</a>'
                        $('.data-list').html(result);
                    } else {
                        result += 'No Result Found!!!';
                        $('.data-list').html(result);
                    }
                }
            });
        } else {
            $('.data-list').html('')
        }
    });
});
