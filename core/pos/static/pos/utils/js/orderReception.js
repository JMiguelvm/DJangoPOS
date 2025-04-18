const btn = document.createElement("button");
btn.id = "btne";
btn.textContent = "hola";
btn.classList = "btn btn-success";
// Name of fields, an input array; Element where table will display; URL for AJAX query
function createTable (n_fields, element, ajax) {
    const table = document.createElement("table");
    table.classList = "display compact"
    table.style.width = "100%";
    const tr = document.createElement("tr");
    // Write the title fields of the table
    n_fields.forEach(element => {
        const th = document.createElement("th");
        th.textContent = element;
        tr.append(th);
    });
    const thead = document.createElement("thead");
    const tfoot = document.createElement("tfoot");
    const tbody = document.createElement("tbody");
    thead.appendChild(tr.cloneNode(true));
    table.appendChild(thead);
    table.appendChild(tbody);
    element.append(table);
    let dt = new DataTable(table, {
        ajax: ajax,
        lengthChange: false,
        pageLength: 5, 
        info: false,
        paging: true,
        searching: true,
        responsive: true,
        columnDefs: [
            { visible: false, targets: 0 },
            { className: 'pointer', targets: "_all" }
        ]
    });
    // Usuful to get data form dt
    return dt
}
$("#test").click(function () { 
    dialog = $.confirm({
        title: 'Confirm!',
        content: 'Hola',
        onContentReady: function () {
            dt = createTable (["id", "name", "numberPhone"], this.$content[0], '/pos/get_vendor')
            dt.on('click', 'tbody tr', function () { 
                let data = dt.row(this).data();
                let context = {id: dt.row(this).data()[0] /*ID form VENDOR ROW*/}
                $.ajax({
                    type: "POST",
                    url: "/pos/get_products",
                    contentType: 'aplication/json',
                    data: JSON.stringify(context),
                    headers: {'X-CSRFTOKEN': CSRF_TOKEN},
                    success: function (response) {
                        console.log('success', response)
                    }
                });
                dialog.close()
            });
        },
        buttons: {
            cancelar: function () {
            }
        }
    });
});


