document.getElementById('upload-form').addEventListener('submit', function(event) {
  event.preventDefault();
  const resultDiv = document.getElementById('result-json');
  resultDiv.innerHTML = '<div> Processing... </div>';

  const formData = new FormData(this);
  fetch('/upload', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    resultDiv.innerHTML = '<pre>' + JSON.stringify(data,null,2) + '</pre>';
  })
  .catch(error => {
    console.error('Error:', error);
  });
});

function previewImage(event) {
  const resultDiv = document.getElementById('tempImage');
  resultDiv.innerHTML = ''; // Clear previous content

  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      const img = document.createElement('img');
      img.src = e.target.result;
      img.classList.add('mt-4', 'w-full', 'rounded-lg');
      resultDiv.appendChild(img);
    };
    reader.readAsDataURL(file);
  }
}