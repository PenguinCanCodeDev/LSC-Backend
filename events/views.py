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
    - Only events where `happening_when` is **greater than the current time**
      are returned.
    - Past events are automatically excluded.

    **Fields Returned:**

    - **title** → Name of the event
    - **happening_when** → Date and time the event will occur
    - **thumbnail** → Event image URL (hosted on Cloudinary)
    - **event_type** → Type of event (e.g. trame session or holiday task)
    - **tag** → Tag associated with the event (e.g. lsc, l300)
    - **level** → Student level the event is meant for
    - **created_when** → Date the event was created

    **Authentication:** Not required.
    """,
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
                            "event_type": "TRAME_SESSION",
                            "tag": "L300",
                            "level": "L300",
                            "created_when": "2026-03-01T10:30:00Z"
                        },
                        {
                            "title": "Holiday Coding Task",
                            "happening_when": "2026-03-20T09:00:00Z",
                            "thumbnail": "https://res.cloudinary.com/example/image/upload/event_images/holiday_task.jpg",
                            "event_type": "HOLIDAY_TASK",
                            "tag": "LSC",
                            "level": "L300",
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

    # get events whose time and date of occurence have not passed
    events = Event.objects.filter(happening_when__gt=timezone.now())
    serializer = EventSerializer(events, many=True)

    return Response({
        'status': True,
        'message': 'Events retrieved successfully',
        'data': serializer.data
    }, status=status.HTTP_200_OK)