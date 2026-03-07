from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import Album, Photo,AlbumLike
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Exists, OuterRef
from .models import Comment
from django.core.paginator import Paginator
from .models import PhotoLike
from django.db.models import Prefetch
from .forms import AvatarForm
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import UserUpdateForm


@login_required
def index(request):

    # --- Фото з лайками ---
    photos_qs = Photo.objects.annotate(
        likes_count=Count('likes')
    )

    if request.user.is_authenticated:
        photos_qs = photos_qs.annotate(
            user_liked=Exists(
                PhotoLike.objects.filter(
                    user=request.user,
                    photo=OuterRef('pk')
                )
            )
        )

    # --- Альбоми ---
    albums_qs = Album.objects.annotate(
        likes_count=Count('likes')
    ).order_by('-likes_count', '-created_at')

    if request.user.is_authenticated:
        albums_qs = albums_qs.annotate(
            user_liked=Exists(
                AlbumLike.objects.filter(
                    user=request.user,
                    album=OuterRef('pk')
                )
            )
        )

    # 🔥 ОПТИМІЗАЦІЯ ТУТ
    albums_qs = albums_qs.prefetch_related(
        Prefetch("photos", queryset=photos_qs, to_attr="photos_with_likes")
    )

    paginator = Paginator(albums_qs, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "main/index.html", {
        "albums": page_obj,
        "page_obj": page_obj,
    })

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()

    return render(request, "main/signup.html", {"form": form})


@login_required
def profile(request):
    profile = request.user.profile

    if request.method == "POST":
        avatar_form = AvatarForm(request.POST, request.FILES, instance=profile)
        user_form = UserUpdateForm(request.POST, instance=request.user)

        if "avatar" in request.FILES:
            if avatar_form.is_valid():
                avatar_form.save()
                return redirect("profile")

        else:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "Дані оновлено")
                return redirect("profile")

    else:
        avatar_form = AvatarForm(instance=profile)
        user_form = UserUpdateForm(instance=request.user)

    my_albums = Album.objects.filter(user=request.user).annotate(
        likes_count=Count('likes')
    ).order_by('-likes_count', '-created_at')

    my_likes = Album.objects.filter(
        likes__user=request.user
    ).annotate(
        likes_count=Count('likes')
    ).order_by('-likes_count')

    liked_photos = Photo.objects.filter(
        likes__user=request.user
    ).annotate(
        likes_count=Count('likes')
    ).order_by('-likes_count', '-created_at')

    my_comments = Comment.objects.filter(user=request.user).select_related("album")

    return render(request, "main/profile.html", {
        "avatar_form": avatar_form,
        "profile": profile,
        "my_albums": my_albums,
        "my_likes": my_likes,
        "my_comments": my_comments,
        "liked_photos": liked_photos,
        "user_form": user_form,
    })
@login_required
def album_detail(request, album_id):

    album = get_object_or_404(
        Album.objects.select_related("user").prefetch_related("photos"),
        id=album_id
    )

    photos = (
        Photo.objects
        .filter(album=album)
        .annotate(likes_count=Count('likes'))
        .order_by('-likes_count', '-created_at')
    )

    if request.user.is_authenticated:
        photos = photos.annotate(
            user_liked=Exists(
                PhotoLike.objects.filter(
                    user=request.user,
                    photo=OuterRef('pk')
                )
            )
        )

    comments = album.comments.select_related("user").order_by("-created_at")

    return render(request, "main/album_detail.html", {
        "album": album,
        "photos": photos,
        "comments": comments
    })
@login_required
@require_POST
def like_album(request, album_id):

    if not request.user.is_authenticated:
        return JsonResponse({"error": "login required"}, status=403)

    album = Album.objects.get(id=album_id)

    like, created = AlbumLike.objects.get_or_create(
        user=request.user,
        album=album
    )

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    count = AlbumLike.objects.filter(album=album).count()

    return JsonResponse({
        "liked": liked,
        "count": count
    })

@login_required
@require_POST
def like_photo(request, photo_id):

    if not request.user.is_authenticated:
        return JsonResponse({"error": "login required"}, status=403)

    photo = Photo.objects.get(id=photo_id)

    like, created = PhotoLike.objects.get_or_create(
        user=request.user,
        photo=photo
    )

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    count = PhotoLike.objects.filter(photo=photo).count()

    return JsonResponse({
        "liked": liked,
        "count": count
    })

@login_required
def add_comment(request, album_id):
    if request.method == "POST":
        text = request.POST.get("text", "").strip()

        if text:
            Comment.objects.create(
                user=request.user,
                album_id=album_id,
                text=text
            )

    return redirect("index")
@login_required
def top_photos(request):
    photos = (
        Photo.objects
        .annotate(likes_count=Count('likes'))
        .filter(likes_count__gt=0)
        .order_by('-likes_count', '-created_at')[:20]
    )

    return render(request, "main/top_photos.html", {
        "photos": photos
    })
@login_required
def public_profile(request, username):
    user_obj = get_object_or_404(User, username=username)

    albums = Album.objects.filter(user=user_obj).annotate(
        likes_count=Count('likes')
    ).order_by('-likes_count', '-created_at')

    return render(request, "main/public_profile.html", {
        "profile_user": user_obj,
        "albums": albums,
    })

def user_owns_album(request, album):
    if album.user != request.user:
        return HttpResponseForbidden("Forbidden")

@require_POST
@login_required
def delete_comment(request, comment_id):
    comment = Comment.objects.filter(
        id=comment_id,
        user=request.user
    ).first()

    if not comment:
        messages.error(request, "Коментар не знайдено або доступ заборонений")
        return redirect("profile")

    comment.delete()
    messages.success(request, "Коментар видалено")
    return redirect("profile")

class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    fields = ["title", "description"]
    template_name = "main/album_form.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        images = self.request.FILES.getlist("images")

        for image in images:
            Photo.objects.create(
                album=self.object,
                image_full=image,
                image_thumb=image
            )

        messages.success(self.request, "Альбом створено")
        return response

class AlbumUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Album
    fields = ["title", "description"]
    template_name = "main/album_form.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        response = super().form_valid(form)

        images = self.request.FILES.getlist("images")

        for image in images:
            Photo.objects.create(
                album=self.object,
                image_full=image,
                image_thumb=image
            )

        messages.success(self.request, "Альбом оновлено")
        return response

    def test_func(self):
        album = self.get_object()
        return album.user == self.request.user

class AlbumDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Album
    template_name = "main/album_confirm_delete.html"
    success_url = reverse_lazy("profile")

    def test_func(self):
        album = self.get_object()
        return album.user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Альбом видалено")
        return super().form_valid(form)

@login_required
@require_POST
def delete_photo(request, photo_id):

    photo = get_object_or_404(Photo, id=photo_id)

    if photo.album.user != request.user:
        return JsonResponse({"success": False})

    photo.delete()

    return JsonResponse({
        "success": True
    })