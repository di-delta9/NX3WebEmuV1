from django.db import models
from django.contrib import admin
# This class defines how to store (System)Profiles and their steps as if the Web Emulator were a working fixture:
# Main Model: The Profile, which has 1 or more Steps below:

class Profile(models.Model):
    profile_id = models.TextField(max_length=200,verbose_name='Profile Label')
    label = models.TextField(max_length=200,verbose_name='Profile Label')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Profile Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Profile Updated')
    steps = models.IntegerField(verbose_name='steps',null=True,blank=True,default=0)
    def __str__(self):
        return "Spectrum Profile: "+self.label
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

# Submodel :Profile Steps.      
class ProfileStep(models.Model):
    profile = models.ForeignKey(Profile,verbose_name = 'Profile',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Step Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Step Updated')
    start = models.TextField(verbose_name='Step Start')
    end = models.TextField(verbose_name='Step End')
    b = models.IntegerField(verbose_name='Blue PCT',null=True,blank=True,default=0)
    r = models.IntegerField(verbose_name='Deep Red PCT',null=True,blank=True,default=0)
    g = models.IntegerField(verbose_name='Green PCT',null=True,blank=True,default=0)
    f = models.IntegerField(verbose_name='Far Red PCT',null=True,blank=True,default=0)
    def __str__(self):
        return "Spectrum Profile: {name}, Start: {start}, End: {end}, B:{B}%, R:{R}%, G:{G}%, F:{F}%".format(name=self.profile.label,start=self.start,end=self.end,B=self.b,R=self.r,G=self.g,F=self.r)
@admin.register(ProfileStep)
class ProfileStepAdmin(admin.ModelAdmin):
    pass      

# This class defines how to store (User) Profiles and their steps as if the Web Emulator were a working fixture:
# User profiles are named as UserProfile and their step is UserStepProfile, respectively.
# Main Model: The Profile, which has 1 or more Steps below:
class UserProfile(models.Model):
    profile_id = models.TextField(max_length=200,verbose_name='Profile Label')
    label = models.TextField(max_length=200,verbose_name='Profile Label')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Profile Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Profile Updated')
    steps = models.IntegerField(verbose_name='steps',null=True,blank=True,default=0)
    def __str__(self):
        return "User Spectrum Profile: "+self.label
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass  

# Submodel :Profile Steps.      
class UserProfileStep(models.Model):
    profile = models.ForeignKey(UserProfile,verbose_name = 'Profile',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Step Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Step Updated')
    start = models.TextField(verbose_name='Step Start')
    end = models.TextField(verbose_name='Step End')
    b = models.IntegerField(verbose_name='Blue PCT',null=True,blank=True,default=0)
    r = models.IntegerField(verbose_name='Deep Red PCT',null=True,blank=True,default=0)
    g = models.IntegerField(verbose_name='Green PCT',null=True,blank=True,default=0)
    f = models.IntegerField(verbose_name='Far Red PCT',null=True,blank=True,default=0)
    def __str__(self):
        return "User Spectrum Profile: {name}, Start: {start}, End: {end}, B:{B}%, R:{R}%, G:{G}%, F:{F}%".format(name=self.profile.label,start=self.start,end=self.end,B=self.b,R=self.r,G=self.g,F=self.r)

@admin.register(UserProfileStep)
class UserProfileStepAdmin(admin.ModelAdmin):
    pass        




# System State model, holds a persistent device state just like the real device would:
class SystemState(models.Model):
    state_id = models.IntegerField(verbose_name='State ID',null=True,blank=True,default=0)
    profile = models.ForeignKey(Profile,verbose_name = 'Profile',on_delete=models.RESTRICT,null=True)
    profileStep = models.ForeignKey(ProfileStep,verbose_name = 'Profile Step',on_delete=models.RESTRICT,null=True)
    userProfile = models.ForeignKey(UserProfile,verbose_name = 'User Profile',on_delete=models.RESTRICT,null=True)
    userProfileStep = models.ForeignKey(UserProfileStep,verbose_name = 'User Profile Step',on_delete=models.RESTRICT,null=True)
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Step Updated')
    signal = models.IntegerField(verbose_name='Signal Strenght',null=True,blank=True,default=0)
    ap = models.TextField(verbose_name='Wifi ESSID',null=True,blank=True,default='WiFi Network')
    sta = models.TextField(verbose_name='STA/AP Mode',null=True,blank=True,default='STA')
    gw = models.TextField(verbose_name='Gateway Address',null=True,blank=True,default=0)
    v48 = models.DecimalField(verbose_name='48V Bus Voltage',null=True,blank=True,default=0,decimal_places=2,max_digits=5)
    t1 = models.DecimalField(verbose_name='PCB 1 Temp',null=True,blank=True,default=0,decimal_places=2,max_digits=5)
    t2 = models.DecimalField(verbose_name='PCB 2 Temp',null=True,blank=True,default=0,decimal_places=2,max_digits=5)
    t3 = models.DecimalField(verbose_name='PCB 3 Temp',null=True,blank=True,default=0,decimal_places=2,max_digits=5)
    fan = models.DecimalField(verbose_name='Fan Power',null=True,blank=True,default=0,decimal_places=2,max_digits=5)
    def __str__(self):
        return "Current System State: Profile: {name}, SIG: {SIG}, AP: {AP}, STA: {STA}, GW: {GW}, V48: {V48}, T1: {T1}, T2: {T2}, T3: {T3}, FAN: {FAN}%".format(name=self.profile.label,AP=self.ap,SIG=self.signal,STA=self.sta,GW=self.gw,V48=self.v48,T1=self.t1,T2=self.t2,T3=self.t3,FAN=self.fan)
@admin.register(SystemState)
class SystemStateAdmin(admin.ModelAdmin):
    pass      
