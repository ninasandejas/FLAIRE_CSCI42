let cropper;
const input = document.getElementById("profile_picture");
const modal = document.getElementById("cropper-modal");
const image = document.getElementById("cropper-image");
const preview = document.getElementById("profile-preview");
const icon = document.getElementById("upload-icon");
const label = document.getElementById("upload-label");

input.addEventListener("change", function (event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      image.src = e.target.result;
      modal.style.display = "block";

      if (cropper) cropper.destroy();
      cropper = new Cropper(image, {
        aspectRatio: 1,
        viewMode: 1,
      });
    };
    reader.readAsDataURL(file);
  }
});

document.getElementById("crop-button").addEventListener("click", function () {
    const canvas = cropper.getCroppedCanvas({ width: 300, height: 300 });
    canvas.toBlob(blob => {
      const file = new File([blob], "profile_picture.jpg", { type: "image/jpeg" });
  
      const dataTransfer = new DataTransfer();
      dataTransfer.items.add(file);
  
      const input = document.getElementById("profile_picture");
      input.files = dataTransfer.files;
  
      const preview = document.getElementById("profile-preview");
      const icon = document.getElementById("upload-icon");
      const modal = document.getElementById("cropper-modal");
  
      const imageURL = URL.createObjectURL(blob);
      preview.src = imageURL;
      preview.style.display = "block";
      icon.style.display = "none";
      modal.style.display = "none";
    });
  });
  

document.getElementById("cancel-crop").addEventListener("click", function () {
  modal.style.display = "none";
  input.value = '';
});