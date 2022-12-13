from django.db import models
from user_authorization.models import *
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class Hospital(models.Model):

    name = models.CharField(('Hospital name'), max_length=30, blank=True)
    address = models.CharField(('Hospital name'), max_length=30, blank=True)
    phone_number = models.CharField(('Phone number'), max_length=12, blank=True)
    rating = models.FloatField(('rating'), default=0, blank=False)

    class Meta:
        verbose_name = ('hospital')
        verbose_name_plural = ('Hospitals')

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'phone_number': self.phone_number,
            'rating': self.rating,
        }


class Comment(models.Model):
    hospital_id = models.ForeignKey(Hospital, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(AdvancedUser, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(5),MinValueValidator(0)])
    approved = models.BooleanField(default=False)

    def approve(self):
        self.approved = True
        self.save()

    class Meta:
        verbose_name = ('comment')
        verbose_name_plural = ('Comment')

    def to_json(self):
        return {
            'id': self.id,
            'hospital': self.hospital_id,
            'author': self.author,
            'text': self.text,
            'rating': self.rating,
            'date_created': self.rating,
            'approved': self.approved
        }




class Specialization(models.Model):
    name = models.CharField(max_length=50)


class Medical_history(models.Model):

    profile_detail = models.ForeignKey(
                'user_authorization.ProfileDetail', on_delete=models.CASCADE, related_name='med_history',
                blank=True, null=True)
    date_of_record = models.DateTimeField(('Date of record'), auto_now_add=True)
    symptoms = models.CharField(('Symptoms of the illness'), max_length=30, blank=True)
    diagnosis = models.CharField(('Diagnosis'), max_length=30, blank=True)

    class Meta:
        verbose_name = ('medical history')
        verbose_name_plural = ('Medical history')

    def to_json(self):
        return {
            'id': self.id,
            'date_of_record': self.date_of_record,
            'symptoms': self.symptoms,
            'diagnosis': self.diagnosis,
        }


class Appointment(models.Model):

    patient = models.ForeignKey('user_authorization.AdvancedUser', on_delete=models.SET_NULL,
                    null=True, blank=True, related_name='patient_appointments')
    doctor = models.ForeignKey('user_authorization.AdvancedUser', on_delete=models.SET_NULL,
                    null=True, blank=True, related_name='doctor_appointments')
    appointment_reason = models.CharField(('Appointment reason'), max_length=30, blank=True)
    appointment_date = models.DateTimeField(('Appointment date'), null=True, blank=True)
    appointment_status = models.CharField(('Appointment status'), max_length=15, blank=True)

    class Meta:
        verbose_name = ('appointment')
        verbose_name_plural = ('Appointments')

    def to_json(self):
        return {
            'id': self.id,
            'appointment_reason': self.appointment_reason,
            'appointment_date': self.appointment_date,
            'appointment_status': self.appointment_status,
        }