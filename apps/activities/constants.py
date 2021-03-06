class RequestStatus:
    APPROVED = 'approved'
    PENDING = 'pending'
    DENIED = 'denied'

    CHOICES = (
        (APPROVED, 'Approved'),
        (PENDING, 'Pending'),
        (DENIED, 'Denied')
    )


class ActivityFormat:
    INDIVIDUAL = 'individual'
    GROUP = 'group'
