

$(function () {

    var buscarCliente_inputId = "#buscar-cliente-input";
    var buscarCliente_btnId = "#buscar-cliente-button";
    var crearClientr_formId = "#form-crear-cliente"
    var displayCliente = "#display-cliente";

    var client_NotFound_id = "#client_NotFound_id"
    var filtro_tipo_documento_idselect = "#id_tipo_documento"

    var buscarVehiculo_inputId = "#buscar-vehiculo-input";
    var buscarVehiculo_btnId = "#buscar-vehiculo-button";
    var crear_vehiculo_formId = "#crear-vehiculo-form"
    var displayVehiculo = "#display-vehiculo";
    var filtro_tipo_vehiculo_idselect = "#id_tipo_vehiculo"
    var contenedor_VehiculoNotFound = "#contenedor_VehiculoNotFound"

    var procesarTransaccion_formId = "#procesarTransaccion"

    const form_to_object = (formJQuery) => {
        // formJQuery debe ser un objeto jQuery, ejemplo: se deberia pasar así $(this)
        const array = formJQuery.serializeArray();

        let data = {}
        array.reduce(function (obj, item) {
            data[item.name] = item.value;
        }, 0);
        return data
    }

    $(crear_vehiculo_formId).submit(function (event) {
        event.preventDefault();
        data = form_to_object($(this));
        console.log(data);
        Transaccion.add_vehiculo(data)
    })

    $(crearClientr_formId).submit(function (event) {
        event.preventDefault();
        const array = $(this).serializeArray();

        let data = {}
        array.reduce(function (obj, item) {
            data[item.name] = item.value;
        }, 0);

        Transaccion.add_cliente(data);

    })

    $(procesarTransaccion_formId).submit(function (event) {
        event.preventDefault();
        const array = $(this).serializeArray();

        let data = {}
        array.reduce(function (obj, item) {
            data[item.name] = item.value;
        }, 0);

        const merge = Object.assign(data, Transaccion)

        $.ajax({
            url: window.location.href,
            type: "POST",
            data: JSON.stringify(merge),
            headers: {
                "X-Requested-Type": "procesar-transaccion",
                "Content-Type": "application/json; charset=utf-8",
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            success: function (data) {
                alert(JSON.stringify(data))
            },
        });

    })

    const Transaccion = {
        add_cliente: function (data) {
            // Recibe un objeto
            this.cliente = data;
            if ($.isEmptyObject(data) == false) {
                sibling = $(displayCliente).nextAll();
                const nombre = data.nombre + " " + data.apellido
                const documento = data.tipo_documento + ". " + data.num_documento
                sibling[0].innerText = nombre
                sibling[1].innerText = documento
            }
        },
        add_vehiculo: function (data) {
            this.vehiculo = data
            if ($.isEmptyObject(data) == false) {
                const string = data.tipo_vehiculo + " - " + data.placa.toUpperCase()
                $(displayVehiculo).next().text(string);
            }
        }
        add_tramites: function(data){
            this.vehiculo = data
            if ($.isEmptyObject(data) == false) {
                const string = data.tipo_vehiculo + " - " + data.placa.toUpperCase()
                $(displayVehiculo).next().text(string);
            }
        }
    }

    const Messages = {
        is_open: false,
        msg_ClientNotFound: function () {
            if (this.is_open == false) {
                this.is_open = true;
                $(client_NotFound_id).fadeIn().delay(2000).fadeOut(function () {
                    this.is_open = false;
                }.bind(this));
            }
        },
        msg_VehiculoNotFound: function () {
            if (this.is_open == false) {
                this.is_open = true;
                $(contenedor_VehiculoNotFound).fadeIn().delay(2000).fadeOut(function () {
                    this.is_open = false;
                }.bind(this));
            }
        }
    }


    $(buscarCliente_btnId).click(function () {
        const num_documento = $(buscarCliente_inputId).val()
        const tipo_documento = $(filtro_tipo_documento_idselect).val()

        $.ajax({
            url: window.location.href,
            type: "POST",
            data: JSON.stringify({ "num_documento": num_documento, "tipo_documento": tipo_documento }),
            headers: {
                "X-Requested-Type": "buscar-cliente",
                "Content-Type": "application/json; charset=utf-8",
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            success: function (data) {
                if (data.length == 0) {
                    Messages.msg_ClientNotFound()
                    Transaccion.add_cliente({})
                } else {
                    Transaccion.add_cliente(data[0])
                }
            },
        });
    });

    $(buscarVehiculo_btnId).click(function () {
        const tipo_vehiculo = $("#id_tipo_vehiculo").val()
        const placa = $("#id_placa").val()

        $.ajax({
            url: window.location.href,
            type: "POST",
            data: JSON.stringify({ "placa": placa, "tipo_vehiculo": tipo_vehiculo }),
            headers: {
                "X-Requested-Type": "buscar-vehiculo",
                "Content-Type": "application/json; charset=utf-8",
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            success: function (data) {
                if (data.length == 0) {
                    Messages.msg_VehiculoNotFound()
                    Transaccion.add_vehiculo({})
                } else {
                    Transaccion.add_vehiculo(data[0])
                }
            },
        });
    });

    $("#buscarTramite_btnId").click(function () {
        const nombre= $("#id_nombre_tramite").val()
        const registro = $("#id_registro").val()
        const clasificacion = $("#id_tipo_vehiculo").val() // TEMPORAL, SE DEBE CONFIRMAR SI SE HA AÑADIDO UN VEHICULO ANTES DE PERMITIR BUSCAR.
        
        $.ajax({
            url: window.location.href,
            type: "POST",
            data: JSON.stringify({"nombre":nombre, "registro": registro, "clasificacion": clasificacion }),
            headers: {
                "X-Requested-Type": "buscar-tramite",
                "Content-Type": "application/json; charset=utf-8",
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            success: function (data) {
                if (data.length == 0) {
                    Messages.msg_TramiteNotFound()
                    Transaccion.add_tramites([])
                } else {
                    Transaccion.add_tramites(data[0])
                }
            },
        });
    });


});