# Generated by Django 3.0.8 on 2020-07-16 15:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('features', '0003_remove_purchase_collection'),
    ]

    operations = [
        migrations.CreateModel(
            name='MultiPlayerInvite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_invite', to='games.Game')),
                ('invitereceiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations_to', to=settings.AUTH_USER_MODEL)),
                ('invitesender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations_from', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('invitesender', 'invitereceiver')},
            },
        ),
    ]
