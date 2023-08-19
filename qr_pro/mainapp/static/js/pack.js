const tabs = document.querySelectorAll('.pack-tab__btns>.btn');
const all_content = document.querySelectorAll('.pack-content');
console.log(tabs)
tabs.forEach((tab, index) => {
    tab.addEventListener('click', (e)=>{
        tabs.forEach(tab=>{tab.classList.remove('active')})
        tab.classList.add('active');

        all_content.forEach(content=>{content.classList.remove('active')});
    all_content[index].classList.add('active');
    })

    
})


const tabs2 = document.querySelectorAll('.pack-tab__property-btns>.btn');
const all_content2 = document.querySelectorAll('.property-content');
console.log(tabs2)
tabs2.forEach((tab, index) => {
    tab.addEventListener('click', (e)=>{
        tabs2.forEach(tab=>{tab.classList.remove('active')})
        tab.classList.add('active');

        all_content2.forEach(content=>{content.classList.remove('active')});
    all_content2[index].classList.add('active');
    })

    
})
// end of tabs

// the beginnig of tables

const headingsKm = document.querySelectorAll('.pack-tab__km .orders-table__item-head');
const iconKm = document.querySelectorAll('.pack-tab__km .print-icon')
headingsKm.forEach((heading, index) => {
    heading.addEventListener('click', (e)=>{
        headingsKm.forEach(heading=>{heading.classList.remove('active')})
        heading.classList.add('active');
        iconKm.forEach(content=>{content.classList.remove('active')});
        iconKm[index].classList.add('active');
    })
})


const headingsPacking = document.querySelectorAll('.pack-tab__packing .orders-table__item-head');
const iconPacking = document.querySelectorAll('.pack-tab__packing .print-icon')
headingsPacking.forEach((heading, index) => {
    heading.addEventListener('click', (e)=>{
        headingsPacking.forEach(heading=>{heading.classList.remove('active')})
        heading.classList.add('active');
        iconPacking.forEach(content=>{content.classList.remove('active')});
        iconPacking[index].classList.add('active');
    })
})

// Свойство table
const headingsPropAll = document.querySelectorAll('.property-all .orders-table__item-head');
const iconPropAll = document.querySelectorAll('.property-all .print-icon')
headingsPropAll.forEach((heading, index) => {
    heading.addEventListener('click', (e)=>{
        headingsPropAll.forEach(heading=>{heading.classList.remove('active')})
        heading.classList.add('active');
        iconPropAll.forEach(content=>{content.classList.remove('active')});
        iconPropAll[index].classList.add('active');
    })
})

const headingsPropOperation = document.querySelectorAll('.property-operation .orders-table__item-head');
const iconPropOperation = document.querySelectorAll('.property-operation .print-icon')
headingsPropOperation.forEach((heading, index) => {
    heading.addEventListener('click', (e)=>{
        headingsPropOperation.forEach(heading=>{heading.classList.remove('active')})
        heading.classList.add('active');
        iconPropOperation.forEach(content=>{content.classList.remove('active')});
        iconPropOperation[index].classList.add('active');
    })
})

const headingsPropDocs = document.querySelectorAll('.property-document .orders-table__item-head');
const iconPropDocs = document.querySelectorAll('.property-document .print-icon')
headingsPropDocs.forEach((heading, index) => {
    heading.addEventListener('click', (e)=>{
        headingsPropDocs.forEach(heading=>{heading.classList.remove('active')})
        heading.classList.add('active');
        iconPropDocs.forEach(content=>{content.classList.remove('active')});
        iconPropDocs[index].classList.add('active');
    })
})

let barcodeValue = '';
let scanCount;

function getCSRFToken() {
  const cookieValue = document.cookie
    .split('; ')
    .find(cookie => cookie.startsWith('csrftoken='));
  return cookieValue ? cookieValue.split('=')[1] : null;
}

function highlightRows(value) {
    var cells = document.querySelectorAll('.pack-tab__table .SGTIN');
    cells.forEach(function(cell) {
        var cleanedValue = value.replace(/[()\s]/g, "");
        if (cell.textContent === cleanedValue) {
            var row = cell.closest('tr');
            if (row) {
                row.classList.add('bg-green');

                var statusCell = row.querySelector('.status');
                if (statusCell) {
                    statusCell.textContent = 'Отсканировано'; // Изменение текста
                }
            }
        }
    });
}


function updateDifference(value, newDifference) {
    var ssccCells = document.querySelectorAll('.pack-tab__table .sscc');

    ssccCells.forEach(function(cell) {
        var cleanedValue = value.replace(/[()\s]/g, "");
        if (cell.textContent === cleanedValue) {
            var row = cell.closest('tr');
            if (row) {
                var differenceCell = row.querySelector('.difference span');
                if (differenceCell) {
                    differenceCell.textContent = newDifference;

                    if (parseInt(newDifference) === 0) {
                        row.classList.add('bg-green');
                    }
                }
            }
        }
    });
}


async function sendBarcodeValue(value) {
  const url = '/pro/packaging/api/scan/'; // Замените на свой URL

  const packInfoElement = document.getElementById('packInfo');
  const pack_id = packInfoElement.textContent;
  const data = { pack_id:pack_id, barcodeValue: value };

  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json', // Указываем тип передаваемых данных (JSON)
      'X-CSRFToken': getCSRFToken(),
    },
    body: JSON.stringify(data),
  };

  try {
    const response = await fetch(url, options);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const responseData = await response.json();
    updateScanCount(responseData.Scan_count); // Обновляем значение Scan_count на странице
    highlightRows(value)
    updateDifference(pack_id, responseData.New_difference)
  } catch (error) {
    console.error('Error:', error);
  }
}


function updateScanCount(newScanCount) {
  scanCount = newScanCount; // Обновляем значение Scan_count
  const scanCountElement = document.querySelector('.section-number.bg-orange');
  scanCountElement.textContent = scanCount; // Обновляем значение на странице
}

document.addEventListener('keypress', async function(event) {
  const keyCode = event.keyCode || event.which;

  barcodeValue += String.fromCharCode(keyCode); // Добавляем символ к barcodeValue при каждом нажатии клавиши

  if (keyCode === 13) { // 13 соответствует клавише Enter
    if (barcodeValue.trim() !== '') {
      await sendBarcodeValue(barcodeValue.trim()); // Отправляем значение штрих-кода без лишних пробелов
      barcodeValue = ''; // Сброс значения штрих-кода после отправки
    }
  }
});
