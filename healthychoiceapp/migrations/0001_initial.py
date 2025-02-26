# Generated by Django 2.1.2 on 2018-12-13 11:45

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateField()),
                ('name', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('slug', models.SlugField(editable=False)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='facts_img/')),
                ('slug', models.SlugField(editable=False)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='healthychoiceapp.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('slug', models.SlugField(editable=False)),
                ('recipe', models.TextField()),
                ('image', models.ImageField(upload_to='')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('categories', models.ManyToManyField(to='healthychoiceapp.Category')),
                ('ingredients', models.ManyToManyField(to='healthychoiceapp.Product')),
            ],
        ),
    ]
