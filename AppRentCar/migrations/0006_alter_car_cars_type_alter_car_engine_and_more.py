# Generated by Django 4.2.4 on 2023-08-21 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppRentCar', '0005_alter_car_cars_type_alter_car_drive_alter_car_engine_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='cars_type',
            field=models.CharField(choices=[('Hatchback', 'Hatchback'), ('Van', 'Van'), ('Sedan', 'Sedan'), ('Suv', 'Suv'), ('Coupe', 'Coupe'), ('Kombi', 'Kombi'), ('Shooting brake', 'Shooting brake')], max_length=32),
        ),
        migrations.AlterField(
            model_name='car',
            name='engine',
            field=models.CharField(choices=[('Benzyna', 'Benzyna'), ('Elektryczny', 'Elektryczny'), ('Diesel', 'Diesel'), ('Hybryda', 'Hybryda')], max_length=32),
        ),
        migrations.AlterField(
            model_name='car',
            name='no_gears',
            field=models.CharField(choices=[('5', '5'), ('8', '8'), ('7', '7'), ('6', '6')], max_length=8),
        ),
        migrations.AlterField(
            model_name='car',
            name='transmission',
            field=models.CharField(choices=[('Manuala', 'Manualna'), ('Automatyczna', 'Automatyczna')], max_length=32),
        ),
    ]
