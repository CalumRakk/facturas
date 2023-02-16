


var inputSearch_id = "#input-search-cliente"
var btnSearch_id = "#button-search-cliente"
var smallClientNameContainer = "#client-name-container"

const object_message = {
    class_name: "45522145",
    is_open: false,
    get_element: function () {
        const msg_class = "45522145"
        var mensaje = $(`<div class='${msg_class}'>No se encontro resultados</div>`);
        $("body").append(mensaje);
        $(`.${msg_class}`).css({
            "background-color": "yellow",
            "color": "black",
            "font-weight": "bold",
            "padding": "5px",
            "position": "absolute",
        });
        return mensaje
    },
    show: function () {
        if (this.is_open == false) {
            this.is_open = true;
            const inputPos = $(inputSearch_id).position();
            element = this.get_element();
            element.css({
                top: inputPos.top - element.outerHeight() - 5,
                left: inputPos.left
            });
            element.fadeIn().delay(2000).fadeOut(function () {
                this.is_open = false;
                element.remove();
            }.bind(this, element));
        }
    }
}


$(btnSearch_id).click(function () {
    const term = $(inputSearch_id).val()
    $.ajax({
        url: window.location.href,
        type: "POST",
        data: JSON.stringify({ "query": term }),
        headers: {
            "X-Requested-Type": "autocomplete",
            "Content-Type": "application/json; charset=utf-8",
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        success: function (data) {
            if (data.length == 0) {
                object_message.show();
            }

            $("table tbody").empty();

            $.each(data, function (index, element) {
                var new_row = $(`
                <tr id='${element.id}'> 
                    <td class='nombre'>${element.nombre}</td>
                    <td class='tipo_documento'>${element.tipo_documento}</td>
                    <td class'num_documento'>${element.num_documento}</td> 
                    <td>
                        <button class="vincular-btn">Vincular</button>
                        <button class="desvincular-btn">Desvincular</button>
                    </td>
                </tr>
                
                `);
                $("table").append(new_row);

                if (index === data.length - 1) {

                    vincularBtns = $(".vincular-btn");
                    vincularBtns.click(function () {
                        const tr_element = $(this).closest('tr');
                        const tr_id = tr_element.attr("id");
                        const td_name = $(this).closest('tr').find('.nombre').text();
                        console.log(tr_id, td_name);
                        $(smallClientNameContainer).text(td_name);
                        $(smallClientNameContainer).next().val(tr_id)
                    });

                    desvincularBtns = $(".desvincular-btn");
                    desvincularBtns.click(function () {
                        $(smallClientNameContainer).empty();
                        $(smallClientNameContainer).next().val("")
                    });

                }
            });
        },
    });
});
