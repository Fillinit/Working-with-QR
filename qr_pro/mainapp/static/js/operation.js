const tabs = document.querySelectorAll('.operation-btns>.btn');
const all_content = document.querySelectorAll('.operation-content');
console.log(tabs)
tabs.forEach((tab, index) => {
    tab.addEventListener('click', (e)=>{
        tabs.forEach(tab=>{tab.classList.remove('active')})
        tab.classList.add('active');

        all_content.forEach(content=>{content.classList.remove('active')});
    all_content[index].classList.add('active');
    })

    
})


const tabs2 = document.querySelectorAll('.svoystvo-btns>.btn');
const all_content2 = document.querySelectorAll('.svoystvo-content');
console.log(tabs2)
tabs2.forEach((tab, index) => {
    tab.addEventListener('click', (e)=>{
        tabs2.forEach(tab=>{tab.classList.remove('active')})
        tab.classList.add('active');

        all_content2.forEach(content=>{content.classList.remove('active')});
    all_content2[index].classList.add('active');
    })

    
})

// Tables
// tab1
const headingsOperationTab = document.querySelectorAll('.operation-tab__km .orders-table__item-head');
const iconOperationTab = document.querySelectorAll('.operation-tab__km .print-icon')
headingsOperationTab.forEach((heading, index) => {
    heading.addEventListener('click', (e)=>{
        headingsOperationTab.forEach(heading=>{heading.classList.remove('active')})
        heading.classList.add('active');
        iconOperationTab.forEach(content=>{content.classList.remove('active')});
        iconOperationTab[index].classList.add('active');
    })
})
// tab2
const headingsUpakovkaTab = document.querySelectorAll('.upakovka-tab__km .orders-table__item-head');
const iconUpakovkaTab = document.querySelectorAll('.upakovka-tab__km .print-icon')
headingsUpakovkaTab.forEach((heading, index) => {
    heading.addEventListener('click', (e)=>{
        headingsUpakovkaTab.forEach(heading=>{heading.classList.remove('active')})
        heading.classList.add('active');
        iconUpakovkaTab.forEach(content=>{content.classList.remove('active')});
        iconUpakovkaTab[index].classList.add('active');
    })
})
// tab 3
const headingsMerchandiseTab = document.querySelectorAll('.merchandise-tab__km .orders-table__item-head');
const iconMerchandiseTab = document.querySelectorAll('.merchandise-tab__km .print-icon')
headingsMerchandiseTab.forEach((heading, index) => {
    heading.addEventListener('click', (e)=>{
        headingsMerchandiseTab.forEach(heading=>{heading.classList.remove('active')})
        heading.classList.add('active');
        iconMerchandiseTab.forEach(content=>{content.classList.remove('active')});
        iconMerchandiseTab[index].classList.add('active');
    })
})
// 4
// 4.1
const headingsSvoystvoTab = document.querySelectorAll('.svoystvo-tab .orders-table__item-head');
const iconSvoystvoTab = document.querySelectorAll('.svoystvo-tab .print-icon')
headingsSvoystvoTab.forEach((heading, index) => {
    heading.addEventListener('click', (e)=>{
        headingsSvoystvoTab.forEach(heading=>{heading.classList.remove('active')})
        heading.classList.add('active');
        iconSvoystvoTab.forEach(content=>{content.classList.remove('active')});
        iconSvoystvoTab[index].classList.add('active');
    })
})
// 4.2
const headingsLastPack = document.querySelectorAll('.lastPack-tab .orders-table__item-head');
const iconLastPack = document.querySelectorAll('.lastPack-tab .print-icon')
headingsLastPack.forEach((heading, index) => {
    heading.addEventListener('click', (e)=>{
        headingsLastPack.forEach(heading=>{heading.classList.remove('active')})
        heading.classList.add('active');
        iconLastPack.forEach(content=>{content.classList.remove('active')});
        iconLastPack[index].classList.add('active');
    })
})
// 4.3
const headingsLastKm = document.querySelectorAll('.lastKm-tab .orders-table__item-head');
const iconLastKm = document.querySelectorAll('.lastKm-tab .print-icon')
headingsLastKm.forEach((heading, index) => {
    heading.addEventListener('click', (e)=>{
        headingsLastKm.forEach(heading=>{heading.classList.remove('active')})
        heading.classList.add('active');
        iconLastKm.forEach(content=>{content.classList.remove('active')});
        iconLastKm[index].classList.add('active');
    })
})
// 4.4
const headingsDogGis = document.querySelectorAll('.docGis-tab .orders-table__item-head');
const iconDogGis = document.querySelectorAll('.docGis-tab .print-icon')
headingsDogGis.forEach((heading, index) => {
    heading.addEventListener('click', (e)=>{
        headingsDogGis.forEach(heading=>{heading.classList.remove('active')})
        heading.classList.add('active');
        iconDogGis.forEach(content=>{content.classList.remove('active')});
        iconDogGis[index].classList.add('active');
    })
})
// 4.5
const headingsShtrixTab = document.querySelectorAll('.shtrix-tab .orders-table__item-head');
const iconShtrixTab = document.querySelectorAll('.shtrix-tab .print-icon')
headingsShtrixTab.forEach((heading, index) => {
    heading.addEventListener('click', (e)=>{
        headingsShtrixTab.forEach(heading=>{heading.classList.remove('active')})
        heading.classList.add('active');
        iconShtrixTab.forEach(content=>{content.classList.remove('active')});
        iconShtrixTab[index].classList.add('active');
    })
})
// 4.6
const headingsKmUpd = document.querySelectorAll('.kmupd-tab .orders-table__item-head');
const iconKmUpd = document.querySelectorAll('.kmupd-tab .print-icon')
headingsKmUpd.forEach((heading, index) => {
    heading.addEventListener('click', (e)=>{
        headingsKmUpd.forEach(heading=>{heading.classList.remove('active')})
        heading.classList.add('active');
        iconKmUpd.forEach(content=>{content.classList.remove('active')});
        iconKmUpd[index].classList.add('active');
    })
})




//tab 5
const headingsUpvTab = document.querySelectorAll('.upv-tab__km .orders-table__item-head');
const iconUpvTab = document.querySelectorAll('.upv-tab__km .print-icon')
headingsUpvTab.forEach((heading, index) => {
    heading.addEventListener('click', (e)=>{
        headingsUpvTab.forEach(heading=>{heading.classList.remove('active')})
        heading.classList.add('active');
        iconUpvTab.forEach(content=>{content.classList.remove('active')});
        iconUpvTab[index].classList.add('active');
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
    console.log(value);
    var cells = document.querySelectorAll('.operation-tab__table .GTIN');
    cells.forEach(function(cell) {
        var cleanedValue = value.replace(/[()\s]/g, "");
        if (cell.textContent === cleanedValue) {
            var row = cell.closest('tr');
            if (row) {
                row.classList.add('bg-green');
            }
        }
    });
}


async function sendBarcodeValue(value) {
  const url = '/operations/api/scan/'; // Замените на свой URL

  const packInfoElement = document.querySelector('.operation-title__numbers span');
  const marking_id = packInfoElement.textContent;
  const data = { marking_id:marking_id, barcodeValue: value };

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
    if (responseData.is_status === 0) {
        console.log('is_status:', responseData.is_status);
    } else if (responseData.is_status === 1) {
        highlightRows(responseData.gtin)
    }
  } catch (error) {
    console.error('Error:', error);
  }
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