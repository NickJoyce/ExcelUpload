var orderWrapper = document.querySelector(".order_wrapper")
var SalesChannelsSelect = document.querySelector("#sales_channel")
var commentToOrder = document.querySelector(".comment_to_order")
var pickupPoint = document.querySelector(".pickup_point")


class DeliveryDataLine {
  constructor(title, input_name) {
    this.title = title;
    this.input_name = input_name;
  }
}

let AddDeliveryBlock = (main, block_before) => {
    let address = new DeliveryDataLine("Адрес доставки:", "address");
    let full_name = new DeliveryDataLine("ФИО:", "full_name");
    let phone = new DeliveryDataLine("Телефон:", "phone");
    lines = [address, full_name, phone]
    lines.forEach(function(item, i, arr) {
        var title_div = document.createElement("h6");
        title_div.textContent = item.title
        title_div.className = "delivery text-start ps-1 mb-2"
        var input_div = document.createElement("input");
        input_div.name = item.input_name
        input_div.className = "delivery form-control mb-3"
        input_div.required = true;
        divs_in_lines = [title_div, input_div]
        divs_in_lines.forEach(function(div, i, arr) {
            main.insertBefore(div, block_before)
        })
    })
}


let DeleteDeliveryBlock = () => {
    let allDeliveryElems = document.querySelectorAll('.delivery')
    if (allDeliveryElems.length == 0) {
    } else {
            allDeliveryElems.forEach(function(elem){
                elem.parentNode.removeChild(elem);
        })
    }
}

var sales_channel_with_additional_fields  = ["Доставка на склад Поставщика", "Деловые линии", "ПЭК", "СДЭК"]



// событие на клик по селекту
SalesChannelsSelect.addEventListener('change', (event) => {
  // индекс элемента селекта на который кликнули
  var ind = SalesChannelsSelect.selectedIndex;
  // список элементов селекта
  var options = SalesChannelsSelect.options;
  if (options[ind].text == "Самовывоз") {
       pickupPoint.style.display = "inline"
       DeleteDeliveryBlock()
    } else if (sales_channel_with_additional_fields.includes(options[ind].text) ) {
        DeleteDeliveryBlock()
        pickupPoint.style.display = "none"
        AddDeliveryBlock(orderWrapper, commentToOrder)
    } else {
        pickupPoint.style.display = "none"
        DeleteDeliveryBlock()
    }
});