document.addEventListener("DOMContentLoaded", function () {

    function getCookie(name) {
        let cookieValue = null;

        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');

            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();

                if (cookies[i].startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(
                        cookies[i].substring(name.length + 1)
                    );
                    break;
                }
            }
        }

        return cookieValue;
    }

    /* ------------------------------
       Preview upload images
    ------------------------------ */

    const input = document.getElementById("imageInput");
    const preview = document.getElementById("imagePreview");

    if (input) {
        input.addEventListener("change", function () {

            preview.innerHTML = "";

            const files = input.files;

            for (let file of files) {

                if (!file.type.startsWith("image/")) continue;

                const reader = new FileReader();

                reader.onload = function (e) {

                    const img = document.createElement("img");
                    img.src = e.target.result;

                    preview.appendChild(img);
                };

                reader.readAsDataURL(file);
            }

        });
    }

    /* ------------------------------
       Delete photo AJAX
    ------------------------------ */

    document.addEventListener("click", function (e) {

        if (!e.target.classList.contains("delete-photo-btn")) return;

        const btn = e.target;
        const photoId = btn.dataset.photo;

        fetch(`/photo/${photoId}/delete/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            }
        })
        .then(response => response.json())
        .then(data => {

            if (data.success) {

                const photoBlock = btn.closest(".existing-photo");

                if (photoBlock) {
                    photoBlock.style.transition = "opacity 0.4s ease";
                    photoBlock.style.opacity = "0";

                    setTimeout(() => photoBlock.remove(), 400);
                }
            }

        });

    });

});