from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import EventSerializer
from .models import Event
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method="get",
    tags=["Events"],
    operation_summary="Retrieve upcoming events",
    operation_description="""
    Returns a list of **upcoming events** whose scheduled date and time
    have **not yet passed**.

    **Filtering Logic:**
    - Only events where `happening_when` is **greater than the current time** are returned.
    - Past events are automatically excluded.
    - Optionally filter by `tag` query param: `?tag=l300` or `?tag=lsc`

    **Fields Returned:**

    - **title** → Name of the event
    - **happening_when** → Date and time the event will occur
    - **thumbnail** → Event image URL (hosted on Cloudinary)
    - **link** → Optional URL (e.g. meeting link or resource) — may be null
    - **event_type** → Type of event (trame_session or holiday_task)
    - **tag** → Tag associated with the event (lsc or l300)
    - **level** → Student level the event is meant for
    - **created_when** → Date the event was created

    **Authentication:** Not required.
    """,
    manual_parameters=[
        openapi.Parameter(
            'tag',
            openapi.IN_QUERY,
            description="Filter events by tag: 'l300' or 'lsc'",
            type=openapi.TYPE_STRING,
            required=False,
        )
    ],
    responses={
        200: openapi.Response(
            description="Events retrieved successfully",
            examples={
                "application/json": {
                    "status": True,
                    "message": "Events retrieved successfully",
                    "data": [
                        {
                            "title": "TRAME Python Session",
                            "happening_when": "2026-03-15T14:00:00Z",
                            "thumbnail": "https://res.cloudinary.com/example/image/upload/event_images/python_session.jpg",
                            "link": "https://meet.google.com/abc-defg-hij",
                            "event_type": "trame_session",
                            "tag": "l300",
                            "level": "l300",
                            "created_when": "2026-03-01T10:30:00Z"
                        },
                        {
                            "title": "Holiday Coding Task",
                            "happening_when": "2026-03-20T09:00:00Z",
                            "thumbnail": "https://res.cloudinary.com/example/image/upload/event_images/holiday_task.jpg",
                            "link": None,
                            "event_type": "holiday_task",
                            "tag": "lsc",
                            "level": "l300",
                            "created_when": "2026-03-02T08:15:00Z"
                        }
                    ]
                }
            }
        )
    }
)
@api_view(['GET'])
def get_events(request):

    # Get events whose date and time of occurrence have not passed
    events = Event.objects.filter(happening_when__gt=timezone.now())

    # Optional tag filter: ?tag=l300 or ?tag=lsc
    tag = request.query_params.get('tag', None)
    if tag:
        events = events.filter(tag__iexact=tag)

    serializer = EventSerializer(events, many=True)

    return Response({
        'status': True,
        'message': 'Events retrieved successfully',
        'data': serializer.data
    }, status=status.HTTP_200_OK)