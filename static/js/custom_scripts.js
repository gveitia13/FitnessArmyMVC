const productModal = document.querySelector('#product_modal')
// const productModal2 = new bootstrap.Modal(document.getElementById('product_modal'));
/*const titleTarget = document.querySelector('#on-off')
let setOnline = () => {
    titleTarget.innerHTML = `<i class="mdi mdi-wifi"></i> Online</span`
    titleTarget.style.color = '#198754'
  },
  setOffline = () => {
    titleTarget.innerHTML = `<i class="mdi mdi-wifi-off"></i> Offline</span`
    titleTarget.style.color = '#dc3545'
  }
if (window.navigator.onLine)
  setOnline()
else
  setOffline()*/
/*window.addEventListener('online', () => setOnline())
window.addEventListener('offline', () => setOffline())*/

//Auxiliary method: submit with ajax and jQuery
function ajaxFunction(url, parameters, type, callback, async = true) {
  $.ajax({
    url: url,
    type: type,
    data: parameters,
    dataType: 'json',
    processData: false,
    contentType: false,
    async: async
  })
    .done(function (data) {
      // callback(data)
      if (!data.hasOwnProperty('error')) {
        callback(data)
        return false
      } else {
        console.log(data)
        Swal.fire({
          title: 'Error',
          text: data['error'],
          icon: 'error'
        })
      }
    })
    .fail(function (jqXHR, textStatus, errorThrown) {
      alert(textStatus + ': ' + errorThrown)
    })
    .always(function (data) {
      console.log(data)
    })
}

class EasyHTTP {

  // Make an HTTP GET Request
  async get(url) {

    // Awaiting fetch response
    const response = await fetch(url);

    // Awaiting for response.json()
    const resData = await response.json();

    // Returning result data
    return resData;
  }

  // Make an HTTP POST Request
  async post(url, data, token) {

    // Awaiting fetch response and
    // defining method, headers and body
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
        "X-CSRFToken": token
      },
      body: JSON.stringify(data)
    });

    // Awaiting response.json()
    const resData = await response.json();

    // Returning result data
    return resData;
  }
}
