document.getElementById("upload-form").addEventListener("submit", function (event) {
  event.preventDefault();

  const formData = new FormData(this);

  fetch("/upload", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      const imageUrl = data.image_url;
      const jsonUrl = data.json_url;

      // Fetch the JSON data
      fetch(jsonUrl)
        .then(response => response.json())
        .then(jsonData => {
          // Load the image and draw annotations
          const img = new Image();
          img.src = imageUrl;
          img.onload = () => {
            const canvas = document.createElement("canvas");
            const context = canvas.getContext("2d");

            canvas.width = img.width;
            canvas.height = img.height;
            context.drawImage(img, 0, 0);

            jsonData.forEach(item => {
              const { label, box, score } = item;
              const [x, y, width, height] = box;

              // Draw the bounding box
              context.strokeStyle = "green";
              context.lineWidth = 3;
              context.strokeRect(x, y, width - x, height - y);

              // Draw the label and score
              context.fillStyle = "yellow";
              context.font = "16px Arial";
              context.fillText(`${label}: ${score}`, x, y - 10);
            });

            // Display the annotated image
            const resultImage = document.getElementById("result-image");
            resultImage.src = canvas.toDataURL();
            resultImage.style.display = "block";
          };
        });
    })
    .catch((error) => console.error("Error:", error));
});
