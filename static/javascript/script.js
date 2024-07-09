document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const imageInput = document.getElementById('image');
    const textInput = document.getElementById('text').value;
    
    const reader = new FileReader();
    reader.onload = function(e) {
      document.getElementById('result-image').src = e.target.result;
      document.getElementById('result-image').style.display = 'block';
    };
    reader.readAsDataURL(imageInput.files[0]);
  
    document.getElementById('result-text').textContent = textInput;
  });
  