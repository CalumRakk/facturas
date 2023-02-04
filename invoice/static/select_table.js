


// const selectAll = document.querySelector("#selectAll");
// const selectRows = document.querySelectorAll(".selectRow");


$(".is_modified").change(function () {
    calculate_the_totals();
});

$(".is_selected").click(function () {
    $(this).toggleClass("selected");
    calculate_the_totals();
});

$('#id_iva').on('input', function () {
    if (this.valueAsNumber % 1 !== 0) {
        this.value = this.value.slice(0, -1);
    }
});

function get_selected_products() {
    let products = [];
    $(".selected").each(function (index) {
        products.push($(this).attr("product_id"));
    });

    return products
}

function calculate_the_totals() {
    var data = {
        subtotal: 0,
        iva: $('#id_iva')[0].valueAsNumber,
        total: 0,
        products: [],
        client: $("#id_client").find("option:selected").val()
    };

    data.products = get_selected_products();

    // establezco el valor del subtotal sumando el price de todos los productos seleccionados
    $(".selected").children().each(function () {
        if ($(this).attr("name") == "price") {
            data.subtotal += parseFloat($(this).text());
        }
    });
    // convierto el iva en un decimal
    iva = parseInt(data.iva) / 100;


    data.total = (data.subtotal + (data.subtotal * iva)).toFixed(2);
    data.subtotal= data.subtotal.toFixed(2)

    $('#id_subtotal').val(data.subtotal);
    $('#id_total').val(data.total);

    return data
}


// $('#invoice-create').submit(function(event) {
//   // event.preventDefault();

//   // // Modifica los datos antes de enviarlos
//   // var datos = $('#invoice-create').serialize();
//   // document.getElementById("product_ids").value = JSON.stringify(calculate_the_totals());

//   // $.ajax({
//   //   type: 'POST',
//   //   url: window.location.pathname,
//   //   data: datos,
//   //   success: function(respuesta) {
//   //     console.log('Solicitud enviada con éxito: ', respuesta);
//   //   },
//   //   error: function(error) {
//   //     console.error('Error al enviar la solicitud: ', error);
//   //   }
//   // });
//   event.preventDefault();
//   jsonData=calculate_the_totals()
//   $.ajax({
//     type: "POST",
//     url: window.location.pathname,
//     data: JSON.stringify(jsonData),
//     contentType: "application/json; charset=utf-8",
//     dataType: "json",
//     success: function(data) {
//         console.log(data)
//     }
//   });
// });


// document.getElementById("#invoice-create").addEventListener("submit", function (event) {
//   event.preventDefault();

//   var elements = document.querySelectorAll("tr.selected");
//   var product_ids = [];
//   for (var i = 0; i < elements.length; i++) {
//     product_ids.push(elements[i].getAttribute("product_id"));
//   }
//   document.getElementById("selected_rows").value = JSON.stringify(data);

//   this.submit();

// });
// document.getElementById("#invoice-create").addEventListener("submit", function (event) {
//   event.preventDefault();

//   let data= calculate_the_totals();
//   $('#selected_rows').val(JSON.stringify(data));
//   this.submit();

// });

// $('#invoice-create').submit(function(event) {
//     //   // event.preventDefault();
//     event.preventDefault();

//     let data= calculate_the_totals();
//     $('#selected_rows').val(JSON.stringify(data));
//     this.submit();
// });



// $('#invoice-create').submit(function (event) {
//     event.preventDefault();

//     // Modifica los datos antes de enviarlos
//     let data = calculate_the_totals()
//     const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

//     $.ajax({
//         type: "POST",
//         url: window.location.pathname,
//         headers: { 'X-CSRFToken': csrftoken },
//         data: JSON.stringify(data),
//         dataType: "application/json; charset=UTF-8",
//     }).done(function (data) {
//         window.location.href = "{% url 'invoice_list' %}";
//     })
// });



$('#invoice-create').submit(function (event) {
    event.preventDefault();

    let data = calculate_the_totals()
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    $.ajax({
        type: "POST",
        url: window.location.pathname,
        headers: { 'X-CSRFToken': csrftoken },
        data: JSON.stringify(data),
        dataType: "json",
    }).done(function (data) {
        window.location.href = data.redirect_url;
    })
});
