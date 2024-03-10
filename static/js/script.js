document.addEventListener("DOMContentLoaded", function () {
  console.log("Content Loaded");
  let element = document.getElementById("div_id_is_combo");
  if (element) {
    element.classList.add("form-switch");
  }

  let is_staff_element = document.getElementById("div_id_is_staff");
  if (is_staff_element) {
    is_staff_element.classList.add("form-switch");
  }
});
