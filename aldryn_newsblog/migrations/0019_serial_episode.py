# Generated by Django 2.2.13 on 2023-01-06 12:40

import django.db.models.deletion
from django.db import migrations, models

import parler.fields


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_newsblog', '0018_hide_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Serial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='episode',
            field=models.PositiveIntegerField(default=1, verbose_name='Episode'),
        ),
        migrations.AlterField(
            model_name='articletranslation',
            name='master',
            field=parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='aldryn_newsblog.Article'),
        ),
        migrations.AlterField(
            model_name='newsblogconfig',
            name='author_no_photo',
            field=models.BooleanField(default=True, help_text='Display "No photo" icon if the user does not have one.', verbose_name='Display No-photo icon'),
        ),
        migrations.AlterField(
            model_name='newsblogconfigtranslation',
            name='master',
            field=parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='aldryn_newsblog.NewsBlogConfig'),
        ),
        migrations.AddField(
            model_name='article',
            name='serial',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='aldryn_newsblog.Serial', verbose_name='Serial'),
        ),
    ]
