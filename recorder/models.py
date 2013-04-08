from django.db import models

# Create your models here.
class LoginRecord(models.Model):
    work_id = models.CharField(max_length=20)
    state   = models.BooleanField()
    start_time = models.DateTimeField()
    stop_time = models.DateTimeField()

    def __unicode__(self):
        return "RECORD: %s %s"%(self.work_id, self.state)


class LoginUsers(models.Model):
    user_name = models.CharField(max_length=20)
    passwd = models.CharField(max_length=8)
    work_id = models.CharField(max_length=20)
    # record = models.ForeignKey(LoginRecord)

    def get_last_record(self):
        '''state'''
        try:
            records = LoginRecord.objects.filter(work_id=self.work_id)
            return records[records.count()-1]
        except Exception, e:
            return None