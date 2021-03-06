# Generated by Django 2.2 on 2019-08-12 18:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart_item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_id', models.TextField()),
                ('product_id', models.TextField()),
                ('product_quantity', models.CharField(max_length=20)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
