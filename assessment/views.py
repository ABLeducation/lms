from django.shortcuts import render,redirect
from django.views.generic import ListView
from .models import *
from django.http import JsonResponse
import math
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.pagesizes import letter # type: ignore
from reportlab.pdfgen import canvas # type: ignore
from io import BytesIO
from django.core.files.base import ContentFile
import os
from django.conf import settings
from PyPDF2 import PdfReader, PdfWriter # type: ignore

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

def generate_certificate(user, quiz, score, passed,date_attempted):
    if passed:
        template_filename = 'certificate_e.pdf'  # For scores greater than or equal to passing score
    else:
        template_filename = 'certificate_c.pdf'
    # Create a temporary PDF with details to overlay on the template
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 22)
    student_profile = user_profile_student.objects.get(user=user)

    # Construct the full name from the profile model
    student_name = f"{student_profile.first_name} {student_profile.last_name}"

    
    # Draw text onto the temporary PDF
    # c.drawString(100, 750, "Certificate of Achievement")
    c.drawString(400, 410, student_name)  # Adjust the coordinates as necessary
    c.drawString(390, 342, f"{quiz.grade}")
    c.drawString(400, 290, f"{quiz.name}")
    c.drawString(420, 236, f"{score:.2f}%")
    c.drawString(405, 157, f"{date_attempted.strftime('%d-%m-%Y')}")
    
    c.save()
    buffer.seek(0)
    
    # Load the template PDF
    template_path = os.path.join(settings.MEDIA_ROOT, template_filename)
    template_reader = PdfReader(template_path)
    template_writer = PdfWriter()
    
    # Overlay the content on the template PDF
    template_page = template_reader.pages[0]
    overlay_pdf = PdfReader(buffer)
    overlay_page = overlay_pdf.pages[0]
    
    template_page.merge_page(overlay_page)
    template_writer.add_page(template_page)
    
    # Save the final PDF to a buffer
    final_buffer = BytesIO()
    template_writer.write(final_buffer)
    final_buffer.seek(0)
    
    filename = f"{user.username}_{quiz.name}_certificate.pdf"
    return ContentFile(final_buffer.getvalue(), filename)

@csrf_exempt
def quiz_data_save(request, pk):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = request.POST
        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')

        score = 0
        multiplier = 100 / quiz.no_of_question  # Calculate the percentage multiplier based on the total number of questions
        results = []
        correct_answer = None
        answered_questions = set()  # To keep track of the questions already processed

        for k, v in data_.items():
            # Use filter() to allow multiple questions with the same text
            questions = Question.objects.filter(text=k)
            if questions.exists():
                for question in questions:
                    # Ensure each question is only processed once
                    if question.id not in answered_questions:
                        answered_questions.add(question.id)
                        a_selected = v[0]  # Get the first answer from the user input

                        if a_selected:
                            question_answers = Answer.objects.filter(question=question)
                            for a in question_answers:
                                if a_selected == a.text and a.correct:
                                    score += 1
                                    correct_answer = a.text
                            results.append({str(question): {"correct_answer": correct_answer, "answered": a_selected}})
                        else:
                            results.append({str(question): 'not answered'})
            else:
                results.append({k: 'Question not found'})

        # Ensure the score does not exceed 100%
        score_ = min(score * multiplier, 100)  # Ensure score cannot exceed 100%

        result = Result.objects.create(quiz=quiz, user=user, score=score_)

        # Check if the user passed the quiz
        passed = score_ >= quiz.required_score_to_pass
        certificate_file = generate_certificate(user, quiz, score_, passed, result.date_attempted)
        result.certificate.save(certificate_file.name, certificate_file)

        return JsonResponse({"passed": passed, "score": score_, "results": results})
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)

