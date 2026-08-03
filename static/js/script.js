document.addEventListener("DOMContentLoaded", () => {

    // Sidebar
    window.toggleSidebar = function () {
        document.getElementById("sidebar").classList.toggle("active");
        document.getElementById("overlay").classList.toggle("active");
    };

    // Dropdown
    window.toggleDropdown = function () {
        document.getElementById("userDropdown").classList.toggle("show");
    };

    window.onclick = function (event) {

        if (!event.target.matches(".dropdown-btn")) {

            document.querySelectorAll(".dropdown-content").forEach(dropdown => {
                dropdown.classList.remove("show");
            });

        }

    };

    // Save buttons
    document.querySelectorAll(".save-btn").forEach(button => {

        button.addEventListener("click", function (event) {

            event.preventDefault();
            event.stopPropagation();

            const promptId = this.dataset.promptId;

            fetch(`/save_prompt/${promptId}`, {
                method: "POST"
            })
            .then(response => response.json())
            .then(data => {

                if (data.saved) {
                    this.textContent = "★";
                    this.classList.add("saved");
                }
                else {
                    this.textContent = "☆";
                    this.classList.remove("saved");
                }

            });

        });

    });

});

document.querySelectorAll(".like-btn").forEach(button => {

    button.addEventListener("click", function (event) {

        event.preventDefault();
        event.stopPropagation();

        const promptId = this.dataset.promptId;

        fetch(`/like_prompt/${promptId}`, {
            method: "POST"
        })
        .then(response => response.json())
        .then(data => {

            this.querySelector(".like-count").textContent = data.likes;

            if (data.liked) {
                this.classList.add("liked");
                this.querySelector(".heart").textContent = "❤";
            } else {
                this.classList.remove("liked");
                this.querySelector(".heart").textContent = "♡";
            }

        });

        });

    });