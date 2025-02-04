# Generated by Django 5.0.1 on 2024-05-19 20:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0004_menuitem_users_alter_menuitem_time_to_serve'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='users',
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='time_to_serve',
            field=models.IntegerField(help_text='Time to make and serve in minutes'),
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coffee.menuitem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coffee.user')),
            ],
        ),
    ]
