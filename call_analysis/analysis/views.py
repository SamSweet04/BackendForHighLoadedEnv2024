from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
import speech_recognition as sr
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from .models import CallRecord

class UploadAudio(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        try:
            audio = request.FILES['file']
            call_record = CallRecord.objects.create(audio_file=audio)

            # Распознавание речи
            recognizer = sr.Recognizer()
            with sr.AudioFile(call_record.audio_file.path) as source:
                audio_data = recognizer.record(source)
                transcription = recognizer.recognize_google(audio_data, language='ru-RU')
                call_record.transcription = transcription

            # Анализ тональности
            analyzer = SentimentIntensityAnalyzer()
            sentiment = analyzer.polarity_scores(transcription)
            call_record.sentiment = sentiment
            call_record.save()

            return Response({"transcription": transcription, "sentiment": sentiment})

        except sr.UnknownValueError:
            return Response({"error": "Речь не распознана"}, status=status.HTTP_400_BAD_REQUEST)
        except sr.RequestError:
            return Response({"error": "Ошибка сервиса распознавания речи"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
