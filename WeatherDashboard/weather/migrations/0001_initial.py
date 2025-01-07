# Generated by Django 4.2.17 on 2025-01-06 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=255)),
                ('datetime', models.DateTimeField()),
                ('temperature', models.FloatField(blank=True, null=True)),
                ('weather_description', models.TextField(blank=True, null=True)),
                ('humidity', models.FloatField(blank=True, null=True)),
                ('wind_speed', models.FloatField(blank=True, null=True)),
            ],
            options={
                'indexes': [models.Index(fields=['city_name'], name='idx_city_name')],
            },
        ),
        migrations.AddConstraint(
            model_name='weather_data',
            constraint=models.UniqueConstraint(fields=('city_name', 'datetime'), name='unique_weather_data'),
        ),
    ]
