from django.shortcuts import render, get_object_or_404
from .models import Standard, Ebook, Topic_name

def grade_list(request):
    grades = Standard.objects.all()
    return render(request, 'curriculum/gradelist.html', {'grades': grades})

def ebook_list(request, grade_id):
    grade = get_object_or_404(Standard, id=grade_id)
    ebooks = Ebook.objects.filter(grade=grade)
    return render(request, 'curriculum/ebook.html', {'grade': grade, 'ebooks': ebooks})

def display_lessons(request, book_id):
    book = get_object_or_404(Ebook, id=book_id)
    lessons = Topic_name.objects.filter(book=book)
    return render(request, 'curriculum/e_lesson.html', {'book': book, 'lessons': lessons})