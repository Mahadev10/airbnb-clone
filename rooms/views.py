from django.utils import timezone
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Count
from . import models
from rooms import models as room_models
from .forms import SearchForm


class HomeView(ListView):
    model = models.Room
    template_name = "rooms/all_rooms.html"
    context_object_name = "rooms"
    paginate_by = 10
    paginate_orphans = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context


class RoomDetail(DetailView):
    model = room_models.Room


def search(request):
    city = request.GET.get("city")
    if city:
        form = SearchForm(request.GET)
        if form.is_valid():
            city = form.cleaned_data.get("city")
            price = form.cleaned_data.get("price")
            country = form.cleaned_data.get("country")
            room_type = form.cleaned_data.get("room_type")
            price = form.cleaned_data.get("price")
            guests = form.cleaned_data.get("guests")
            bedrooms = form.cleaned_data.get("bedrooms")
            beds = form.cleaned_data.get("beds")
            baths = form.cleaned_data.get("baths")
            instant_book = form.cleaned_data.get("instant_book")
            superhost = form.cleaned_data.get("superhost")
            amenities = form.cleaned_data.get("amenities")
            facilities = form.cleaned_data.get("facilities")

            filter_args = {}

            if city != "Anywhere":
                filter_args["city__startswith"] = city
            if country is not None:
                filter_args["country"] = country
            if room_type is not None:
                filter_args["room_type"] = room_type
            if price is not None:
                filter_args["price__lte"] = price
            if guests is not None:
                filter_args["guests__gte"] = guests
            if bedrooms is not None:
                filter_args["bedrooms__gte"] = bedrooms
            if beds is not None:
                filter_args["beds__gte"] = beds
            if baths is not None:
                filter_args["baths__gte"] = baths
            if instant_book is True:
                filter_args["instant_book"] = True
            if superhost is True:
                filter_args["superhost"] = True
            rooms = room_models.Room.objects.filter(**filter_args).order_by("-created")
            if len(amenities) > 0:
                rooms = rooms.filter(amenities__in=amenities)
                rooms_selected = (
                    rooms.values("id")
                    .annotate(total=Count("id"))
                    .filter(total=amenities.count())
                )
                rooms_id = [room.get("id") for room in rooms_selected]
                rooms = room_models.Room.objects.filter(id__in=rooms_id)
            if len(facilities) > 0:
                rooms = rooms.filter(facilities__in=facilities)
                rooms_selected = (
                    rooms.values("id")
                    .annotate(total=Count("id"))
                    .filter(total=facilities.count())
                )
                rooms_id = [room.get("id") for room in rooms_selected]
                rooms = room_models.Room.objects.filter(id__in=rooms_id)
            return render(
                request, "rooms/search.html", context={"form": form, "rooms": rooms}
            )

    else:
        form = SearchForm()
    return render(request, "rooms/search.html", context={"form": form})
