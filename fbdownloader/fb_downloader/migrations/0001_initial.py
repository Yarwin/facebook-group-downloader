# Generated by Django 2.0.2 on 2018-02-25 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FbGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FbMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(null=True, upload_to='images')),
                ('fb_url', models.URLField(max_length=1024, null=True)),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FbPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=255, unique=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('created_time', models.DateTimeField()),
                ('last_active', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FbReaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='FbUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='fbreaction',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fb_downloader.FbUser'),
        ),
        migrations.AddField(
            model_name='fbreaction',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to='fb_downloader.FbPost'),
        ),
        migrations.AddField(
            model_name='fbpost',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fb_downloader.FbUser', to_field='user_id'),
        ),
        migrations.AddField(
            model_name='fbpost',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fb_downloader.FbGroup'),
        ),
        migrations.AddField(
            model_name='fbpost',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='fb_downloader.FbPost', to_field='post_id'),
        ),
        migrations.AddField(
            model_name='fbmedia',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='fb_downloader.FbPost'),
        ),
    ]