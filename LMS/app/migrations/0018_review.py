# Generated by Django 4.2.1 on 2023-07-11 13:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0017_remove_subscriber_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.DecimalField(choices=[(5, 'Awesome - 5 stars'), (4.5, 'Pretty good - 4.5 stars'), (4, 'Pretty good - 4 stars'), (3.5, 'Meh - 3.5 stars'), (3, 'Meh - 3 stars'), (2.5, 'Kinda bad - 2.5 stars'), (2, 'Kinda bad - 2 stars'), (1.5, 'Meh - 1.5 stars'), (1, 'Sucks big time - 1 star'), (0.5, 'Sucks big time - 0.5 stars')], decimal_places=1, max_digits=2)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
