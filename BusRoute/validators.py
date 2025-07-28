import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_24_hour_format(value):
    if not re.match(r'^([01]\d|2[0-3])[0-5]\d$', value):
        raise ValidationError(
            _('%(value)s is not a valid time in HHMM format'),
            params={'value': value},
        )