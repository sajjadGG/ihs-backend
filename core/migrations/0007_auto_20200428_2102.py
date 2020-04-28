# Generated by Django 3.0.2 on 2020-04-28 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_appointment_clinic_clinicdoctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='appointment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Appointment'),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.CharField(blank=True, max_length=1023, null=True),
        ),
    ]
