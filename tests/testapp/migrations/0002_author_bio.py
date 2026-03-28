from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("testapp", "0001_initial"),
    ]
    operations = [
        migrations.AddField(
            model_name="author",
            name="bio",
            field=models.TextField(default=""),
        ),
    ]
