document.addEventListener("DOMContentLoaded", () => {
    const items = document.querySelectorAll(".pyramid-item");
    const revealOptions = {
      threshold: 0.1
    };
  
    const revealOnScroll = new IntersectionObserver(function(entries, observer) {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("revealed");
          observer.unobserve(entry.target);
        }
      });
    }, revealOptions);
  
    items.forEach(item => {
      revealOnScroll.observe(item);
    });
  });
  
  document.addEventListener("mousemove", (e) => {
    const glitter = document.createElement("div");
    glitter.className = "glitter-dot";
    glitter.style.left = `${e.pageX - 3}px`; 
    glitter.style.top = `${e.pageY - 3}px`;  

    
    const container = document.getElementById("glitter-trail-container");
    container.appendChild(glitter);
  
    setTimeout(() => glitter.remove(), 800);
  });
  