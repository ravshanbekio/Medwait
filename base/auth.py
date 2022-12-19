from hospital.models import Doctor

class DoctorAuthentication(object):
    def authenticate(self, username=None):
        try:
            user = Doctor.objects.get(username=username)
            return user
        except Exception:
            return None
        
    def get_user(self, doctor_id):
        try:
            return Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return None