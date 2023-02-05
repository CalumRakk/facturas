

$(document).ready(function () {
    var options = {
        valueNames: ['id','name', 'price', "maker", "opciones"]
    }; 
    var products = new List('users', options);
    products.clear();
    removeBtns_selector_name= ".remove-item-btn"

    
    function add_product(data) {
        products.add(data);
        refreshCallbacks();
    };

    function refreshCallbacks() {
        removeBtns = $(removeBtns_selector_name);
        
        removeBtns.click(function() {
          var itemId = $(this).closest('tr').find('.id').text();
          products.remove('id', itemId);
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

        },
        close: function (event, ui) {
            $(this).val("");
        }
    })

});

