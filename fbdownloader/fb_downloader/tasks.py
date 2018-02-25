from __future__ import absolute_import, unicode_literals

from celery import shared_task
import requests

from .models import FbUser, FbPost, FbMedia

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile


@shared_task
def save_image(url: str, post: FbPost, description: str):

    if FbMedia.objects.filter(fb_url=url).first():
        return

    image = FbMedia(post=post, fb_url=url, description=description)
    img_filename = url.split('/')[-1].split('?')[0]

    with NamedTemporaryFile() as temp:

        r = requests.get(url)
        temp.write(r.content)
        temp.flush()

        image.photo.save(img_filename, File(temp), save=True)


@shared_task
def create_post_and_author(parent_id, author_data, group, attachments: list, **kwargs):
    # todo - scrap reactions too
    author, created = FbUser.objects.get_or_create(**author_data)
    if created:
        author.save()

    created_time = locals().get('kwargs').get('created_time')
    parent = FbPost.objects.filter(post_id=parent_id).first()

    if parent:
        last_active = getattr(parent, 'last_active')
        if not last_active:
            pass
        elif created_time > last_active:
            parent.update(last_active=created_time)

    post, created = FbPost.objects.get_or_create(**kwargs, group=group, author=author, parent=parent)

    if not created:
        post.save()

    for attachment in attachments:
        #todo handle other type of attachments - video, files, etc.
        url = attachment.get('media', {}).get('image', '')
        if not url:
            return

        save_image(description=attachment.get('description'),
                   url=url.get('src'),
                   post=post,
                   )
