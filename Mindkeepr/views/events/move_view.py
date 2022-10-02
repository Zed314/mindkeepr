
from . import EventViewModal
from Mindkeepr.forms.events import MoveEventForm

class MoveEventViewModal(EventViewModal):
    template_name = 'events/move-event-detail-modal.html'
    permission_required = "Mindkeepr.add_moveevent"
    form_class = MoveEventForm
    success_url = '/formmoveeventmodal'