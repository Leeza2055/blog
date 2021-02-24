from django.views.generic import *
from django.db.models import Q
from django.http import JsonResponse
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from .models import *
from .forms import *


class UserRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            pass
        else:
            return redirect("/login/")
        return super().dispatch(request, *args, **kwargs)


class HomeView(TemplateView):
    template_name = 'home.html'


class SignupView(FormView):
    template_name = "signup.html"
    form_class = SignupForm
    success_url = "/"

    def form_valid(self, form):
        uname = form.cleaned_data["username"]
        email = form.cleaned_data["email"]
        pword = form.cleaned_data["password"]
        print(uname, email, pword)
        User.objects.create_user(uname, email, pword)
        return super().form_valid(form)


class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = "/"

    def form_valid(self, form):
        a = form.cleaned_data["username"]
        b = form.cleaned_data["password"]
        usr = authenticate(username=a, password=b)
        if usr is not None:
            login(self.request, usr)
        else:
            return render(self.request, self.template_name,
                          {"error": "Invalid username or password",
                           "form": form})
        return super().form_valid(form)


class LogoutView(View):

    def get(self, request):
        logout(request)

        return redirect("/login/")


class BlogListView(ListView):
    template_name = "bloglist.html"
    queryset = Blog.objects.all()
    context_object_name = "allblogs"


class BlogCreateView(UserRequiredMixin, CreateView):
    template_name = "blogcreate.html"
    form_class = BlogForm
    #success_url = "/blog/list/"
    success_url = reverse_lazy("blogapp:bloglist")

    def form_valid(self, form):
        logged_in_user = self.request.user
        form.instance.author = logged_in_user
        return super().form_valid(form)


class BlogDetailView(DetailView):
    template_name = "blogdetail.html"
    model = Blog
    context_object_name = "blogobject"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_id = self.kwargs["pk"]
        blog = Blog.objects.get(id=blog_id)

        context["commentform"] = CommentForm
        return context


class CommentCreateView(UserRequiredMixin, CreateView):
    template_name = "commentcreate.html"
    form_class = CommentForm
    success_url = reverse_lazy("blogapp:bloglist")

    def form_valid(self, form):
        blog_id = self.kwargs["pk"]
        blog = Blog.objects.get(id=blog_id)
        form.instance.blog = blog
        logged_in_user = self.request.user
        form.instance.commenter = logged_in_user

        return super().form_valid(form)

    def get_success_url(self):
        blog_id = self.kwargs["pk"]
        return "/blog/" + str(blog_id) + "/detail/"


class BlogUpdateView(UserRequiredMixin, UpdateView):
    template_name = "blogcreate.html"
    form_class = BlogForm
    model = Blog
    success_url = reverse_lazy("blogapp:bloglist")


class BlogDeleteView(UserRequiredMixin, DeleteView):
    template_name = "blogdelete.html"
    model = Blog
    success_url = reverse_lazy("blogapp:bloglist")


class CommentDeleteView(UserRequiredMixin, DeleteView):
    template_name = "commentdelete.html"
    model = Comment
    success_url = reverse_lazy("blogapp:bloglist")

    def dispatch(self, request, *args, **kwargs):
        comment_id = self.kwargs["pk"]
        comment = Comment.objects.get(id=comment_id)
        if request.user == comment.commenter:
            pass
        else:
            return render(self.request, "error.html", {"error: Invalid action"})
        return super().dispatch(request, *args, **kwargs)


class PasswordChangeView(UserRequiredMixin, FormView):
    template_name = "Passwordchange.html"
    form_class = ChangePasswordForm
    success_url = "/"

    def form_valid(self, form):
        logged_in_user = self.request.user
        new_pword = form.cleaned_data["new_password"]
        old_pword = form.cleaned_data["old_password"]
        usr = authenticate(username=logged_in_user.username,
                           password=old_pword)
        if usr is not None:
            logged_in_user.set_password(new_pword)
            logged_in_user.save()
            send_mail("Password Changed", "Your password has been changed successfully. Your \
				new password is " + new_pword, settings.EMAIL_HOST_USER, [logged_in_user.email,
                                                              "sangit.niroula@gmail.com"], fail_silently=False)
        else:
            return render(self.request, self.template_name, {"error": "Invalid password",
                                                             "form": form})

        return super().form_valid(form)


class SearchView(TemplateView):
    template_name = "searchresult.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyword = self.request.GET["query"]
        print(keyword, "+++++++++++++++++")
        blogs = Blog.objects.filter(Q(title__icontains=keyword)
                                    | Q(content__icontains=keyword) | Q(author__username__icontains=keyword))
        context["searched_blogs"] = blogs

        return context


class UsernameCheckerView(View):
    def get(self, request):

        # print("I was called")
        user_input = request.GET["uname"]
        if User.objects.filter(username=user_input).exists():
            message = "yes"
        else:
            message = "no"

        return JsonResponse({"response": message})

