from django.http.response import Http404
from django.utils import timezone
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.edit import FormView
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from users import mixins as user_mixins
from . import models
from rooms import models as room_models
from .forms import SearchForm, CreatePhotoForm


class HomeView(ListView):
    model = models.Room
    template_name = "rooms/rooms_list.html"
    context_object_name = "rooms"
    paginate_by = 12
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


class EditRoomView(user_mixins.LoginOnlyView, UpdateView):
    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404
        return room


class RoomPhotosView(user_mixins.LoginOnlyView, RoomDetail):
    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404
        return room


@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Cant delete that photo")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo Delted")
    except models.Room.DoesNotExist:
        return redirect("core:home")
    return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))


class EditPhotoView(user_mixins.LoginOnlyView, UpdateView):

    model = models.Photo
    pk_url_kwarg = "photo_pk"
    template_name = "rooms/photo_edit.html"
    fields = ("caption",)

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        messages.success(self.request, "Photo Updated")
        return reverse("rooms:photos", args=[room_pk])


class AddPhotoView(user_mixins.LoginOnlyView, FormView):
    model = models.Photo
    template_name = "rooms/photo_create.html"
    fields = ("caption", "file")
    form_class = CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request,"Photo Uploaded")
        return redirect(reverse("rooms:photos", args=[pk]))
