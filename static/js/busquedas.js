$('#busquedaGeneral').keyup(function () {
    var valorBuscar = $('#busquedaGeneral').val();
    console.log(valorBuscar)
    if (valorBuscar == "")
    {
        window.location.replace('/');
    }else
    {
        $.ajax(
            {
                url:'/busquedaGeneral',
                type:'POST',
                data:{'valorBuscar':valorBuscar},
                dataType:'json',
                success:function (response) {
                    var i;
                    var template = "";
                    var result = JSON.parse(response);
                    for(i=0;i<result.length;i++)
                    {
                        template += `
                        <div class="col-6 col-sm-6 col-md-4 col-lg-3 mt-2 elemento">
                            <div class="card shadow">
                                <div class="card-header bg-white p-0">
                                    <div class="text-center lead small">
                                        <p>${result[i].nombre}</p>
                                    </div>
                                </div>
                                    <div class="card-body pt-2 pb-2" data-toggle="modal" data-target="#exampleModalLong">
                                        <img src='${result[i].imagen}' alt="" class="img-fluid rounded" id='${result[i].id}'>
                                    </div>
                                <div class="card-footer text-center bg-white p-1">
                                    <span class="icon-manitaArriba" id="${result[i].id}" name=""><span id="likes">0</span></span>
                                </div>
                            </div>
                        </div>
                    `;
                    }
                    $('.galeriaBusqueda').html(template);
                }
            }
        );
    }
});