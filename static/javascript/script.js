document.getElementById('upload-form').addEventListener('submit', function(event) {
  event.preventDefault();
  const formData = new FormData(this);
  fetch('/upload', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    const resultDiv = document.getElementById('result-json');
    resultDiv.innerHTML = '<pre>' + JSON.stringify(data,null,2) + '</pre>';
  })
  .catch(error => {
    console.error('Error:', error);
  });
});