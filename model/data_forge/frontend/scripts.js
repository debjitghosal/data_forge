document.addEventListener("DOMContentLoaded", function () {
  const uploadBox = document.getElementById("upload-box");
  const selectButton = document.getElementById("select-file-btn");
  const resultText = document.getElementById("result-text"); // Where the result will be displayed

  // Create hidden file input
  const fileInput = document.createElement("input");
  fileInput.type = "file";
  fileInput.accept = ".png, .jpg, .jpeg";
  fileInput.style.display = "none";
  document.body.appendChild(fileInput);

  // Click Events
  selectButton.addEventListener("click", () => fileInput.click());
  uploadBox.addEventListener("click", () => fileInput.click());

  // File Selected
  fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
      const file = fileInput.files[0];
      alert(`You selected: ${file.name}`);
      uploadFile(file);  // Call function to upload the file
    }
  });

  // Drag & Drop
  uploadBox.addEventListener("dragover", (e) => {
    e.preventDefault();
    uploadBox.classList.add("border-indigo-500");
  });

  uploadBox.addEventListener("dragleave", () => {
    uploadBox.classList.remove("border-indigo-500");
  });

  uploadBox.addEventListener("drop", (e) => {
    e.preventDefault();
    uploadBox.classList.remove("border-indigo-500");
    const file = e.dataTransfer.files[0];
    alert(`You dropped: ${file.name}`);
    uploadFile(file);  // Call function to upload the file
  });

  // Function to upload the image to the Flask backend
  function uploadFile(file) {
    const formData = new FormData();
    formData.append("image", file);

    // 👇 IMPORTANT: Use FULL backend URL here
    fetch("https://data-forge-1nto.onrender.com/predict", {
  method: "POST",
  body: formData,
})

      .then((response) => response.json())  // Assuming the response is in JSON format
      .then((data) => {
        const style = data.style;
        const confidence = data.confidence;
        
        // Display result (or handle error if necessary)
        resultText.innerHTML = `Predicted Style: ${style}<br>Confidence: ${confidence}%`;
      })
      .catch((error) => {
        console.error("Error uploading file:", error);
        resultText.innerHTML = "Error uploading file. Please try again.";
      });
  }
});
