from __future__ import absolute_import, unicode_literals

import logging

import facepy
from celery import shared_task
from datetime import datetime
import pytz
import requests
from django.db import IntegrityError

from .models import FbUser, FbPost, FbMedia, FbGroup

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile


logger = logging.getLogger(__name__)


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
        # todo - update last active date via @property
        last_active = getattr(parent, 'last_active')
        if not last_active:
            pass
        elif created_time > last_active:
            parent.update(last_active=created_time)
    try:
        post, created = FbPost.objects.get_or_create(**kwargs, group=group, author=author, parent=parent)

        if not created:
            post.save()

    except IntegrityError:
        post = FbPost.objects.filter(post_id=locals().get('kwargs').get('post_id')).first()
        pass

    for attachment in attachments:
        # todo handle other type of attachments - video, files, etc.
        if type(attachment) is not dict:
            # dirty hack
            return
        url = attachment.get('media', {}).get('image', '')
        if not url:
            continue

        save_image(description=attachment.get('description', ''),
                   url=url.get('src'),
                   post=post,
                   )


@shared_task
def manage_post(post: dict, group: FbGroup, parent_id: str=None, skip: bool=True):
    author_data = post.get('from')
    author_data = {
        'user_id': author_data.get('id') if author_data else '12345',
        'name': author_data.get('name') if author_data else 'disabled account'
    }

    attachments = post.get('attachment', '')
    if attachments:
        attachments = [attachments]
    
    elif not attachments:
        attachments = post.get('attachments', {})
        if attachments:
            attachments =  attachments.get('data', [])

    created_time = datetime.strptime(
        post.get('created_time').split('+')[0], '%Y-%m-%dT%H:%M:%S')
    created_time = pytz.timezone("Europe/Warsaw").localize(created_time)
    # todo - scrap reactions too
    # todo - scrap pools
    create_post_and_author(
        author_data=author_data,
        post_id=post.get('id'),
        message=post.get('message', None),
        created_time=created_time,
        parent_id=parent_id,
        group=group,
        attachments=attachments,
    )

    if not post.get('comments'):
        return

    if post['comments'].get('data'):
        for comment in post['comments'].get('data'):
            manage_post(comment, group, post.get('id'))


@shared_task
def fetch_group_posts(group_id: str, group_name: str, token: str, fields: str=None):
    group, created = FbGroup.objects.get_or_create(
        group_id=group_id,
        name=group_name
    )
    if created:
        group.save()

    if not fields:
        fields = 'id,from,message,attachments,reactions, created_time,' \
                 'comments{message,from,attachment,reactions,created_time,' \
                 'comments{from,message,attachment,reactions,created_time}}'
    graph = facepy.GraphAPI(token)
    fetched_data = graph.get(group_id + "/feed", fields=fields, page=True, retry=3)
    for data in fetched_data:
        for post in data.get('data'):
            logger.info('Scrapping post {0} from {1}'.format(post.get('id'), post.get('created_time')))
            manage_post(post, group)

    logger.info('scrapping complete.')
