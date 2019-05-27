from django.db import models

class Link(models.Model):
    id =            models.AutoField(primary_key=True)
    url =           models.URLField(unique=True)
    display_name =  models.CharField(max_length=256)

class Person(models.Model):
    id =            models.AutoField(primary_key=True)
    ma_id =         models.IntegerField(unique=True)
    ma_link =       models.ForeignKey(Link, on_delete=models.CASCADE)

class Lable(models.Model):
    id =            models.AutoField(primary_key=True)
    ma_id =         models.IntegerField(unique=True)
    ma_link =       models.ForeignKey(Link, on_delete=models.CASCADE)
    address =       models.CharField(max_length=256)
    country =       models.CharField(max_length=256)
    phone_number =  models.CharField(max_length=256)
    status =        models.CharField(max_length=256)
    specialised_in =models.CharField(max_length=256)
    founding_date = models.DateField(max_length=256)
    online_shopping=models.CharField(max_length=256)
    email =         models.EmailField()
    website =       models.ForeignKey(Link, on_delete=models.CASCADE)
    links =         models.ManyToManyField(Link)
    notes =         models.TextField(blank=True)


class Band(models.Model):
    id =            models.AutoField(primary_key=True)
    ma_id =         models.IntegerField(unique=True)
    ma_link =       models.ForeignKey(Link, on_delete=models.CASCADE)
    name =          models.CharField(max_length=256)
    band_members =  models.ManyToManyField(Person,through='Membership')
    country =       models.CharField(max_length=256)
    location =      models.CharField(max_length=256)
    formed =        models.CharField(max_length=256)
    years_active =  models.CharField(max_length=256)
    genre =         models.CharField(max_length=256)
    themes =        models.CharField(max_length=256)
    status =        models.CharField(max_length=256)
    last_label =    models.ForeignKey(Lable, on_delete=models.CASCADE)
    albums =        models.ManyToManyField(Album, on_delete=models.CASCADE)
    description =   models.TextField(blank=True)
    links =         models.ManyToManyField(Link)


class Album(models.Model):
    id =            models.AutoField(primary_key=True)
    ma_id =         models.IntegerField(unique=True)
    ma_link =       models.ForeignKey(Link, on_delete=models.CASCADE)
    name =          models.CharField(max_length=256)
    type =          models.CharField(max_length=256)
    release_date =  models.DateField()
    catalog_id =    models.CharField(max_length=256)
    label =         models.ForeignKey(Lable, on_delete=models.CASCADE)
    format =        models.CharField(max_length=256)
    notes =         models.TextField(blank=True)
    duration =      models.DurationField()
    band_members =  models.ManyToManyField(Person,through='Worked_on')
    Miscellaneous_staff = models.ManyToManyField(Person,through='Worked_on')

class Song(models.Model):
    id =            models.AutoField(primary_key=True)
    ma_id =         models.IntegerField(unique=True)
    ma_link =       models.ForeignKey(Link,on_delete=models.CASCADE)
    name =          models.CharField(max_length=256)
    album =         models.ForeignKey(Album, on_delete=models.CASCADE)
    duration_s =    models.DurationField()
    lyrics =        models.TextField(blank=True)

class Worked_on(models.Model):
    album =        models.ForeignKey(Album, on_delete=models.CASCADE)
    person =       models.ForeignKey(Person, on_delete=models.CASCADE)
    position =     models.CharField(max_length=256)

class Membership(models.Model):
    band =         models.ForeignKey(Band, on_delete=models.CASCADE)
    person =       models.ForeignKey(Person, on_delete=models.CASCADE)
    position =          models.CharField(max_length=256)
    started =      models.DateField()
    ended =        models.DateField()
