from django import forms
from django_countries.fields import CountryField
from .models import RoomType, Amenity, Facility


class SearchForm(forms.Form):
    city = forms.CharField(initial="Anywhere")
    price = forms.IntegerField()
    country = CountryField(default="IN").formfield()
    room_type = forms.ModelChoiceField(
        required=False,
        empty_label="Any kind",
        queryset=RoomType.objects.all(),
    )
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    facilities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
