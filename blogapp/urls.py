from django.urls import path
from .views import *
app_name = 'blogapp'

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("blog/list/", BlogListView.as_view(), name="bloglist"),
    path("blog/create/", BlogCreateView.as_view(), name="blogcreate"),
    path("blog/<int:pk>/detail/", BlogDetailView.as_view(), name="blogdetail"),
    path("blog/<int:pk>/comment/",
         CommentCreateView.as_view(), name="commentcreate"),
    path("blog/<int:pk>/update/", BlogUpdateView.as_view(), name="blogupdate"),
    path("blog/<int:pk>/delete/", BlogDeleteView.as_view(), name="blogdelete"),
    path("blog/<int:pk>/comment/delete/",
         CommentDeleteView.as_view(), name="commentdelete"),
    path("change/password/", PasswordChangeView.as_view(), name="passwordchange"),
    path("search/", SearchView.as_view(), name="search"),
    path("username_checker/", UsernameCheckerView.as_view(), name="usernamechecker"),






]
