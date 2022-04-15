# Generated by Django 4.0.3 on 2022-04-15 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=45)),
                ('subtitle', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('running_time', models.IntegerField()),
                ('running_date', models.DateField()),
                ('location', models.CharField(max_length=45)),
                ('preparation', models.CharField(max_length=45)),
                ('max_visitor', models.IntegerField()),
                ('image_url', models.CharField(max_length=1000)),
                ('close_date', models.DateField()),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.host')),
            ],
            options={
                'db_table': 'places',
            },
        ),
        migrations.CreateModel(
            name='PlaceStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'place_statuses',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content', models.TextField()),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.place')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'reviews',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.place')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'reservations',
            },
        ),
        migrations.AddField(
            model_name='place',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.placestatus'),
        ),
    ]
