const tabs = document.querySelectorAll('.content-bar__btns>.btn');
const all_content = document.querySelectorAll('.content-bar__item');
tabs.forEach((tab, index) => {
    tab.addEventListener('click', (e)=>{
        tabs.forEach(tab=>{tab.classList.remove('active')})
        tab.classList.add('active');

        all_content.forEach(content=>{content.classList.remove('active')});
    all_content[index].classList.add('active');
    })

    
})


const headingsPrint = document.querySelectorAll('.content-bar__items-print .orders-table__item-head');
const iconPrint = document.querySelectorAll('.content-bar__items-print .print-icon')
headingsPrint.forEach((heading, index) => {
    heading.addEventListener('click', (e)=>{
        headingsPrint.forEach(heading=>{heading.classList.remove('active')})
        heading.classList.add('active');
        iconPrint.forEach(content=>{content.classList.remove('active')});
        iconPrint[index].classList.add('active');
    })
})


const headingsPack = document.querySelectorAll('.content-bar__items-pack .orders-table__item-head');
const iconPack = document.querySelectorAll('.content-bar__items-pack .print-icon')
headingsPack.forEach((heading, index) => {
    heading.addEventListener('click', (e)=>{
        headingsPack.forEach(heading=>{heading.classList.remove('active')})
        heading.classList.add('active');
        iconPack.forEach(content=>{content.classList.remove('active')});
        iconPack[index].classList.add('active');
    })
})


const headingsMaster = document.querySelectorAll('.content-bar__items-master .orders-table__item-head');
const iconMaster = document.querySelectorAll('.content-bar__items-master .print-icon')
headingsMaster.forEach((heading, index) => {
    heading.addEventListener('click', (e)=>{
        headingsMaster.forEach(heading=>{heading.classList.remove('active')})
        heading.classList.add('active');
        iconMaster.forEach(content=>{content.classList.remove('active')});
        iconMaster[index].classList.add('active');
    })
})




function setupCheckboxListeners(checkboxClass, hiddenInputId, displayId) {
    const checkboxes = document.querySelectorAll(checkboxClass);

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            updateHiddenInput(checkboxes, hiddenInputId, displayId);
        });
    });
}

function updateHiddenInput(checkboxes, hiddenInputId, displayId) {
    const selectedValues = Array.from(checkboxes)
        .filter(checkbox => checkbox.checked)
        .map(checkbox => checkbox.getAttribute('value'))
        .join(',');

    const hiddenInput = document.getElementById(hiddenInputId);
    hiddenInput.value = selectedValues;

    const selectedValuesDisplay = document.getElementById(displayId);
    selectedValuesDisplay.textContent = selectedValues;
}

// Использование для первого набора
setupCheckboxListeners('.checkbox-select', 'selected-checkboxes', 'selected-values-display');

// Использование для второго набора
setupCheckboxListeners('.checkbox-select_2', 'selected-checkboxes_2', 'selected-values-display_2');

// Использование для третьего набора
setupCheckboxListeners('.checkbox-select_3', 'selected-checkboxes_3', 'selected-values-display_3');


