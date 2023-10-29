let barcodeValue = '';
let responseData;
let packId;

function getCSRFToken() {
  const cookieValue = document.cookie
    .split('; ')
    .find(cookie => cookie.startsWith('csrftoken='));
  return cookieValue ? cookieValue.split('=')[1] : null;
}
// pack_script.js

async function sendBarcodeValue(value) {
  const url = '/packaging/api/scan/'; // Замените на свой URL
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
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    if (responseData.is_status === 1) {
        packId = responseData.pack_Info.id;
        window.location.href = `/packaging/${packId}/`;
      } else {
      // Код для случая '0'
      }
  } catch (error) {
    console.error('Error:', error);
  }
}


document.addEventListener('keypress', async function(event) {
  const keyCode = event.keyCode || event.which;

  barcodeValue += String.fromCharCode(keyCode);

  if (keyCode === 13) {
    if (barcodeValue.trim() !== '') {
      console.log('barcodeValue', barcodeValue);
      await sendBarcodeValue(barcodeValue.trim());
      barcodeValue = '';
    }
  }
});
