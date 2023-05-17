from django.db import models

# class Integration(models.Model):
#     name = models.CharField(max_length=200)


class Message(models.Model):
    body = models.TextField()
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)
    status_codes = ((1, "PENDING"), (2, "QUEUED"), (3, "ERROR"), (4, "SENT"))
    status = models.IntegerField(choices=status_codes, default=1)
    # integration = models.ForeignKey(Integration, on_delete=models.PROTECT)
