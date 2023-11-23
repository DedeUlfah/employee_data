function submitForm() {
    var form = document.getElementById('uploadForm');
    var formData = new FormData(form);
  
    fetch('/proses_upload', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      // Mengarahkan ke halaman baru dengan menyertakan hasil prediksi sebagai parameter URL
      window.location.href = '/hasil?result=' + encodeURIComponent(data.result);
    })
    .catch(error => console.error('Error:', error));
  }
  
  // Mencegah perilaku pengiriman formulir bawaan
  document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();
    submitForm();
  });
  