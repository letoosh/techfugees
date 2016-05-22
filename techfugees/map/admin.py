from django.contrib import admin, messages
from django.http import Http404
from django.shortcuts import redirect
from django.conf import settings
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials
from map.utils import google_spreadsheet_row_to_trip

from .models import Trip


class TripAdmin(admin.ModelAdmin):
    list_display = ['start_country', 'end_country', 'year', 'price', 'ccy']

admin.site.register(Trip, TripAdmin)


def sync_google_data(request):
    if not request.user.is_authenticated() or not request.user.is_staff:
        raise Http404()

    scope = ['https://spreadsheets.google.com/feeds']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        os.path.join(settings.BASE_DIR, settings.GOOGLE_JSON_CREDENTIALS),
        scope
    )

    gc = gspread.authorize(credentials)

    wks = gc.open_by_url(settings.GOOGLE_SPREADSHEET_URL).sheet1

    rows = wks.get_all_values()

    Trip.objects.all().delete()

    for row in rows[2:]:
        google_spreadsheet_row_to_trip(row).save()

    messages.success(request, "Synced ${0} rows".format(len(rows) - 2))

    return redirect('/admin/')

admin.site.register_view('sync', 'Sync Google Data', view=sync_google_data)