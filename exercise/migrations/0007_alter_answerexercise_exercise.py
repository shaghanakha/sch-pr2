# Generated by Django 4.0.2 on 2022-02-16 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0006_alter_answerexercise_exercise'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answerexercise',
            name='exercise',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='exercise.exercise'),
        ),
    ]
