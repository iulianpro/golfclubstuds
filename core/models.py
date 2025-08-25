from django.db import models


class Member(models.Model):
    class Status(models.TextChoices):
        CURRENT = "CURRENT", "Current"
        EX_MEMBER = "EX_MEMBER", "Ex-Member"

    # Basic info
    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)

    # Membership status with choices
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.CURRENT,
        db_index=True,
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)  # set when created
    updated_at = models.DateTimeField(auto_now=True)      # set on every update

    def toggle_status(self, *, save=True):
        """
        Toggle between CURRENT and EX_MEMBER.
        If save=True, persist the change in the database.
        """
        self.status = (
            self.Status.EX_MEMBER
            if self.status == self.Status.CURRENT
            else self.Status.CURRENT
        )
        if save:
            self.save(update_fields=["status", "updated_at"])
        return self.status

    def __str__(self):
        # Display member as "Name (Status)"
        return f"{self.name} ({self.get_status_display()})"

    class Meta:
        ordering = ["name"]  # default order by name
        indexes = [
            models.Index(fields=["status", "name"]),  # for faster filtering
        ]
