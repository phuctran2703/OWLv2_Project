document
  .getElementById("upload-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(this);

    fetch("/upload", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.blob())
      .then((blob) => {
        const url = URL.createObjectURL(blob);
        document.getElementById("result-image").src = url;
        document.getElementById("result-image").style.display = "block";
      })
      .catch((error) => console.error("Error:", error));
  });
