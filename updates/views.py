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
    - Only updates where `happening_when` is **greater than or equal to the current time** are returned.
    - Updates scheduled in the past are automatically excluded.
    - Optionally filter by `tag` query param: `?tag=l300` or `?tag=lsc`
    - Optionally filter by `type` query param: `?type=podcast`, `?type=trame session`, `?type=holiday task`

    **Update Types:**

    - **trame session** → A TRAME learning session.
    - **podcast** → A podcast release.
    - **holiday task** → A holiday assignment or task for students.

    **Tags:**

    - **l300** → Update is targeted at L300 users.
    - **lsc** → Update is targeted at LSC users.

    **Fields Returned:**

    - **title** → Title of the update
    - **type** → Category of update (trame session, podcast, or holiday task)
    - **tag** → Audience tag (l300 or lsc)
    - **happening_when** → Scheduled date and time of the update
    - **link** → Optional URL associated with this update — may be null

    **Authentication:** Not required.
    """,
    manual_parameters=[
        openapi.Parameter(
            'tag',
            openapi.IN_QUERY,
            description="Filter updates by audience: 'l300' or 'lsc'",
            type=openapi.TYPE_STRING,
            required=False,
        ),
        openapi.Parameter(
            'type',
            openapi.IN_QUERY,
            description="Filter updates by type: 'podcast', 'trame session', or 'holiday task'",
            type=openapi.TYPE_STRING,
            required=False,
        ),
    ],
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
                            "tag": "l300",
                            "happening_when": "2026-03-12T14:00:00Z",
                            "link": "https://youtube.com/live/example"
                        },
                        {
                            "title": "New Tech Podcast Episode",
                            "type": "podcast",
                            "tag": "lsc",
                            "happening_when": "2026-03-15T18:30:00Z",
                            "link": "https://open.spotify.com/episode/example"
                        },
                        {
                            "title": "Holiday Django Assignment",
                            "type": "holiday task",
                            "tag": "l300",
                            "happening_when": "2026-03-20T09:00:00Z",
                            "link": None
                        }
                    ]
                }
            }
        )
    }
)
@api_view(['GET'])
def get_updates(request):

    # Get all updates whose date and time of occurrence has not passed
    updates = Update.objects.filter(happening_when__gte=timezone.now())

    # Optional tag filter: ?tag=l300 or ?tag=lsc
    tag = request.query_params.get('tag', None)
    if tag:
        updates = updates.filter(tag__iexact=tag)

    # Optional type filter: ?type=podcast
    update_type = request.query_params.get('type', None)
    if update_type:
        updates = updates.filter(type__iexact=update_type)

    serializer = UpdateSerializer(updates, many=True)

    return Response({
        'status': True,
        'message': 'updates retrieved successfully',
        'data': serializer.data
    }, status=status.HTTP_200_OK)