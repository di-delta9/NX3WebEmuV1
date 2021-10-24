#!/usr/bin/python3
from django.core.management.base import BaseCommand, CommandError
from NX3.models import Profile,ProfileStep
import os,sys,json


class Command(BaseCommand):
    help = 'Imports the specified json spectrum profile into the Emulator\'s System profiles.'

    def add_arguments(self, parser):
        parser.add_argument('profile_file', nargs='+', type=str)

    def handle(self, *args, **options):
        fname = options['profile_file'][0]
        with open(fname) as f:
            data = json.loads(f.read())
            f.close();
            self.stdout.write(self.style.MIGRATE_HEADING('Loading profile "%s" into System Spectrums...' % data['name']))
            prof = Profile.objects.get_or_create(label=data["name"],profile_id=data["id"])
            objects = ProfileStep.objects.filter(profile=prof[0].id)
            objects.delete()
            for step in data["steps"]:
                step_item = ProfileStep.objects.get_or_create(profile=prof[0],start=step["start"],end=step["end"],b=step["b"],g=step["g"],r=step["r"],f=step["f"])
                self.stdout.write(self.style.MIGRATE_LABEL('STEP Starting at "%s" and Ending at "%s" added...'%(step['start'],step["end"])))
            self.stdout.write(self.style.SUCCESS('Profile "%s" loaded into System Spectrums...' % data['name']))


