from django.db import models

class TeacherHourPreset(models.Model):
    # preset_id = models.BigAutoField(primary_key=True)
    # discipline = models.ForeignKey(Discipline, on_delete=models.PROTECT)
    # date_from = models.DateField()
    # date_to = models.DateField()
    # settings_json = models.JSONField(default=dict, blank=True)
    # is_active = models.BooleanField(default=True)
    #
    # class Meta:
    #     db_table = "op_teacher_hour_preset"
    #     constraints = [models.CheckConstraint(
    #         check=Q(date_from__lte=models.F("date_to")),
    #         name="ck_preset_period_valid",
    #     )]
    pass