from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Destination(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'agent'})

    name = models.CharField(max_length=100)

    country = models.CharField(max_length=100, default='Ethiopia')

    city = models.CharField(max_length=100, blank=True, null = True)

    location = models.CharField(max_length=100)

    description = models.TextField()

    image = models.ImageField(upload_to='destinations/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Package(models.Model):
    destination = models.ForeignKey(
        Destination, on_delete=models.CASCADE, related_name="packages"
    )
    agent = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="packages",
        limit_choices_to={'role': 'agent'}
    )
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    details = models.TextField()
    image = models.ImageField(upload_to='packages/', null=True, blank=True)
    likes = models.ManyToManyField(User, related_name="liked_packages", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    seats = models.PositiveIntegerField(default=10)
    seats_remaining = models.PositiveIntegerField(default=10)

    booked_seats = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} - {self.destination.name}"
    def available_seats(self):
        return self.total_seats - self.booked_seats
    def likes_count(self):
        return self.likes.count()
    def like(self, user):
        """Add a like from the user"""
        self.likes.add(user)
        self.save()

    def unlike(self, user):
        """Remove a like from the user"""
        self.likes.remove(user)
        self.save()

    def likes_count(self):
        """Return the total number of likes"""
        return self.likes.count()