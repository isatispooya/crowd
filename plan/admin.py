from django.contrib import admin
from . import models


admin.site.register(models.Plan)
admin.site.register(models.DocumentationFiles)
admin.site.register(models.Appendices)
admin.site.register(models.PaymentGateway)
admin.site.register(models.Comment)
admin.site.register(models.Participant)
admin.site.register(models.DocumentationRecieve)