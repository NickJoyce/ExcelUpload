const MarketplaceAddressDates = JSON.parse(document.querySelector("#data").value)

const MarketplaceAddress = Object.keys(MarketplaceAddressDates)

var MarketplaceAddressSelect = document.querySelector("#marketplace_address")
var SupplyDateSelect = document.querySelector("#supply_date")


for (var i in MarketplaceAddress) {
    var option = document.createElement('option');
    let mp_address = MarketplaceAddress[i]
    option.text = mp_address;
    option.value = mp_address;
    MarketplaceAddressSelect.add(option);
    if (i === "0") {
            for (var j in MarketplaceAddressDates[mp_address]){
                var option = document.createElement('option');
                option.text = MarketplaceAddressDates[mp_address][j];
                option.value = MarketplaceAddressDates[mp_address][j];
                SupplyDateSelect.add(option);
            }
        }
}

// событие на клик по селекту
MarketplaceAddressSelect.addEventListener('click', (event) => {
  // индекс элемента селекта на который кликнули
  var ind = MarketplaceAddressSelect.selectedIndex;
  // список элементов селекта с адресами
  var options = MarketplaceAddressSelect.options;
  // очищаем селект с датами
  SupplyDateSelect.innerHTML = ""
  MarketplaceAddressDates[options[ind].text].forEach(function(item, i, arr) {
        var option = document.createElement('option');
        option.text = item;
        option.value = item;
        SupplyDateSelect.add(option);
    });


});