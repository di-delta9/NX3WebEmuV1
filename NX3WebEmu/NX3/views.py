from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
import netifaces
from datetime import datetime
from dateutil import tz
from .models import Profile,ProfileStep,UserProfile,UserProfileStep,SystemState
from .functions import StepFunctions
import json
# Create your views here.
# Generic Dashboard landing page view:
def dashboard(request):
    context = {}
    return render(request,"dashboard.html",context)
# API calls: 
# /api/hdr.json: Dashboard header call:
def api_hdr(request):
    
    data = {"sys":{
            "ip":str(netifaces.ifaddresses(netifaces.interfaces()[1])[netifaces.AF_INET][0]['addr']),
            "mac":str(netifaces.ifaddresses(netifaces.interfaces()[1])[netifaces.AF_LINK][0]['addr']),
            "time":datetime.now(tz = tz.tzlocal()).strftime("%H:%M")
    }}
    return JsonResponse(data,safe=False)

# /api/spec/profile.csv: Profile CSV for spectrum data update in dashboard:
def api_profile(request):
    state,created = SystemState.objects.get_or_create(state_id=0)
    if (state.userProfile is not None):
        step = StepFunctions.user_select_step(StepFunctions,state.userProfile)
        returnstr = "{S},{W},{P},{I},{M},{K}".format(S=state.userProfile.label,W='u',P=step.b,I=step.r,M=step.g,K=step.f)
    else:
        step = StepFunctions.select_step(StepFunctions,state.profile)
        returnstr = "{S},{W},{P},{I},{M},{K}".format(S=state.profile.label,W='s',P=step.b,I=step.r,M=step.g,K=step.f)
    return HttpResponse(returnstr)


# /api/spec/profiles.json: Get all available system and user profiles:
def api_profiles(request):
    data = {"s":[],"u":[]}
    profs = Profile.objects.all()
    for p in profs:
        data["s"].append({"i":p.profile_id,"l":p.label,"s":False})
    profs = UserProfile.objects.all()
    for p in profs:
        data["u"].append({"i":p.profile_id,"l":p.label,"s":False})
    return JsonResponse(data,safe=False)

# /api/sensors/conn.csv: Connectivity sensors CSV for data update in dashboard:
def api_conn(request):
    state,created = SystemState.objects.get_or_create(state_id=0)
    
    ipaddr = str(netifaces.ifaddresses(netifaces.interfaces()[1])[netifaces.AF_INET][0]['addr'])
    returnstr = "{S},{W},{P},{I},{M}".format(S=state.sta,W=state.ap,P=state.signal,I=ipaddr,M=state.gw)
    return HttpResponse(returnstr)

# /api/spec/power.csv: Power CSV for data update in dashboard:
def api_power(request):
    state,created = SystemState.objects.get_or_create(state_id=0)
    returnstr = "{S},{W},{P},{I},{M}".format(S=state.v48,W=state.t1,P=state.t2,I=state.t3,M=state.fan)
    return HttpResponse(returnstr)

# /api/spec/set.json: API hook to set the profile / state to the fixture:
def api_spec_set(request):
    if "load" not in request.POST:
        return HttpResponse('{"stat":"profile-not-specified"}')
    lprof = request.POST["load"].split("_")
    state,created = SystemState.objects.get_or_create(state_id=0)
    if (lprof[0] == "s"):
        try:
            profile = Profile.objects.get(profile_id=lprof[1])
            state.userProfile = None
            state.profile = profile
            state.save()
        except Exception as e:
            print(e)
            return HttpResponse('{"stat":"profile-not-found"}')
    elif (lprof[0] == "u"):
        try:
            profile = UserProfile.objects.get(profile_id=lprof[1])
            state.userProfile = profile
            state.profile = None
            state.save()
        except Exception as e:
            print(e)
            return HttpResponse('{"stat":"profile-not-found"}')

    
    return HttpResponse('{"stat":"ok"}')

# PROFILE VIEWER / EDITOR api calls:
# /prb/[profile_id].json: Get System provided spectrum profile:
def getprb(request,lprof):
    try:
        profile = Profile.objects.get(profile_id=lprof)
    except Exception as e:
        print(e)
        return HttpResponse('{"stat":"profile-not-found"}') 
    data = {
        "type":"profile",
        "id":lprof,
        "name":profile.label,
        "steps":[]
    }
    steps = ProfileStep.objects.filter(profile=profile)
    for step in steps:
        sdata = {"start":step.start,"end":step.end,"b":step.b,"r":step.r,"g":step.g,"f":step.f}
        data["steps"].append(sdata)
    data["count"]= steps.count()
    return JsonResponse(data,safe=False)

# /pru/[profile_id].json: Get User provided spectrum profile:
def getpru(request,lprof):
    try:
        profile = UserProfile.objects.get(profile_id=lprof)
    except Exception as e:
        print(e)
        return HttpResponse('{"stat":"profile-not-found"}') 
    data = {
        "type":"profile",
        "id":lprof,
        "name":profile.label,
        "steps":[]
    }
    steps = UserProfileStep.objects.filter(profile=profile)
    for step in steps:
        sdata = {"start":step.start,"end":step.end,"b":step.b,"r":step.r,"g":step.g,"f":step.f}
        data["steps"].append(sdata)
    data["count"]= steps.count()
    return JsonResponse(data,safe=False)

# SAVE user profile:
def api_spec_create(request):
    #prof = Profile.objects.get_or_create(label=data["name"],profile_id=data["pid"])
    data = json.loads(request.POST["pdata"])
    prof = UserProfile.objects.get_or_create(label=data["name"],profile_id=data["id"])
    objects = UserProfileStep.objects.filter(profile=prof[0].id)
    objects.delete()
    for step in data["steps"]:
        step_item = UserProfileStep.objects.get_or_create(profile=prof[0],start=step["start"],end=step["end"],b=step["b"],g=step["g"],r=step["r"],f=step["f"])
    return HttpResponse('ok') 
    
# Dashboard pages:
# Dashboard landing:
def dashboard_db(request):
    context = {}
    return render(request,"dash.html",context)

#Dashboard spectrum select:
def dashboard_db_spselect(request):
    context = {}
    return render(request,"sp_select.html",context)


#Dashboard current spectrum:
def dashboard_db_spoutput(request):
    context = {}
    return render(request,"sp_output.html",context)

#Spectrum Viewer (Defaults... from old name):
def dashboard_db_spdefaults(request):
    context = {}
    return render(request,"sp_defaults.html",context)

#Spectrum Editor 
def dashboard_db_spedit(request):
    context = {}
    return render(request,"sp_editor.html",context)

