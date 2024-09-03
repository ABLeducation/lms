from django.shortcuts import render,redirect
from django.views.generic import ListView
from .models import *
from django.http import JsonResponse
import math
from django.views.decorators.csrf import csrf_exempt
import logging

class QuizView(ListView):
    model=Quiz
    template_name='quizes/main.html'
    
    def get_queryset(self):
        # Assuming you have a way to identify the logged-in student and their grade
        user=self.request.user
        student =user_profile_student.objects.get(user=user)
        student_grade=student.grade
        student_school=student.school
        school=School.objects.get(name__icontains=student_school)

        # Filter quizzes based on the student's grade
        queryset = Quiz.objects.filter(grade=student_grade, schools=school)
        return queryset

def quiz_view(request,pk):
    quiz=Quiz.objects.get(pk=pk)
    return render(request, 'quizes/quizview.html', {'quiz':quiz})

def quiz_data_view(request,pk):
    quiz=Quiz.objects.get(pk=pk)
    question=[]
    for q in quiz.get_questions():
        answers=[]
        for a in q.get_answers():
            answers.append(a.text)
        question.append({str(q):answers})
    return JsonResponse({'data':question,'time':quiz.time})

@csrf_exempt
def quiz_data_save(request, pk):
    # Check if the request is an AJAX request
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = request.POST
        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        questions = []
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')

        score = 0
        multiplier = 100 / quiz.no_of_question
        results = []
        correct_answer = None

        for k, v in data_.items():
            question = Question.objects.get(text=k)
            questions.append(question)
            a_selected = v[0]  # Get the first answer

            if a_selected:
                question_answers = Answer.objects.filter(question=question)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text
                results.append({str(question): {"correct_answer": correct_answer, "answered": a_selected}})
            else:
                results.append({str(question): 'not answered'})

        score_ = score * multiplier
        Result.objects.create(quiz=quiz, user=user, score=score_)

        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({"passed": True, "score": score_, "results": results})
        else:
            return JsonResponse({"passed": False, "score": score_, "results": results})
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)