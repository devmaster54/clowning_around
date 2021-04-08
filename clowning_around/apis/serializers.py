from rest_framework import serializers
from clowning_around.apis.models import (
    AppointmentModel,
    RequestModel,
    IssueModel,
    RateEmojiModel,
)
from clowning_around.users.models import User, TroupeLeader, Client, Clown


class AppointmentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    client = serializers.CharField(required=True, write_only=True)
    clown = serializers.CharField(required=True, write_only=True)
    status = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = AppointmentModel
        fields = "__all__"

    def validate(self, data):
        super().validate(data)

        request = self.context.get("request")
        user = request.user
        if not hasattr(user, "troupeleader"):
            raise Exception("You are not Allowed to create an appointment.")

        troupe_leader = TroupeLeader.objects.get(user=user)
        total_count = AppointmentModel.objects.filter(
            clown__troupe=troupe_leader.troupe
        ).count()
        if total_count >= troupe_leader.troupe.max_capacity:
            raise Exception("You can't create more appointments.")
        if not Clown.objects.filter(
            user__username=data.get("clown"), troupe=troupe_leader.troupe
        ).exists():
            raise Exception("Invalid clown ID")
        if not Client.objects.filter(user__username=data.get("client")).exists():
            raise Exception("Invalid client ID")
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        troupe_leader = TroupeLeader.objects.get(user=user)
        clown = Clown.objects.get(
            user__username=validated_data.get("clown"), troupe=troupe_leader.troupe
        )
        client = Client.objects.get(user__username=validated_data.get("client"))
        appointment = AppointmentModel.objects.create(client=client, clown=clown)
        return {
            "id": appointment.id,
            "status": appointment.status,
            "created_at": appointment.created_at,
        }


class AppointmentUpdateSerializer(serializers.ModelSerializer):
    appointment = serializers.IntegerField(required=True, write_only=True)
    status = serializers.IntegerField(required=True, write_only=True)

    class Meta:
        model = AppointmentModel
        fields = "__all__"

    def validate(self, data):
        super().validate(data)

        request = self.context.get("request")
        user = request.user
        if not hasattr(user, "clown"):
            raise Exception("You are not Allowed")

        if not AppointmentModel.objects.filter(
            pk=data.get("appointment"), clown=user.clown
        ).exists():
            raise Exception("Invalid Params")
        if data.get("status") > 4 or data.get("status") < 1:
            raise Exception("Invalid Params")
        return data

    def create(self, validated_data):
        appointment = AppointmentModel.objects.get(pk=validated_data.get("appointment"))
        appointment.status = validated_data.get("status")
        appointment.save()
        return AppointmentSerializer(appointment).data


class ClientSerializer(serializers.ModelSerializer):
    contact_name = serializers.CharField()
    contact_email = serializers.EmailField()
    contact_number = serializers.CharField()

    class Meta:
        model = Client
        exclude = ["user"]


class RequestContactSerializer(serializers.ModelSerializer):
    appointment = serializers.IntegerField(required=True, write_only=True)
    reason = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = RequestModel
        fields = "__all__"

    def validate(self, data):
        super().validate(data)

        request = self.context.get("request")
        user = request.user
        if not hasattr(user, "clown"):
            raise Exception("You are not Allowed")

        if not AppointmentModel.objects.filter(
            pk=data.get("appointment"), clown=user.clown
        ).exists():
            raise Exception("Invalid Params")
        return data

    def create(self, validated_data):
        appointment = AppointmentModel.objects.get(pk=validated_data.get("appointment"))
        RequestModel.objects.create(
            appointment=appointment, reason=validated_data.get("reason")
        )
        return ClientSerializer(appointment.client).data


class ReportIssueSerializer(serializers.ModelSerializer):
    appointment = serializers.IntegerField(required=True, write_only=True)
    issue = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = IssueModel
        fields = "__all__"

    def validate(self, data):
        super().validate(data)

        request = self.context.get("request")
        user = request.user
        if not hasattr(user, "clown"):
            raise Exception("You are not Allowed")

        if not AppointmentModel.objects.filter(
            pk=data.get("appointment"), clown=user.clown
        ).exists():
            raise Exception("Invalid Params")
        return data

    def create(self, validated_data):
        appointment = AppointmentModel.objects.get(pk=validated_data.get("appointment"))
        IssueModel.objects.create(
            appointment=appointment, issue=validated_data.get("issue")
        )
        return validated_data


class RateEmojiSerializer(serializers.ModelSerializer):
    appointment = serializers.IntegerField(required=True, write_only=True)
    emoji = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = RateEmojiModel
        fields = "__all__"

    def validate(self, data):
        super().validate(data)

        request = self.context.get("request")
        user = request.user

        if not hasattr(user, "client"):
            raise Exception("You are not Allowed")

        if not AppointmentModel.objects.filter(
            pk=data.get("appointment"), client=user.client, status=3
        ).exists():
            raise Exception("Invalid Params")
        return data

    def create(self, validated_data):
        appointment = AppointmentModel.objects.get(pk=validated_data.get("appointment"))
        RateEmojiModel.objects.create(
            appointment=appointment, emoji=validated_data.get("emoji")
        )
        return validated_data
