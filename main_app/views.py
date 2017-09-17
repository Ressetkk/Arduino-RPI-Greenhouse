from django.shortcuts import render
from .models import Sensors
from .models import Buttons
from .forms import UpdateFieldsForm
from django.http import HttpResponse, HttpResponseRedirect
import sqlite3 as lite

# Create your views here.

def index(request):
    sensor_data = Sensors.objects.all()
    button_data = Buttons.objects.all()

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UpdateFieldsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            con = lite.connect('/home/pi/szklarnia/db.sqlite3')
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            cur = con.cursor()
            data = form.cleaned_data
            data_parsed = [int(data['temp_val']), int(data['hum_val']), int(data['temp_range'])]
            if data['led_power'] == 'True':
                data_parsed.append(1)
            else:
                data_parsed.append(0)
            cur.execute("update main_app_sensors set value=%s where id=4" %data_parsed[0])
            cur.execute("update main_app_sensors set value=%s where id=5" %data_parsed[1])
            cur.execute("update main_app_sensors set value=%s where id=6" %data_parsed[2])
            cur.execute("update main_app_buttons set state=%s where id=0" %data_parsed[3])
            con.commit()
            return HttpResponseRedirect('#')

    else:
        form = UpdateFieldsForm()

    return render(request, 'index.html', {'sensor_data':sensor_data, 'button_data':button_data, 'form':form})
