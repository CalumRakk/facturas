

$(document).ready(function () {
    // CON ESTABLECER LOS SIGUIENTES VALORES INICIALES TODO LO SIGUIENTE DEBERIA FUNCIONAR
    var options = {
        valueNames: ['id', 'name', 'price', "maker", "opciones"]
    };
    var products = new List('users', options);
    products.clear();
    removeBtns_selector_name = ".remove-item-btn"
    iva_selector_name = "#id_iva"
    subtotal_selector_name = "#id_subtotal"
    total_selector_name = "#id_total"

    function add_product(data) {
        products.add(data);
        refreshCallbacks();
    };

    function refreshCallbacks() {
        removeBtns = $(removeBtns_selector_name);

        removeBtns.click(function () {
            var itemId = $(this).closest('tr').find('.id').text();
            products.remove('id', itemId);
            calculate_the_totals();
        });
    };

    $('#autocomplete').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.href,
                type: "POST",
                data: JSON.stringify({ query: request.term }),
                headers: {
                    "X-Requested-Type": "autocomplete",
                    "Content-Type": "application/json; charset=utf-8",
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                dataType: "json",
                success: function (data) {
                    response(data);
                }
            });
        },
        minLength: 2,
        select: function (event, ui) {

            console.log(ui)
            add_product(ui.item)
            calculate_the_totals()

        },
        close: function (event, ui) {
            $(this).val("");
        }
    });

    function calculate_the_totals() {
        data = products.items.map(function myFunction(item) { return item.values() });
        iva = $(iva_selector_name)[0].valueAsNumber
        iva_decimal = parseInt(iva) / 100;
        subtotal = data.reduce((acumulado, item) => acumulado + parseFloat(item.price), 0);
        total = (subtotal + (subtotal * iva_decimal)).toFixed(2);

        $(subtotal_selector_name).val(subtotal);
        $(total_selector_name).val(total);
    };


});

