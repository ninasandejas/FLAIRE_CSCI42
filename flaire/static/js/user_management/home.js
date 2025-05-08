
  
  document.addEventListener("DOMContentLoaded", () => {
    for (let i = 0; i < 15; i++) {
      setTimeout(() => {
        const bubble = document.createElement("div");
        bubble.classList.add("heart-bubble");
        bubble.style.left = `${Math.random() * 100}vw`;
        bubble.style.backgroundColor = ["#f7c1d9", "#ffc1e3", "#fce4ec", "#e5a0bb"][Math.floor(Math.random() * 4)];
        document.body.appendChild(bubble);
        bubble.addEventListener("animationend", () => bubble.remove());
      }, i * 120);
    }
  });
  