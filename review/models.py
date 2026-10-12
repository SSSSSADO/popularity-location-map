from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class Review(models.Model):
    location = models.ForeignKey(
        "location.Location",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "reviews"
        ordering = ["-created_at", "-updated_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["location", "author"],
                name="unique_review_per_user_location",
            )
        ]

    def __str__(self) -> str:
        return f"{self.location} - {self.author}: {self.rating}/5"


class ReviewVote(models.Model):
    class VoteType(models.TextChoices):
        LIKE = "Like"
        DISLIKE = "Dislike"

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="review_votes",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="review_votes",
    )
    vote = models.CharField(max_length=7, choices=VoteType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "review_votes"
        ordering = ["created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["review", "author"],
                name="unique_vote_per_user_review",
            )
        ]

    def __str__(self):
        return f"{self.user}: {self.vote_type} on review {self.review_id}"
