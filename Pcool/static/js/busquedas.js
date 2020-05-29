//busqueda general de productos
$('#busquedaGeneral').keyup(function () {
    var valorBuscar = $('#busquedaGeneral').val();
    console.log(valorBuscar)
    if (valorBuscar == "")
    {
        $('#tilesTiendas').show(500);
        $('#tileBusquedaGeneral').hide(500);
    }else
    {
        $('#tileBusquedaGeneral').show(500);
        $('#tilesTiendas').hide(500);
        $.ajax(
            {
                url:'/busquedaGeneral',
                data:{'valorBuscar':valorBuscar},
                type:'GET',
                dataType:'json',
                success:function (response) {
                    var i;
                    var template = "";
                    for(i=0;i<response.length;i++)
                    {
                        template += `
                        <div class="col-6 col-sm-6 col-md-4 col-lg-3 mt-2 elemento">
                            <div class="card shadow">
                                <div class="card-header bg-white p-0">
                                    <div class="text-center lead small">
                                        <p>${response[i].nombre}</p>
                                    </div>
                                </div>
                                    <div class="card-body pt-2 pb-2 imgP" data-toggle="modal" data-target="#exampleModalLong">
                                        <img src='${response[i].imagen}' alt="" class="img-fluid rounded" id='${response[i].id}'>
                                    </div>
                                <div class="card-footer text-center bg-white p-1">
                                    <span class="icon-manitaArriba" id="${response[i].id}" name="${response[i].likes}"><span id="likes">${response[i].likes}</span></span>
                                </div>
                            </div>
                        </div>
                    `;
                    }
                    $('#tileBusquedaGeneral').html(template);
                }
            }
        );
    }
});
