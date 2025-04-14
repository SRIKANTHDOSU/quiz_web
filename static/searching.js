document.addEventListener("DOMContentLoaded", () => {
    const input = document.querySelector(".search");
    const buttons = document.querySelectorAll(".concept-btn");
  
    input.addEventListener("input", () => {
      const inputValue = input.value.trim().toLowerCase();
  
      buttons.forEach(button => {
        const text = button.textContent.trim().toLowerCase();
        button.style.display = text.includes(inputValue) ? "" : "none";
      });
    });
  });
  

