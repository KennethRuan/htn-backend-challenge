from django.db import models


class Hacker(models.Model):
    hacker_id = models.AutoField(primary_key=True)
    name = models.TextField()
    company = models.TextField()
    email = models.TextField()
    phone = models.TextField()

    class Meta:
        managed = False
        db_table = 'hackers'


class Skill(models.Model):
    skill_id = models.AutoField(primary_key=True)
    name = models.TextField()
    rating = models.TextField()
    hacker = models.ForeignKey(Hacker, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'skills'
