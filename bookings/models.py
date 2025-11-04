from django.db import models
from django.contrib.auth import get_user_model
from destinations.models import Package

User = get_user_model()

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="bookings")
    seats_booked = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Check if there are enough seats
        if self.seats_booked > self.package.available_seats():
            raise ValueError("Not enough seats available for this package")
        
        # Update booked seats
        self.package.booked_seats += self.seats_booked
        self.package.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} booked {self.seats_booked} seat(s) for {self.package.title}"
