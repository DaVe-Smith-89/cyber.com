
$(document).ready(function(){
    $('.search-box').on('input', function(e){
        text = $('.search-box').val();
        if ($('.search-box').val()){
            $.ajax({
                method:'post',
                data:{aim: text},
                url: '/tools',
                success: function(res){
                    result = '<hr>';
                    if (res['title']){
                        result += '<a href="/tool/'+res['id']+'">'+res['title']+'</a>'
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
