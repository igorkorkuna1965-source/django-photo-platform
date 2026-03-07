function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".like-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const albumId = btn.dataset.album;

            fetch(`/album/${albumId}/like/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            })
            .then(res => {
                if (res.status === 403) {
                    window.location.href = "/login/";
                    throw new Error("auth");
                }
                return res.json();
            })
            .then(data => {

                if (!data) return;

                const block = btn.closest(".album-block");

                if (!block) return;

                block.querySelector(".likes-count").innerText =
                    "❤️ " + data.count;

                btn.classList.toggle("liked", data.liked);

                let text = block.querySelector(".liked-text");

                if (data.liked && !text) {
                    btn.insertAdjacentHTML(
                        "afterend",
                        "<span class='liked-text'>Ви вже оцінили</span>"
                    );
                }

                if (!data.liked && text) {
                    text.remove();
                }

            })
            .catch(err => {
                if (err.message !== "auth")
                    console.error(err);
            });
        });
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("show");
            }
        });
    }, { threshold: 0.2 });

    document.querySelectorAll(".zoom, .slide-left, .fade-in").forEach(el => {
        observer.observe(el);
    });
});

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".photo-like-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const photoId = btn.dataset.photo;

            fetch(`/photo/${photoId}/like/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            })
            .then(res => {
                if (res.status === 403) {
                    window.location.href = "/login/";
                    throw new Error("auth");
                }
                return res.json();
            })
            .then(data => {

                if (!data) return;

                btn.classList.toggle("liked", data.liked);
                btn.nextElementSibling.innerText = data.count;

            })
            .catch(err => {
                if (err.message !== "auth")
                    console.error(err);
            });
        });
    });
});

document.addEventListener("DOMContentLoaded", () => {
    setTimeout(() => {
        document.querySelectorAll(".message").forEach(el => {
            el.style.opacity = "0";
            el.style.transform = "translateY(-10px)";
            setTimeout(() => el.remove(), 400);
        });
    }, 5000);
});

document.addEventListener("click", function(e) {

    const btn = e.target.closest(".delete-photo-btn");

    if (!btn) return;

    const photoId = btn.dataset.photo;

    fetch(`/photo/${photoId}/delete/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {

        if (!data.success) return;

        const photoBlock = btn.closest(".existing-photo");

        if (!photoBlock) return;

        photoBlock.style.opacity = "0";

        setTimeout(() => {
            photoBlock.remove();
        }, 400);

    });

});

document.addEventListener("DOMContentLoaded", () => {

    const lightbox = document.getElementById("lightbox");
    const lightboxImg = document.getElementById("lightbox-img");

    document.querySelectorAll(".photo-grid img").forEach(img => {

        img.addEventListener("click", () => {

            lightboxImg.src = img.dataset.full;
            lightbox.classList.add("show");

        });

    });

    lightbox.addEventListener("click", () => {

        lightbox.classList.remove("show");

    });

});

document.addEventListener("DOMContentLoaded", () => {

    const sections = document.querySelectorAll("section[id]");
    const menuLinks = document.querySelectorAll(".nav-animated a");

    window.addEventListener("scroll", () => {

        let scrollPos = window.scrollY + 120;

        sections.forEach(section => {

            if (
                scrollPos >= section.offsetTop &&
                scrollPos < section.offsetTop + section.offsetHeight
            ) {

                menuLinks.forEach(link => {
                    link.classList.remove("active");

                    if (link.getAttribute("href") === "#" + section.id) {
                        link.classList.add("active");
                    }
                });
            }
        });

    });

});