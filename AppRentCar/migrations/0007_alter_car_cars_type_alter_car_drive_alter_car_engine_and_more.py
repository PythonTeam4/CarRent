# Generated by Django 4.2.4 on 2023-08-24 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppRentCar', '0006_alter_car_cars_type_alter_car_engine_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='cars_type',
            field=models.CharField(choices=[('Hatchback', 'Hatchback'), ('Shooting brake', 'Shooting brake'), ('Van', 'Van'), ('Suv', 'Suv'), ('Sedan', 'Sedan'), ('Kombi', 'Kombi'), ('Coupe', 'Coupe')], max_length=32),
        ),
        migrations.AlterField(
            model_name='car',
            name='drive',
            field=models.CharField(choices=[('Tylni', 'Tylni'), ('Przedni', 'Przedni'), ('4x4', '4x4')], max_length=32),
        ),
        migrations.AlterField(
            model_name='car',
            name='engine',
            field=models.CharField(choices=[('Benzyna', 'Benzyna'), ('Hybryda', 'Hybryda'), ('Elektryczny', 'Elektryczny'), ('Diesel', 'Diesel')], max_length=32),
        ),
        migrations.AlterField(
            model_name='car',
            name='no_gears',
            field=models.CharField(choices=[('6', '6'), ('5', '5'), ('7', '7'), ('8', '8')], max_length=8),
        ),
    ]
