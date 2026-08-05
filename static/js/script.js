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

    // Save button
    document.querySelectorAll(".save-btn").forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            event.stopPropagation();
            const promptId = this.dataset.promptId;

            fetch(`/save_prompt/${promptId}`, {
                method: "POST"
            })

            .then(response => {
                if (!response.ok) {
                    return response.json();
                }
                return response.json();
            })

            .then(data => {
                if (data.error) {
                    showToast(data.error);
                    return;
                }

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

    // Like button
    document.querySelectorAll(".like-btn").forEach(button => {
    button.addEventListener("click", function (event) {
        event.preventDefault();
        event.stopPropagation();
        const promptId = this.dataset.promptId;
        fetch(`/like_prompt/${promptId}`, {
            method: "POST"
        })

        .then(response => {
            if (!response.ok) {
                return response.json();
            }
            return response.json();
        })
        
        .then(data => {
            if (data.error) {
                showToast(data.error);
                return;
            }

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
});

let toastTimer;

function showToast(message) {
    const toast = document.getElementById("toast");
    clearTimeout(toastTimer);
    toast.textContent = message;
    toast.classList.add("show");
    toastTimer = setTimeout(() => {
        toast.classList.remove("show");
    }, 2500);
}