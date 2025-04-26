// scripts.js
document.addEventListener("DOMContentLoaded", function () {
    const uploadBox = document.getElementById("upload-box");
    const selectButton = document.getElementById("select-file-btn");
  
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
        // TODO: Send to backend or display preview
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
      // TODO: Send to backend or display preview
    });
  });
  