const currentLocation = location.href;
const categoryItem = document.querySelectorAll('.category-name');
const categoryLen = categoryItem.length;
for (let i = 0; i < categoryLen; ++i) {
    if (categoryItem[i].href === currentLocation) {
        categoryItem[i].className = "active-category";
    }
}