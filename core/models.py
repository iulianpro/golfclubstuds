# core/models.py
from django.db import models
from django.db.models.functions import Lower


class Member(models.Model):
    class Status(models.TextChoices):
        CURRENT = 'CURRENT', 'Current'
        EX_MEMBER = 'EX_MEMBER', 'Ex-Member'

    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.CURRENT,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Canonicalise email before saving
        if self.email:
            self.email = self.email.strip().lower()
        super().save(*args, **kwargs)

    def toggle_status(self, *, save=True):
        self.status = (
            self.Status.EX_MEMBER if self.status == self.Status.CURRENT else self.Status.CURRENT
        )
        if save:
            self.save(update_fields=['status', 'updated_at'])
        return self.status

    def __str__(self):
        return f'{self.name} ({self.get_status_display()})'

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['status', 'name'])]
        # Case-insensitive uniqueness (when the DB supports functional unique indexes)
        constraints = [
            models.UniqueConstraint(
                Lower('email'),
                name='uniq_member_email_ci',
            ),
        ]
