const currentLocation = location.href;
const categoryItem = document.querySelectorAll('.category-name');
const categoryLen = categoryItem.length;
var select = document.getElementById("select");

for (let i = 0; i < categoryLen; ++i) {
    if (categoryItem[i].href === currentLocation) {
        categoryItem[i].className = "active-category";
        select.options[i+1].selected = true;
    }
}

