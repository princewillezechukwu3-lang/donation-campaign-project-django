from django.db import models

class Campaign(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    minimum_donation = models.DecimalField(max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title


class Donation(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='donations')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    donor_name = models.CharField(max_length=255)
    donor_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor_name} - ₦{self.amount}"