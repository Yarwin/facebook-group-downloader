from multiprocessing import Process

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from .tasks import fetch_group_posts
from .models import FbPost, FbGroup


@csrf_exempt
def get_group(request):
    if request.method == 'POST':
        token = request.POST.get('user_token')
        group_id = request.POST.get('group_id')
        group_name = request.POST.get('group_name')
        p = Process(target=fetch_group_posts, args=(group_id, group_name, token))
        p.start()
        return redirect('/')

    return render(request, 'get-group.html')


class HomeListView(ListView):
    model = FbGroup
    template_name = "home.html"

    def get_queryset(self):
        return FbGroup.objects.all()


class GroupListView(ListView):
    # todo - add detailed post view
    # todo - make stats
    model = FbPost
    template_name = "group/index.html"
    ordering = ['-last_active']
    paginate_by = 20

    def get_queryset(self):
        result = FbPost.objects.filter(group__group_id=self.kwargs['group'], parent=None)
        post = self.request.GET.get('m', '')
        author = self.request.GET.get('a', '')
        if author:
            result = result.filter(author__name__contains=author)
        if post:
            result = result.filter(message__icontains=post)

        return result