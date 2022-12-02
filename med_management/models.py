from django.db import models

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

class Medical_history(models.Model):

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

    appointment_reason = models.CharField(('Appointment reason'), max_length=30, blank=True)
    appointment_date = models.DateTimeField(('Appointment date'), auto_now_add=True)
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