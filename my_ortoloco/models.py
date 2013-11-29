import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from django.core import validators
from django.core.exceptions import ValidationError

import model_audit
import helpers


class Depot(models.Model):
    """
    Location where stuff is picked up.
    """
    code = models.CharField("Code", max_length=100, validators=[validators.validate_slug], unique=True)
    name = models.CharField("Depot Name", max_length=100, unique=True)
    description = models.TextField("Beschreibung", max_length=1000, default="")
    contact = models.ForeignKey("Loco", on_delete=models.PROTECT)
    weekday = models.PositiveIntegerField("Wochentag", choices=helpers.weekday_choices)

    addr_street = models.CharField("Strasse", max_length=100)
    addr_zipcode = models.CharField("PLZ", max_length=10)
    addr_location = models.CharField("Ort", max_length=50)

    def __unicode__(self):
        return u"%s" % (self.name)


class ExtraAboType(models.Model):
    """
    Types of extra abos, e.g. eggs, cheese, fruit
    """
    name = models.CharField("Name", max_length=100, unique=True)
    description = models.TextField("Beschreibung", max_length=1000)

    def __unicode__(self):
        return u"%s" % (self.name)


class Abo(models.Model):
    """
    One Abo that may be shared among several people.
    """
    depot = models.ForeignKey(Depot, on_delete=models.PROTECT)
    primary_loco = models.ForeignKey("Loco", related_name="abo_primary", null=True, blank=True)
    groesse = models.PositiveIntegerField(default=1)
    extra_abos = models.ManyToManyField(ExtraAboType, null=True, blank=True)

    def __unicode__(self):
        namelist = ["1 Einheit" if self.groesse == 1 else "%d Einheiten" % self.groesse]
        namelist.extend(extra.name for extra in self.extra_abos.all())
        return u"Abo (%s)" % (" + ".join(namelist))

    def bezieher(self):
        locos = self.locos.all()
        return ", ".join(unicode(loco) for loco in locos)

    def verantwortlicher_bezieher(self):
        loco = self.primary_loco
        return unicode(loco) if loco is not None else ""

    def haus_abos(self):
        return int(self.groesse / 10)

    def grosse_abos(self):
        return int((self.groesse % 10) / 2)

    def kleine_abos(self):
        return self.groesse % 2


class Loco(models.Model):
    """
    Additional fields for Django's default user class.
    """

    # user class is only used for logins, permissions, and other builtin django stuff
    # all user information should be stored in the Loco model
    user = models.OneToOneField(User, related_name='loco')
    
    first_name = models.CharField("Vorname", max_length=30)
    last_name = models.CharField("Nachname", max_length=30)
    email = models.EmailField()
    
    abo = models.ForeignKey(Abo, related_name="locos", null=True, blank=True)

    addr_street = models.CharField("Strasse", max_length=100, null=True, blank=True)
    addr_zipcode = models.CharField("PLZ", max_length=10, null=True, blank=True)
    addr_location = models.CharField("Ort", max_length=50, null=True, blank=True)
    birthday = models.DateField("Geburtsdatum", null=True, blank=True)
    phone = models.CharField("Telefonnr", max_length=50, null=True, blank=True)
    mobile_phone = models.CharField("Mobile", max_length=50, null=True, blank=True)

    def __unicode__(self):
        return u"%s %s (%s)" %(self.first_name, self.last_name, self.user.username)

    @classmethod
    def create(cls, sender, instance, created, **kdws):
        """
        Callback to create corresponding loco when new user is created.
        """
        if created:
            cls.objects.create(user=instance)



class Anteilschein(models.Model):
    loco = models.ForeignKey(Loco, null=True, blank=True, on_delete=models.SET_NULL)
    paid = models.BooleanField(default=False)

    def __unicode__(self):
        return u"Anteilschein #%s" % (self.id)


class Taetigkeitsbereich(models.Model):
    name = models.CharField("Name", max_length=100, validators=[validators.validate_slug], unique=True)
    description = models.TextField("Beschreibung", max_length=1000, default="")
    coordinator = models.ForeignKey(Loco, on_delete=models.PROTECT)
    locos = models.ManyToManyField(Loco, related_name="taetigkeitsbereiche")
    core = models.BooleanField("Kernbereich", default=False)

    def __unicode__(self):
        return u'%s' % self.name



class JobTyp(models.Model):
    """
    Recurring type of job.
    """
    name = models.CharField("Name", max_length=100, unique=True)
    description = models.TextField("Beschreibung", max_length=1000, default="")
    bereich = models.ForeignKey(Taetigkeitsbereich, on_delete=models.PROTECT)
    duration = models.PositiveIntegerField("Dauer in Stunden")
    location = models.CharField("Ort", max_length=100, default="")

    def __unicode__(self):
        return u'%s - %s' % (self.bereich, self.name)


class Job(models.Model):
    typ = models.ForeignKey(JobTyp, on_delete=models.PROTECT)
    slots = models.PositiveIntegerField("Plaetze")
    time = models.DateTimeField()
    earning = models.PositiveIntegerField("Bohnen pro Person", default=1)

    def __unicode__(self):
        return u'Job #%s' % (self.id)


    def freie_plaetze(self):
        return self.boehnli_set.filter(loco=None).count()


    def besetzte_plaetze(self):
        return self.slots - self.freie_plaetze()


    def get_status_bohne(self):
        boehnlis = Boehnli.objects.filter(job_id=self.id)
        participants = []
        for bohne in boehnlis:
            if bohne.loco is not None:
                participants.append(bohne.loco)
        print (100/ self.slots * participants.__len__())
        if self.slots == participants.__len__():
            return "erbse_voll.png"
        elif 100 / self.slots * participants.__len__() >= 75:
            return "erbse_fast_voll.png"
        elif 100 / self.slots * participants.__len__() >= 50:
            return "erbse_halb.png"
        else:
            return "erbse_fast_leer.png"


class Boehnli(models.Model):
    """
    Single boehnli (work unit).
    Automatically created during job creation.
    """
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    loco = models.ForeignKey(Loco, on_delete=models.PROTECT, null=True, blank=True)

    def __unicode__(self):
        return u'Boehnli #%s' % self.id

    def zeit(self):
        return self.job.time

    @classmethod
    def update(cls, sender, instance, created, **kwds):
        """
        Create and delete boehnli objects as jobs are created and have their amount of slots changed
        """
        if created:
            for i in range(instance.slots):
                cls.objects.create(job=instance)
        else:
            boehnlis = cls.objects.filter(job=instance)
            current_n = len(boehnlis)
            target_n = instance.slots
            if current_n < target_n:
                for i in range(target_n - current_n):
                    cls.objects.create(job=instance)
            elif current_n > target_n:
                to_delete = current_n - target_n
                free_boehnlis = [boehnli for boehnli in boehnlis if boehnli.loco == None]
                for boehnli in free_boehnlis[:to_delete]:
                    boehnli.delete()


#model_audit.m2m(Abo.users)
model_audit.m2m(Abo.extra_abos)
model_audit.fk(Abo.depot)
model_audit.fk(Anteilschein.loco)

signals.post_save.connect(Loco.create, sender=User)
signals.post_save.connect(Boehnli.update, sender=Job)
