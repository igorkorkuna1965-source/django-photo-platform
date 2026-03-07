from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

urlpatterns = [
    path("", views.index, name="index"),

    path("login/",
         auth_views.LoginView.as_view(template_name="main/login.html"),
         name="login"),

    path("logout/",
         auth_views.LogoutView.as_view(next_page="index"),
         name="logout"),

    path("signup/", views.signup, name="signup"),

    path("album/<int:album_id>/like/", views.like_album, name="like_album"),

    path("album/<int:album_id>/comment/",
         views.add_comment,
         name="add_comment"),

    path("profile/", views.profile, name="profile"),

    path("user/<str:username>/", views.public_profile, name="public_profile"),

    path("photo/<int:photo_id>/like/",
         views.like_photo,
         name="like_photo"),

    path("top-photos/", views.top_photos, name="top_photos"),

    path("album/create/",
         views.AlbumCreateView.as_view(),
         name="album_create"),

    path("album/<int:pk>/edit/",
         views.AlbumUpdateView.as_view(),
         name="album_edit"),

    path("album/<int:pk>/delete/",
         views.AlbumDeleteView.as_view(),
         name="album_delete"),

    path("comment/<int:comment_id>/delete/",
         views.delete_comment,
         name="delete_comment"),

    path("photo/<int:photo_id>/delete/",
         views.delete_photo,
         name="delete_photo"),

    path("password-change/",
         PasswordChangeView.as_view(
             template_name="main/password_change.html",
             success_url=reverse_lazy("profile"),
         ),
         name="password_change"),
    path("album/<int:album_id>/", views.album_detail, name="album_detail"),
]

# Static + Media
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)