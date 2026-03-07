document.addEventListener("DOMContentLoaded", () => {
    const animatedItems = document.querySelectorAll(
        '.slide-left, .zoom'
    );

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('show');
            }
        });
    }, {
        threshold: 0.2
    });

    animatedItems.forEach(item => observer.observe(item));
});

document.querySelectorAll(".like-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        const albumId = btn.dataset.id;

        fetch(`/album/${albumId}/like/`)
            .then(res => res.json())
            .then(data => {
                document.getElementById(
                    `likes-${albumId}`
                ).innerText = data.count;

                btn.classList.toggle("liked", data.liked);
            });
    });
});
