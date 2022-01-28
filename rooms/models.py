from django.db import models
from django.urls import reverse
from core import models as core_models
from django_countries.fields import CountryField
from django.utils import timezone
from users.models import User
from cal import Calendar


class AbstractItem(core_models.TimeStampedModel):
    """Abstract Item"""

    name = models.CharField(max_length=80)
    # subtitle = models.CharField(max_length=30)
    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name


class RoomType(AbstractItem):
    """RoomType Model Definition"""

    pass


class Amenity(AbstractItem):
    """Amenity Model Definition"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    """Facility Model Definition"""

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    """House Rule Model Definition"""

    pass


class Photo(core_models.TimeStampedModel):
    """Photo Model Definition"""

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", on_delete=models.CASCADE, related_name="photos")

    def __str__(self) -> str:
        return self.caption


class Room(core_models.TimeStampedModel):
    """Room Model Definition"""

    name = models.CharField(max_length=200)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=200)
    guests = models.IntegerField(default=1)
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rooms")
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField(Amenity, blank=True, related_name="rooms")
    facilities = models.ManyToManyField(Facility, blank=True, related_name="rooms")
    house_rules = models.ManyToManyField(HouseRule, blank=True, related_name="rooms")

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("rooms:detail", args=(self.pk,))

    def save(self, *args, **kwargs):
        self.city = self.city.capitalize()
        super().save(*args, **kwargs)

    def total_rating(self):
        total_reviews = self.reviews.all()
        sum = 0
        if total_reviews.count() > 0:
            for review in total_reviews:
                sum += review.rating_average()
            return round(sum / total_reviews.count(), 2)
        return 0

    def first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]
        return photos

    def get_calendars(self):
        now = timezone.now()
        year = now.year
        current_month = now.month
        next_month = current_month + 1
        if current_month == 12:
            next_month = 1
        this_month_cal = Calendar(year, current_month)
        next_month_cal = Calendar(year, next_month)
        return [this_month_cal, next_month_cal]
