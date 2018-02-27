from datetime import datetime
import pytz

import facepy
import logging

from ..tasks import create_post_and_author
from ..models import FbGroup

logger = logging.getLogger(__name__)


def manage_post(post: dict, group: FbGroup, parent_id: str=None, skip: bool=True):
    author_data = post.get('from')
    author_data = {
        'user_id': author_data.get('id') if author_data else '12345',
        'name': author_data.get('name') if author_data else 'disabled account'
    }
    attachments = post.get('attachment', {})

    if not attachments:
        attachments = post.get('attachments', {})
        if attachments:
            attachments =  attachments.get('data', [])

    created_time = datetime.strptime(
        post.get('created_time').split('+')[0], '%Y-%m-%dT%H:%M:%S')
    created_time = pytz.timezone("Europe/Warsaw").localize(created_time)

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


def fetch_group_post(group_id: str, group_name: str, token: str, fields: str=None):
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
