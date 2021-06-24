from django.contrib import admin
from .models import *

#sales
admin.site.register(Account)
admin.site.register(Note)
admin.site.register(EmailTemplate)
admin.site.register(Script)
admin.site.register(VoicemailScript)

#time
admin.site.register(TimeRecord)

#leadpdf
admin.site.register(LeadPDF)

#support
admin.site.register(SupportTicket)

# sponsor cohort
admin.site.register(SponsorCohort)
#forum
admin.site.register(Comment)
admin.site.register(Discussion)

#documents
admin.site.register(Document)

#tasks
admin.site.register(Task)
