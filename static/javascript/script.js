document
  .getElementById("upload-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(this);

    fetch("/upload", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((jsonData) => {
        // Handle the JSON response directly
        const resultDiv = document.getElementById("result");
        resultDiv.innerHTML = ""; // Clear any previous results

        jsonData.forEach((item) => {
          const { label, box, score } = item;
          const [x, y, width, height] = box;

          // Create and append result details
          const resultItem = document.createElement("div");
          resultItem.className = "result-item";
          resultItem.innerHTML = `
          <p><strong>Label:</strong> ${label}</p>
          <p><strong>Box:</strong> [${x}, ${y}, ${width}, ${height}]</p>
          <p><strong>Score:</strong> ${score}</p>
        `;
          resultDiv.appendChild(resultItem);
        });
      })
      .catch((error) => console.error("Error:", error));
  });
