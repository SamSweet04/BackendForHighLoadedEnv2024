import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from kvstore.models import KeyValue
from kvstore.serializers import KeyValueSerializer

OTHER_INSTANCES = ["http://django1:8000", "http://django2:8000"]

class KeyValueView(APIView):
    def post(self, request):
        serializer = KeyValueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, key=None):
        try:
            kv = KeyValue.objects.get(key=key)
            serializer = KeyValueSerializer(kv)
            return Response(serializer.data)
        except KeyValue.DoesNotExist:
            return Response({"error": "Key not found"}, status=status.HTTP_404_NOT_FOUND)


class QuorumKeyValueView(APIView):
    def post(self, request):
        serializer = KeyValueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            successful_writes = 1

            # Attempt to write to other instances
            for instance in OTHER_INSTANCES:
                try:
                    response = requests.post(f"{instance}/api/kv/", json=request.data)
                    if response.status_code == status.HTTP_201_CREATED:
                        successful_writes += 1
                except requests.ConnectionError:
                    pass

            if successful_writes >= 2:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"error": "Failed to reach write quorum"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, key=None):
        try:
            kv = KeyValue.objects.get(key=key)
            serializer = KeyValueSerializer(kv)
            data = serializer.data
        except KeyValue.DoesNotExist:
            data = None

        successful_reads = [data] if data else []
        for instance in OTHER_INSTANCES:
            try:
                response = requests.get(f"{instance}/api/kv/{key}/")
                if response.status_code == status.HTTP_200_OK:
                    successful_reads.append(response.json())
            except requests.ConnectionError:
                pass

        if len(successful_reads) >= 2:
            return Response(successful_reads[0], status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to reach read quorum"}, status=status.HTTP_404_NOT_FOUND)
