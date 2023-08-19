let barcodeValue = '';
let responseData;
let packId;

function getCSRFToken() {
  const cookieValue = document.cookie
    .split('; ')
    .find(cookie => cookie.startsWith('csrftoken='));
  return cookieValue ? cookieValue.split('=')[1] : null;
}

async function sendBarcodeValue(value) {
  const url = '/marking_codes/api/scan/'; // Замените на свой URL
  const data = { barcodeValue: value };

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
    responseData = await response.json();
    packId = responseData.pack_Info.id;
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    console.log('Barcode value sent successfully.');
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

      window.location.href = `/packaging/${packId}/`; // Редирект на страницу с правильно подставленным packId
    }
  }
});
