from NX3.models import Profile,ProfileStep,UserProfile,UserProfileStep
from datetime import datetime
from dateutil import tz
class StepFunctions():
    def select_step(self,profile):
        if profile is False:
            print("**** ERROR, specified profile not found: {pr}****".format(pr=profile_id))
            return False
        profile_steps = ProfileStep.objects.filter(profile=profile)
        time = datetime.now(tz = tz.tzlocal())
        hour = time.strftime("%H")
        min = time.strftime("%M")
        tNow = int(hour)*60+int(min)
        for step in profile_steps:
            ts = step.start.split(":")
            tStart = (int(ts[0])*60)+int(ts[1])
            ts = step.end.split(":")
            tEnd = (int(ts[0])*60)+int(ts[1])
            if (tNow <= tEnd):
                if (tNow >= tStart):
                    return step
                        
    def user_select_step(self,profile):
        if profile is False:
            print("**** ERROR, specified user profile not found: {pr}****".format(pr=profile_id))
            return False
        profile_steps = UserProfileStep.objects.filter(profile=profile)
        time = datetime.now(tz = tz.tzlocal())
        hour = time.strftime("%H")
        min = time.strftime("%M")
        tNow = int(hour)*60+int(min)
        for step in profile_steps:
            ts = step.start.split(":")
            tStart = (int(ts[0])*60)+int(ts[1])
            ts = step.end.split(":")
            tEnd = (int(ts[0])*60)+int(ts[1])
            if (tNow <= tEnd):
                if (tNow >= tStart):
                    return step
                        
                    
                
            
        
