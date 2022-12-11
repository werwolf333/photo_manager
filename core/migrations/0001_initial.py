# Generated by Django 4.0 on 2022-12-10 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('geo_longitude', models.FloatField(blank=True, max_length=200, null=True)),
                ('geo_latitude', models.FloatField(blank=True, max_length=200, null=True)),
                ('geo_altitude', models.FloatField(blank=True, max_length=200, null=True)),
                ('date_of_download', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, help_text='100x100px', upload_to='images/core/', verbose_name='ссылка картинки')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='human', to='core.photo')),
            ],
        ),
    ]