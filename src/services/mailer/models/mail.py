from django.db import models


class Mail(models.Model):
    """
    Entity for the collection of user uploaded data
    """

    sender = models.CharField(max_length=150)
    subject = models.CharField(max_length=150)
    recipients = models.ManyToManyField("user.User", related_name="mails", blank=True)
    # TODO: should be encrypted
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        """
        String representation of the dataset
        """
        return str(self.subject)
