from django.db import migrations


def seed_defaults(apps, schema_editor):
    Department = apps.get_model("accounts", "Department")
    ComplaintCategory = apps.get_model("complaints", "ComplaintCategory")

    departments = [
        {"name": "ICT", "code": "ICT"},
        {"name": "Electrical", "code": "ELEC"},
        {"name": "Plumbing", "code": "PLUMB"},
        {"name": "Cleaning", "code": "CLEAN"},
        {"name": "Security", "code": "SEC"},
    ]
    categories = [
        {"name": "Electrical Fault", "description": "Power failure, damaged wiring, sockets, or lighting."},
        {"name": "Plumbing Issue", "description": "Leaks, blocked drains, toilets, or water supply issues."},
        {"name": "Internet / Network", "description": "Wi-Fi, LAN, or access issues affecting connectivity."},
        {"name": "Cleaning / Sanitation", "description": "Waste, hygiene, or janitorial service concerns."},
        {"name": "Furniture / Fixtures", "description": "Broken desks, chairs, doors, windows, or fittings."},
    ]

    for department in departments:
        Department.objects.get_or_create(**department)

    for category in categories:
        ComplaintCategory.objects.get_or_create(name=category["name"], defaults={"description": category["description"]})


def unseed_defaults(apps, schema_editor):
    Department = apps.get_model("accounts", "Department")
    ComplaintCategory = apps.get_model("complaints", "ComplaintCategory")

    Department.objects.filter(code__in=["ICT", "ELEC", "PLUMB", "CLEAN", "SEC"]).delete()
    ComplaintCategory.objects.filter(
        name__in=[
            "Electrical Fault",
            "Plumbing Issue",
            "Internet / Network",
            "Cleaning / Sanitation",
            "Furniture / Fixtures",
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("complaints", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_defaults, unseed_defaults),
    ]