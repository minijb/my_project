$(function() {
    $(".text").mouseover(function(){
        $(this).addClass('mouseOver');
        
    });
    $(".text").mouseout(function(){
        $(this).removeClass('mouseOver');
        
    });

    // $(".img_bu").on('click',function(){
    //     let me = $(this)
    //     let a = me.attr("con");
    //     if(a==0){
    //         me.attr("con",1);
    //         me.attr("src","../Img/select_by_age/u251_selected.svg")
    //     }else{
    //         me.attr("con",0);
    //         me.attr("src","../Img/select_by_age/u251.svg")
    //     }
    // });

    // $(".img_bu").mouseover(function(){
    //     let me = $(this)
    //     let a = me.attr("con")
    //     if(a == 0){
    //         me.attr("src","../Img/select_by_age/u251_mouseOver.svg")
    //     }
    // })
    // $(".img_bu").mouseout(function(){
    //     let me = $(this)
    //     let a = me.attr("con")
    //     if(a == 0){
    //         me.attr("src","../Img/select_by_age/u251.svg")
    //     }
    // })

});