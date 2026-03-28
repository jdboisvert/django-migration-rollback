from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("testapp2", "0001_initial"),
    ]
    operations = [
        migrations.AddField(
            model_name="book",
            name="summary",
            field=models.TextField(default=""),
        ),
    ]
