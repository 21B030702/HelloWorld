# Generated by Django 5.0.4 on 2024-04-19 07:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_delivery"),
    ]

    operations = [
        migrations.AlterField(
            model_name="delivery",
            name="delivery_status",
            field=models.CharField(
                choices=[
                    ("processing", "Processing"),
                    ("shipped", "Shipped"),
                    ("delivered", "Delivered"),
                    ("canceled", "Canceled"),
                ],
                max_length=50,
            ),
        ),
        migrations.CreateModel(
            name="Bid",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bid_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("bid_time", models.DateTimeField(auto_now_add=True)),
                (
                    "bidder",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bids",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bids",
                        to="core.item",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DeliveryStatus",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("processing", "Processing"),
                            ("shipped", "Shipped"),
                            ("delivered", "Delivered"),
                            ("canceled", "Canceled"),
                        ],
                        max_length=50,
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "purchase",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="delivery_statuses",
                        to="core.purchase",
                    ),
                ),
            ],
        ),
    ]
