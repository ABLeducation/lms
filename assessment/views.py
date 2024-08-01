from django.shortcuts import render,redirect
from django.views.generic import ListView
from .models import *
from django.http import JsonResponse
import math
# Create your views here.

class QuizView(ListView):
    model=Quiz
    template_name='quizes/main.html'
    
    def get_queryset(self):
        # Assuming you have a way to identify the logged-in student and their grade
        user=self.request.user
        student =user_profile_student.objects.get(user=user)
        student_grade=student.grade

        # Filter quizzes based on the student's grade
        queryset = Quiz.objects.filter(grade=student_grade)
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
    return JsonResponse({'data':question,
                         'time':quiz.time})
                         

def quiz_data_save(request,pk):
    if request.is_ajax():
        questions=[]
        data=request.POST
        data_=dict(data.lists())
        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key', k)
            question=Question.objects.get(text=k)
            questions.append(question)

        user=request.user
        quiz=Quiz.objects.get(pk=pk)

        score=0
        multiplier=100/quiz.no_of_question
        results=[]
        correct_answer=None

        for q in questions:
            a_selected=request.POST.get(q.text)

            if a_selected != "":
                question_answers=Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score +=1
                            correct_answer=a.text
                    else:
                        if a.correct:
                            correct_answer=a.text
                results.append({str(q):{"correct_answer":correct_answer, "answered":a_selected}})
            else:
                results.append({str(q):'not answered'})
        score_=score*multiplier
        Result.objects.create(quiz=quiz,user=user,score=score_)

        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({"passed":True, "score":score_, "results":results})
        else:
            return JsonResponse({"passed":False, "score":score_,"results":results})


        