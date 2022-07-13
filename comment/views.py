from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from article.models import ArticleStorage
from userprofile.models import Profile
from .forms import CommentForm


@login_required
def post_comment(request, article_id):
    selected_article = get_object_or_404(ArticleStorage, id=article_id)
    user_profile = Profile.objects.get(user_id=request.user.id)
    if request.method == 'POST' and user_profile.comment_permission:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = selected_article
            new_comment.user = request.user
            new_comment.save()
    return redirect(selected_article)
