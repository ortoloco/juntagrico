# Generated by Django 2.2.2 on 2019-06-25 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('juntagrico', '0016_auto_20190402_0832'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='job',
            options={'permissions': (('can_edit_past_jobs', 'kann vergangene Jobs editieren'),), 'verbose_name': 'AbstractJob', 'verbose_name_plural': 'AbstractJobs'},
        ),
        migrations.AlterField(
            model_name='assignment',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='juntagrico.Job'),
        ),
    ]