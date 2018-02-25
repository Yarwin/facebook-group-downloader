from multiprocessing import Process

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from .models import FbPost, FbGroup
from .downloader_script.fetch_group import fetch_group_post


@csrf_exempt
def get_group(request):
    if request.method == 'POST':
        token = request.POST.get('user_token')
        group_id = request.POST.get('group_id')
        group_name = request.POST.get('group_name')
        p = Process(target=fetch_group_post, args=(group_id, group_name, token))
        p.start()
        return redirect('/')

    return render(request, 'get-group.html')


class HomeListView(ListView):
    model = FbGroup
    template_name = "home.html"

    def get_queryset(self):
        return FbGroup.objects.all()


class GroupListView(ListView):
    # todo - add another view filtering, add detailed post view
    model = FbPost
    template_name = "group/index.html"
    paginate_by = 20

    def get_queryset(self):
        return FbPost.objects.filter(group__group_id=self.kwargs['group'], parent=None).order_by('-last_active')
