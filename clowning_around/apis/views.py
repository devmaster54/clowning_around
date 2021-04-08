from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from clowning_around.apis.serializers import (
    AppointmentSerializer,
    RequestContactSerializer,
    ReportIssueSerializer,
    RateEmojiSerializer,
    AppointmentUpdateSerializer,
)
from clowning_around.apis.models import AppointmentModel


class AppointmentApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            if user.is_client:
                queryset = (
                    AppointmentModel.objects.filter(client__user=user)
                    .exclude(status=2)
                    .exclude(status=4)
                )
            elif user.is_clown:
                queryset = AppointmentModel.objects.filter(clown__user=user)
            else:
                raise Exception("You are not allowed.")
            res_data = AppointmentSerializer(queryset, many=True).data
            return Response(
                {"success": True, "data": res_data}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request, *args, **kwargs):
        try:

            serializer = AppointmentSerializer(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            res_data = serializer.save()
            return Response(
                {"success": True, "data": res_data}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, *args, **kwargs):
        try:
            serializer = AppointmentUpdateSerializer(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            res_data = serializer.save()
            return Response(
                {"success": True, "data": res_data}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class RequestContactApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            serializer = RequestContactSerializer(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            res_data = serializer.save()
            return Response(
                {"success": True, "data": res_data}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class ReportIssueApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            serializer = ReportIssueSerializer(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"success": True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class RateEmojiApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            serializer = RateEmojiSerializer(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"success": True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

