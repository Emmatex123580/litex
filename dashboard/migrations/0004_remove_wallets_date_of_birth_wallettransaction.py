# Generated by Django 4.1.4 on 2023-02-10 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_customuser_verified_alter_customuser_uid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallets',
            name='date_of_birth',
        ),
        migrations.CreateModel(
            name='WalletTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=250, verbose_name='transaction id')),
                ('status', models.CharField(choices=[('pending', 'pending'), ('success', 'success'), ('fail', 'fail')], default='pending', max_length=200, null=True)),
                ('transaction_type', models.CharField(choices=[('funding', 'Bank transfer funding'), ('payout', 'Bank transfer payout'), ('debit user wallet', 'Debit user wallet'), ('credit user wallet ', 'credit user wallet')], max_length=250, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=100, verbose_name='amount')),
                ('date', models.CharField(max_length=200, verbose_name='date')),
                ('wallet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.wallets')),
            ],
        ),
    ]