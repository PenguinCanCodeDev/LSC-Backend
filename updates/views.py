from rest_framework import status
from rest_framework.response import Response
from .serializers import UpdateSerializer
from .models import Update
from rest_framework.decorators import api_view
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method="get",
    tags=["Updates"],
    operation_summary="Retrieve upcoming updates",
    operation_description="""
    Returns a list of **updates** whose scheduled date and time
    **have not yet passed**.

    **Filtering Logic:**
    - Only updates where `happening_when` is **greater than or equal to the current time**
      are returned.
    - Updates scheduled in the past are automatically excluded.

    **Update Types:**

    - **TRAME SESSION** → A TRAME learning session.
    - **PODCAST** → A podcast release.
    - **HOLIDAY TASK** → A holiday assignment or task for students.

    **Fields Returned:**

    - **title** → Title of the update
    - **type** → Category of update (trame session, podcast, or holiday task)
    - **happening_when** → Scheduled date and time of the update

    **Authentication:** Not required.
    """,
    responses={
        200: openapi.Response(
            description="Updates retrieved successfully",
            examples={
                "application/json": {
                    "status": True,
                    "message": "updates retrieved successfully",
                    "data": [
                        {
                            "title": "TRAME Backend Development Session",
                            "type": "trame session",
                            "happening_when": "2026-03-12T14:00:00Z"
                        },
                        {
                            "title": "New Tech Podcast Episode",
                            "type": "podcast",
                            "happening_when": "2026-03-15T18:30:00Z"
                        },
                        {
                            "title": "Holiday Django Assignment",
                            "type": "holiday task",
                            "happening_when": "2026-03-20T09:00:00Z"
                        }
                    ]
                }
            }
        )
    }
)
@api_view(['GET'])
def get_updates(request):

    # get all updates whose date and time of occurence has not been passed
    updates = Update.objects.filter(happening_when__gte=timezone.now())
    serializer = UpdateSerializer(updates, many=True)

    return Response({
        'status': True,
        'message': 'updates retrieved successfully',
        'data': serializer.data
    }, status=status.HTTP_200_OK)