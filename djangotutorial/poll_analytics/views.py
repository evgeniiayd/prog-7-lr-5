from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from polls.models import Question, Choice


@api_view(['GET'])
def voting_stats(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        choices = Choice.objects.filter(question=question)

        total_votes = sum(choice.votes for choice in choices)
        data = {
            'question': question.question_text,
            'total_votes': total_votes,
            'options': []
        }

        for choice in choices:
            percentage = (choice.votes / total_votes) * 100 if total_votes > 0 else 0
            data['options'].append({
                'choice': choice.choice_text,
                'votes': choice.votes,
                'percentage': round(percentage, 2)
            })

        return Response(data)
    except Question.DoesNotExist:
        return Response({'error': 'Голосование не найдено'}, status=404)

import csv
from django.http import HttpResponse
import codecs

@api_view(['GET'])
def export_votes(request, question_id, forma):
    try:
        question = Question.objects.get(id=question_id)
        choices = Choice.objects.filter(question=question)

        if forma == 'json':
            data = {
                'question': question.question_text,
                'choices': [{'text': c.choice_text, 'votes': c.votes} for c in choices]
            }
            return Response(data)

        if forma == 'csv':
            # Проверка на наличие вариантов
            if not choices.exists():
                return Response({'error': 'Нет вариантов ответов'}, status=404)

            response = HttpResponse(content_type='text/csv; charset=utf-8')
            response['Content-Disposition'] = f'attachment; filename="votes_{question_id}.csv"'  # Исправлено!
            writer = csv.writer(response)
            writer.writerow(['Вариант', 'Голоса'])
            for choice in choices:
                writer.writerow([choice.choice_text, choice.votes])
            return response

    except Question.DoesNotExist:
         return Response({'error': 'Голосование не найдено'}, status=404)


import matplotlib.pyplot as plt
import base64
from io import BytesIO


@api_view(['GET'])
def vote_chart(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        choices = Choice.objects.filter(question=question)

        labels = [c.choice_text for c in choices]
        votes = [c.votes for c in choices]

        plt.figure(figsize=(6, 4))
        plt.bar(labels, votes, color='skyblue')
        plt.title(question.question_text)
        plt.xlabel('Варианты')
        plt.ylabel('Голоса')

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png).decode('utf-8')
        return Response({'chart': graphic})

    except Question.DoesNotExist:
        return Response({'error': 'Голосование не найдено'}, status=404)
