from django.db import models


class FbGroup(models.Model):
    group_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class FbUser(models.Model):
    user_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class FbPost(models.Model):
    # todo - handle group notifications (like changes of descriptions, appointment of moderators, etc.)
    post_id = models.CharField(max_length=255, unique=True)
    group = models.ForeignKey(FbGroup, on_delete=models.CASCADE)
    author = models.ForeignKey(FbUser, to_field='user_id',  on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    created_time = models.DateTimeField()
    last_active = models.DateTimeField(null=True)
    parent = models.ForeignKey("self",  to_field='post_id', on_delete=models.CASCADE,
                               blank=True, null=True, related_name='children')

    def get_images(self):
        return FbMedia.objects.filter(post=self)


class FbMedia(models.Model):
    # todo make models for other media types - files, notes, videos and such
    photo = models.ImageField(upload_to='images', null=True)
    fb_url = models.URLField(null=True, max_length=1024)
    description = models.TextField(null=True)
    post = models.ForeignKey(FbPost, on_delete=models.CASCADE, blank=True, null=True, related_name='images')


class FbReaction(models.Model):
    author = models.ForeignKey(FbUser,  on_delete=models.CASCADE)
    type = models.TextField()
    post = models.ForeignKey(FbPost, on_delete=models.CASCADE, blank=True, null=True, related_name='reactions')

    def __str__(self):
        return "{0} from {1}".format(self.author, self.type)