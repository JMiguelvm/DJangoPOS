document.addEventListener('DOMContentLoaded', function () {
    var cbProduct = document.querySelectorAll('.cbProduct');
    // Add amount to bill fields
    var button2000 = document.getElementById('button2000');
    var amount2000 = document.getElementById('amount2000');
    
    var button5000 = document.getElementById('button5000');
    var amount5000 = document.getElementById('amount5000');
    
    var button10000 = document.getElementById('button10000');
    var amount10000 = document.getElementById('amount10000');
    
    var button20000 = document.getElementById('button20000');
    var amount20000 = document.getElementById('amount20000');
    
    var button50000 = document.getElementById('button50000');
    var amount50000 = document.getElementById('amount50000');
    
    var button100000 = document.getElementById('button100000');
    var amount100000 = document.getElementById('amount100000');
    
    // Result of money calculated
    var divResult100000 = document.getElementById('divResult100000');
    var result100000 = document.getElementById('result100000');
    
    var divResult50000 = document.getElementById('divResult50000');
    var result50000 = document.getElementById('result50000');
    
    var divResult20000 = document.getElementById('divResult20000');
    var result20000 = document.getElementById('result20000');
    
    var divResult10000 = document.getElementById('divResult10000');
    var result10000 = document.getElementById('result10000');
    
    var divResult5000 = document.getElementById('divResult5000');
    var result5000 = document.getElementById('result5000');
    
    var divResult2000 = document.getElementById('divResult2000');
    var result2000 = document.getElementById('result2000');
    
    var divResult1000 = document.getElementById('divResult1000');
    var result1000 = document.getElementById('result1000');
    
    var divResult500 = document.getElementById('divResult500');
    var result500 = document.getElementById('result500');
    
    var divResult200 = document.getElementById('divResult200');
    var result200 = document.getElementById('result200');
    
    var divResult100 = document.getElementById('divResult100');
    var result100 = document.getElementById('result100');
    
    var divResult50 = document.getElementById('divResult50');
    var result50 = document.getElementById('result50');
    
    var inputMAmount = document.getElementById('inputMAmount');
    var calcAmountDiv = document.getElementById('calcAmountDiv');
    var calculationButton = document.getElementById('calculationButton');
    var calcAmountDivIns = document.getElementById('calcAmountDivIns');
    var reloadButton = document.getElementById('reloadButton');
    var saleProducts = document.getElementById('saleProducts');
    
    const formatter = new Intl.NumberFormat('de-DE', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    });
    
    var formDraft = document.getElementById('saveAsDraft');
    var formPublish = document.getElementById('saveAsPublish');

    // Search
    var searchButton = document.getElementById('searchButton');
    var searchInput = document.getElementById('searchInput');
    var products = document.querySelectorAll('.productItem');
    var productDivs = document.querySelectorAll('.productDiv');
    var productList = [-1];
    
    searchButton.addEventListener('click', function () {
        let input = searchInput.value.toLowerCase();
        for (let i = 0; i < products.length; i++) {
            let productName = products[i].innerHTML.toLowerCase();
            let productActive = productDivs[i].getAttribute('data-active');
            if (productName.includes(input) && productActive === '1') {
                productDivs[i].style.display = 'flex';
            }
            else {
                productDivs[i].style.display = 'none';
            }
        }
    });
    
    // Select Category
    
    var categoryList = document.querySelectorAll('.categoryLabel');
    var categoryAll = document.getElementById('categoryAll');
    
    function selectCategory(category) {
        let actualCategory = category.getAttribute('data-category');
        for (let i = 0; i < productDivs.length; i++) {
            let productCategory = productDivs[i].getAttribute('data-category');
            if (actualCategory === productCategory) {
                productDivs[i].style.display = 'flex';
                productDivs[i].setAttribute('data-active', '1')
            }
            else {
                productDivs[i].style.display = 'none';
                productDivs[i].setAttribute('data-active', '0')
            }
        }
    }
    
    categoryList.forEach(category => {
        category.addEventListener('click', function () {
            selectCategory(category);
        });
    })
    
    categoryAll.addEventListener('click', function () {
        for (let i = 0; i < productDivs.length; i++) {
            productDivs[i].style.display = 'flex';
            productDivs[i].setAttribute('data-active', '1');
        }
    })
    // -----------
    
    // Add and Reduce product amount
    
    function loadActualOrder() {
        let unitPrice = document.querySelectorAll('.pUnitCount');
        let totalPrice = document.querySelectorAll('.pTotalCount');
        for (let i = 0; i < unitPrice.length; i++) {
            let unit = parseFloat(unitPrice[i].textContent.replace(',', '.'));
            let total = parseFloat(totalPrice[i].textContent.replace(',', '.'));
            unitPrice[i].textContent = formatter.format(unit);
            totalPrice[i].textContent = formatter.format(total);
        }
    }
    
    loadActualOrder();
    
    function updateTotalCount(id, price) {
        let tCount = document.getElementById(`pTotalCount${id}`);
        let count = document.getElementById(`pCount${id}`);
        let number = parseInt(price)*count.value;
        tCount.textContent = formatter.format(number);
        tCount.setAttribute('data-price', number);
        let addOrder = document.querySelectorAll('.addOrder');
        addOrder.forEach(addButton => {
            addButton.disabled = count ? false : true;
        })
        calculateTotalOrder()
    }
    
    function calculateTotalOrder() {
        let productItem = document.querySelectorAll('.pTotalCount');
        let totalSale = document.getElementById('totalSale');
        let inputMAmount = document.getElementById('inputMAmount');
        let debt = document.getElementById('debt');
        totalSale.setAttribute('data-price', 0);
        for (let i = 0; i < productItem.length; i++) {
            actualAmount = productItem[i].getAttribute('data-price').replace(',', '.');
            function formatToThreeDecimals(num) {
                return Number(num).toFixed(3);
            }
            tContent = Number(totalSale.getAttribute('data-price'));
            aAmount = Number(actualAmount);
            tSale = tContent + aAmount;
            console.log(actualAmount)
            totalSale.setAttribute('data-price', tSale);
            if (tSale < 1000) {
                totalSale.textContent = tSale;
            }
            else {
                totalSale.textContent = formatToThreeDecimals(tSale/1000);
            }
            inputMAmount.textContent = Math.floor(tSale);
            debt.value = Math.floor(tSale);
        }
    }
    calculateTotalOrder();
    // -------------
    
    
    function handleAddProductClick(event) {
        let countInput = event.target.closest('.input-group').querySelector('.saleProductCount');
        let actualId = countInput.getAttribute('data-id');
        let actualPrice = countInput.getAttribute('data-price');
        let actualCount = Number(countInput.value);
        actualCount++;
        countInput.value = actualCount;
        updateTotalCount(actualId, actualPrice);
        countInput.setAttribute('value', `${actualCount}`);
    }
    
    // Función para manejar el clic en el botón de reducir
    function handleReduceProductClick(event) {
        let countInput = event.target.closest('.input-group').querySelector('.saleProductCount');
        let actualId = countInput.getAttribute('data-id');
        let actualPrice = countInput.getAttribute('data-price');
        let actualCount = parseInt(countInput.value, 10);
        if (actualCount > 0) {
            actualCount--;
        }
        countInput.value = actualCount;
        updateTotalCount(actualId, actualPrice);
        countInput.setAttribute('value', `${actualCount}`);
    }
    
    // Función para asignar los event listeners
    function setupProductEventListeners() {
        // Elimina los event listeners existentes y los añade de nuevo
        document.querySelectorAll('.saleProductAdd').forEach(button => {
            button.removeEventListener('click', handleAddProductClick);
            button.addEventListener('click', handleAddProductClick);
        });
    
        document.querySelectorAll('.saleProductReduce').forEach(button => {
            button.removeEventListener('click', handleReduceProductClick);
            button.addEventListener('click', handleReduceProductClick);
        });
    }
    
    
    setupProductEventListeners();
    
    window.addProduct = function(id, pname, pprice) {
        let productInList;
        let pid = id;
        let name = pname;
        let price = pprice;


        for (let i = 0; i < productList.length; i++) {
            if (productList[i] == pid) {productInList = true; break;}
        }
        if (productInList == true) {
            let count = document.getElementById(`pCount${pid}`);
            let num = parseInt(count.value);
            num++;
            count.value = num;
            count.setAttribute('value', `${num}`);
            updateTotalCount(pid, price);
        }
        
        else {
            let product = `
            <div class="row card-header m-0 productItem">
                <div class="col-8">
                    <div class="pos-product-thumb">
                        <div class="info">
                            <div class="title">${name}</div>
                            <div class="single-price">$<span>${price}</span></div>
                            <div class="input-group qty">
                                <div class="input-group-append">
                                    <button class="saleProductReduce btn btn-default" id="saleProductReduce${pid}"><i class="fa fa-minus"></i></button>
                                </div>
                                <input type="number" class="form-control saleProductCount" data-id="${pid}" data-name="${name}" data-price="${price}" id="pCount${pid}" value="1" disabled>
                                <div class="input-group-prepend">
                                    <button class="saleProductAdd btn btn-default" id="saleProductAdd${pid}"><i class="fa fa-plus"></i></button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-4 total-price align-content-center fs-4">$<span class="pTotalCount" id="pTotalCount${pid}"></span></div>
            </div>
            `;
            saleProducts.innerHTML = product + saleProducts.innerHTML;
            productList.push(pid);
            updateTotalCount(pid, price);
            setupProductEventListeners();
        }
    }

    cbProduct.forEach(checkbox => {
        checkbox.addEventListener('click', function () {
            setTimeout(function () {
                checkbox.checked = false;
            }, 400);
            addProduct(checkbox.getAttribute('data-id'),
            checkbox.getAttribute('data-name'),
            checkbox.getAttribute('data-price')
        )
        })
    });
    
    
    
    
    reloadButton.addEventListener('click', function () {
        let elements = [
            [result100000, divResult100000, amount100000],
            [result50000, divResult50000, amount50000],
            [result20000, divResult20000, amount20000],
            [result10000, divResult10000, amount10000],
            [result5000, divResult5000, amount5000],
            [result2000, divResult2000, amount2000],
            [result1000, divResult1000],
            [result500, divResult500],
            [result200, divResult200],
            [result100, divResult100],
            [result50, divResult50]
        ];
        elements.forEach(element => {
            element[0].innerHTML = 0;
            element[1].style.display = 'none';
            if (element[2]) {
                element[2].innerHTML = 0;
            }
        })
        calcAmountDiv.style.display = 'none';
        calcAmountDivIns.style.display = 'none';
    })
    
    
    function addMAmount(button, span) {
        button.addEventListener("click", function () {
            let actualNumber = Number(span.innerHTML);
            console.log(span.innerHTML);
            actualNumber++;
            span.innerHTML = actualNumber;
        })
    }
    
    calculationButton.addEventListener('click', function () {
        let money = [
            [100000, divResult100000, result100000, Number(amount100000.innerHTML)],
            [50000, divResult50000, result50000, Number(amount50000.innerHTML)],
            [20000, divResult20000, result20000, Number(amount20000.innerHTML)],
            [10000, divResult10000, result10000, Number(amount10000.innerHTML)],
            [5000, divResult5000, result5000, Number(amount5000.innerHTML)],
            [2000, divResult2000, result2000, Number(amount2000.innerHTML)],
            [1000, divResult1000, result1000],
            [500, divResult500, result500],
            [200, divResult200, result200],
            [100, divResult100, result100],
            [50, divResult50, result50]
        ];
    
        let amountToPay = Number(inputMAmount.innerHTML);
        let amountToReturn = amountToPay;
        for (let i = 0; i < 6; i++) {
            amountToReturn = amountToReturn - (money[i][3]*money[i][0]);
        }
    
        if (amountToReturn >= 0) {
            calcAmountDivIns.style.display = 'block';
        }
    
        else {
            amountToReturn = Math.abs(amountToReturn);
            console.log('El valor a devolver es: ' + amountToReturn);
            calcAmountDiv.style.display = 'block';
            for (let i = 0; i < money.length; i++) {
                money[i][2].textContent = "0";
                money[i][1].style.display = 'none';
            }
            for (let i = 0; i < money.length; i++) {
                if ((amountToReturn - money[i][0]) >= 0) {
                    amountToReturn -= money[i][0];
                    money[i][1].style.display = 'block';
                    let numberOfValuta = Number(money[i][2].innerHTML);
                    numberOfValuta++;
                    money[i][2].innerHTML = numberOfValuta;
                    if (amountToReturn > money[i][0]) {i--;}
                    if (amountToReturn < 50) {
                        break;
                    }
                }
            }
        }
    });
    
    addMAmount(button2000, amount2000);
    addMAmount(button5000, amount5000);
    addMAmount(button10000, amount10000);
    addMAmount(button20000, amount20000);
    addMAmount(button50000, amount50000);
    addMAmount(button100000, amount100000);
    if (1 == 1) {
        var toastElList = [].slice.call(document.querySelectorAll('.toast'))
        var toastList = toastElList.map(function(toastEl) {
            return new bootstrap.Toast(toastEl)
        })
        toastList.forEach(toast => toast.show()) 
    }
    
    function saveProducts() {
        let inputs = document.querySelectorAll('.saleProductCount');
        let nInputs = 0;
        let output = '';
        for (let input of inputs) {
            output += `<input type="hidden" name="p${nInputs}" value="${input.getAttribute('data-id')}"></input>`;
            output += `<input type="hidden" name="q${nInputs}" value="${input.value}"></input>`;
            nInputs++;
        }
        output += `<input type="hidden" name="nInputs" value="${nInputs}"></input>`;
        return output;
    }
    
    
    
    formDraft.addEventListener('submit', function(event){
        event.preventDefault();
        formDraft.innerHTML = saveProducts() + formDraft.innerHTML;
        formDraft.submit();
    })
    
    formPublish.addEventListener('submit', function(event){
        event.preventDefault();
        formPublish.innerHTML = saveProducts() + formPublish.innerHTML;
        formPublish.submit();
    })
    
    var clientAddDebt = document.getElementById('selectCustomer');

    clientAddDebt.addEventListener('change', function(){
        let debt = document.getElementById('cDebt');
        if (debt) {
            debt.value = clientAddDebt.options[clientAddDebt.selectedIndex].value
        }
        else {
            formPublish.innerHTML = `<input type="hidden" id="cDebt" name="customer" value="${clientAddDebt.options[clientAddDebt.selectedIndex].value}"></input>` + formPublish.innerHTML
        }
    })

    var debtClient = document.getElementById('debtClient');
    var selectCustomer = document.getElementById('selectCustomer');
    debtClient.addEventListener('change', function(){
        selectCustomer.style.display = this.checked ? 'block' : 'none';
    });
    
    var barCode = document.getElementById('barCode');
    var bar_code_input = document.getElementById('bar_code_input');
    barCode.addEventListener('change', function(){
        bar_code_input.style.display = this.checked ? 'block' : 'none';
        if (bar_code_input.style.display == 'block') {
            bar_code_input.focus();
        }
    });
});

