fetch("./data/data.json")
  .then(response => response.json())
  .then(data => {
    const container = document.getElementById("accordionContainer");

    data.forEach((item, index) => {
      const card = document.createElement("div");
      card.classList.add("accordion-item");

      card.innerHTML = `
        <div class="accordion-header">
          ${item.title}
          <span class="icon">+</span>
        </div>
        <div class="accordion-content">
          <p>${item.content}</p>
        </div>
      `;


      card.querySelector(".accordion-header").addEventListener("click", () => {
        const isActive = card.classList.contains("active");

        document.querySelectorAll(".accordion-item")
          .forEach(item => item.classList.remove("active"));

        if (!isActive) {
          card.classList.add("active");
          card.querySelector(".icon").textContent = "-";
        }

        document.querySelectorAll(".accordion-item").forEach(item => {
          const icon = item.querySelector(".icon");
          icon.textContent = item.classList.contains("active") ? "-" : "+";
        });
      });

      container.appendChild(card);
    });
  });
