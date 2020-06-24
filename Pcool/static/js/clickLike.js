
$(document).on('click','.icon-manitaArriba', function(){
    var elemento = $(this)[0];
    var id = elemento.getAttribute('id');
    var ids = id.toString();
    var likes = $('#likes'+ids).text();
    $.get("/addLike", {id,likes}, (response)=>{
        var d = JSON.parse(response);
        $('#likes'+d.id).text(d.likes);
    })
});

$('#btn').click(()=>{
    swal({
        icon:"warning",
        text:"seguro quieres borrar este dato",
        buttons:true,
    }).then((r)=>{
        if(r){
            swal("listo","","success");
        }else{
            swal("Error","","error");
        }
    });
});