from django.shortcuts import render,HttpResponseRedirect,redirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,FormView
from .models import *
from django.urls import reverse_lazy
from .forms import CommentForm,ReplyForm, LessonForm
from django.db.models import Q
from django.views.decorators.cache import cache_page
# from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

class StandardListView(LoginRequiredMixin, ListView):
    context_object_name = 'standards'
    model = Standard
    template_name = 'curriculum/standard_list_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the user profile if it exists
        try:
            user_profile = user_profile_student.objects.get(user=self.request.user)
            grade = user_profile.grade
            school = user_profile.school

            # Define the first context
            list1 = ["Sparsh Global School,Greater Noida", "JP International School,Greater Noida", "SPS,Sonipat"]
            list2 = ["Vivekanand School,Anand Vihar"]

            if school in list1:
                valid_grades = range(1, 10)
                grades = [g for g in valid_grades]

            elif school in list2:
                valid_grades = range(6, 10)
                grades = [g for g in valid_grades]
        
            else:
                grades = [grade]

            # Add the grade to the first context
            context['grades'] = grades

            # Define the second context
            second_context = {
                'grade': grade
            }

            # Combine the two contexts
            context.update(second_context)

        except user_profile_student.DoesNotExist:
            # Return an HttpResponse if the user profile does not exist
            context['error_message'] = "User profile does not exist."

        return context

# @method_decorator(cache_page(60 * 60*24), name='dispatch')
class SubjectListView(DetailView):
    context_object_name = 'standards'
    model = Standard
    template_name = 'curriculum/subject_list_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            # Retrieve the user's profile
            user_profile = user_profile_student.objects.get(user=self.request.user)
            school = School.objects.get(name=user_profile.school)
            grade = user_profile.grade
            
            # Ensure you're filtering using the school object
            filtered_subjects = Subject.objects.filter(schools=school,standard=grade)

            # Add the filtered subjects to the context
            context['filtered_subjects'] = filtered_subjects

        except user_profile_student.DoesNotExist:
            # Handle case where the user profile does not exist
            context['error_message'] = "User profile does not exist."

        except School.DoesNotExist:
            # Handle case where the school does not exist
            context['error_message'] = "School does not exist."

        return context
    

# @method_decorator(cache_page(60 * 60*24), name='dispatch')
class LessonListView(DetailView):
    context_object_name = 'subjects'
    model = Subject
    template_name = 'curriculum/lesson_list_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            # Retrieve the user's profile
            user_profile = user_profile_student.objects.get(user=self.request.user)
            
            # Retrieve the actual School object, not just the name (ensure the school field is a foreign key to School)
            school = School.objects.get(name=user_profile.school)
            subject = self.get_object()
            grade = user_profile.grade
            
            # Ensure you're filtering using the school object
            filtered_lessons = Lesson.objects.filter(schools=school,subject=subject)

            # Add the filtered subjects to the context
            context['filtered_lessons'] = filtered_lessons

        except user_profile_student.DoesNotExist:
            # Handle case where the user profile does not exist
            context['error_message'] = "User profile does not exist."

        except School.DoesNotExist:
            # Handle case where the school does not exist
            context['error_message'] = "School does not exist."

        return context

# @method_decorator(cache_page(60 * 60*24), name='dispatch')
class LessonDetailView(DetailView,FormView):
    context_object_name = 'lessons'
    model = Lesson
    template_name = 'curriculum/lesson_detail_view.html'
    form_class = CommentForm
    second_form_class = ReplyForm

    def get_context_data(self, **kwargs):
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(request=self.request)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(request=self.request)
        # context['comments'] = Comment.objects.filter(id=self.object.id)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'form' in request.POST:
            form_class = self.get_form_class()
            form_name = 'form'
        else:
            form_class = self.second_form_class
            form_name = 'form2'

        form = self.get_form(form_class)

        if form_name=='form' and form.is_valid():
            print("comment form is returned")
            return self.form_valid(form)
        elif form_name=='form2' and form.is_valid():
            print("reply form is returned")
            return self.form2_valid(form)


    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.Standard
        subject = self.object.subject
        return reverse_lazy('curriculum:lesson_detail',kwargs={'standard':standard.slug,
                                                             'subject':subject.slug,
                                                             'slug':self.object.slug})
    def form_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.lesson_name = self.object.comments.name
        fm.lesson_name_id = self.object.id
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

    def form2_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.comment_name_id = self.request.POST.get('comment.id')
        fm.save()
        return HttpResponseRedirect(self.get_success_url())


class LessonCreateView(CreateView):
    # fields = ('lesson_id','name','position','image','video','ppt','Notes')
    form_class = LessonForm
    context_object_name = 'subject'
    model= Subject
    template_name = 'curriculum/lesson_create.html'

    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.standard
        return reverse_lazy('curriculum:lesson_list',kwargs={'standard':standard.slug,
                                                             'slug':self.object.slug})


    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.created_by = self.request.user
        fm.Standard = self.object.standard
        fm.subject = self.object
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

class LessonUpdateView(UpdateView):
    fields = ('name','position','video','ppt','Notes')
    model= Lesson
    template_name = 'curriculum/lesson_update.html'
    context_object_name = 'lessons'

class LessonDeleteView(DeleteView):
    model= Lesson
    context_object_name = 'lessons'
    template_name = 'curriculum/lesson_delete.html'

    def get_success_url(self):
        print(self.object)
        standard = self.object.Standard
        subject = self.object.subject
        return reverse_lazy('curriculum:lesson_list',kwargs={'standard':standard.slug,'slug':subject.slug})

def ai(request):
    subjects=AISubject.objects.all()
    return render(request, "ai/ai.html",{"subjects":subjects})

@login_required  
def lessons(request,slug):
    subjects=AISubject.objects.get(slug=slug)
    lessons=AILesson.objects.filter(subject=subjects)
    return render(request, "ai/lessons.html", {"subjects":subjects, "lessons":lessons})

def lesson_detail(request,slug):
    subjects=AISubject.objects.all()
    lessons=AILesson.objects.get(slug=slug)
    return render(request, "ai/lesson_detail.html", {"subjects":subjects, "lessons":lessons})
    
def coding(request):
    subjects=CodingSubject.objects.all()
    return render(request, "coding/coding.html", {"subjects":subjects})

@login_required
def codinglessons(request,slug):
    subjects=CodingSubject.objects.get(slug=slug)
    lessons=CodingLesson.objects.filter(subject=subjects)
    return render(request, "coding/codinglessons.html", {"subjects":subjects, "lessons":lessons})

def codinglesson_detail(request,slug):
    subjects=CodingSubject.objects.all()
    lessons=CodingLesson.objects.get(slug=slug)
    return render(request, "coding/codinglesson_detail.html", {"subjects":subjects, "lessons":lessons})
    
def training_level(request):
    return render(request, "trainer/training_level.html")

def trainer_subject_1(request):
    subjects=Subject.objects.filter(Q(subject_id='arduino_uno') | Q(subject_id='designing') | Q(subject_id='robotics') | Q(subject_id='python') | Q(subject_id='scratch') | Q(subject_id='electronics_4'))
    return render(request, "trainer/subject.html",{"subjects":subjects})

def trainer_subject_2(request):
    subjects=Subject.objects.filter(Q(subject_id='arduino_uno_8') | Q(subject_id='python_8') | Q(subject_id="arduino") | Q(subject_id="IoT"))
    return render(request, "trainer/subject.html",{"subjects":subjects})

def trainer_subject_3(request):
    subjects=Subject.objects.filter(Q(subject_id='python_10') | Q(subject_id='arduino_10') | Q(subject_id='ai_11'))
    return render(request, "trainer/subject.html",{"subjects":subjects})

def trainer_lesson(request,slug):
    subjects=Subject.objects.get(slug=slug)
    lessons=Lesson.objects.filter(subject=subjects)
    if subjects.slug=="python":
        lessons=lessons.all()
        # lessons=lessons.filter(Q(lesson_id="python_7_1") | Q(lesson_id="python_7_2") | Q(lesson_id="python_7_1") | Q(lesson_id="python_7_1")| Q(lesson_id="python_7_1"))

    elif subjects.slug=="arduino_uno_8":
        lessons=lessons.filter(Q(lesson_id="arduino_7_1"))
    return render(request, "trainer/trainer_lesson.html", {"subjects":subjects, "lessons":lessons})
    
def trainer_lesson_detail(request,slug):
    subjects=Subject.objects.all()
    lessons=Lesson.objects.get(slug=slug)
    return render(request,"trainer/trainer_lesson_detail.html",{"subject":subjects,"lessons":lessons})
    
def display_kits(request):
    kits=Mechanzo_kit_name.objects.all()
    return render (request,'curriculum/kits_display.html',{"kits":kits})

def display_models(request,slug):
    kit_name=Mechanzo_kit_name.objects.get(slug=slug)
    models_name=Mechanzo_model_name.objects.filter(kit=kit_name)
    return render (request,'curriculum/models_display.html',{'models':models_name, 'kits':kit_name})
    
from rest_framework import generics
from rest_framework import permissions
from .models import LectureRating
from .serializers import LectureRatingSerializer

class LectureRatingCreateView(generics.CreateAPIView):
    queryset = LectureRating.objects.all()
    serializer_class = LectureRatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        lecture_id = self.request.data.get('lecture')
        user = self.request.user
        # Check if the user has already rated the lecture
        existing_rating = LectureRating.objects.filter(lecture=lecture_id, user=user).first()
        if existing_rating:
            # Update the existing rating
            existing_rating.rating = self.request.data.get('rating')
            existing_rating.save()
        else:
            # Create a new rating
            serializer.save(user=user)
            
def mentor_training_level(request):
    # Check if the user has completed all lessons in level 1
    level_1_lessons = TeacherLesson.objects.filter(subject__level='Phase-I')
    completed_lessons_level_1 = UserLessonProgress.objects.filter(user=request.user, lesson__in=level_1_lessons, completed=True).count()
    
    if completed_lessons_level_1 == level_1_lessons.count():
        unlock_level_2 = True  # Unlock level 2
    else:
        unlock_level_2 = False

    # Check if the user has completed all lessons in level 2
    level_2_lessons = TeacherLesson.objects.filter(subject__level='Phase-II')
    completed_lessons_level_2 = UserLessonProgress.objects.filter(user=request.user, lesson__in=level_2_lessons, completed=True).count()

    if completed_lessons_level_2 == level_2_lessons.count():
        unlock_level_3 = True  # Unlock level 3
    else:
        unlock_level_3 = False

    return render(request, "trainer/mentor_training_level.html", {
        'unlock_level_2': unlock_level_2,
        'unlock_level_3': unlock_level_3,
    })


def mentor_subjects_by_level(request, level):
    subjects = TeacherSubject.objects.filter(level=level)
    
    lessons_by_subject_and_module = {}

    for subject in subjects:
        lessons = TeacherLesson.objects.filter(subject=subject).order_by('module', 'position')
        lessons_by_modules = {}
        for module_key, module_name in TeacherLesson.MODULE_CHOICES:
            module_lessons = lessons.filter(module=module_key)
            if module_lessons.exists():
                lessons_by_modules[module_key] = {
                    'name': module_name,
                    'lessons': module_lessons
                }
        lessons_by_subject_and_module[subject] = lessons_by_modules

    return render(request, "trainer/mentor_subject.html", {
        "lessons_by_subject_and_module": lessons_by_subject_and_module,
    })


def mentor_lesson_by_module(request, subject_slug, module):
    # Get lessons for the specified subject and module
    subject = TeacherSubject.objects.get(slug=subject_slug)
    lessons = TeacherLesson.objects.filter(subject=subject, module=module).order_by('position')

    return render(request, "trainer/mentor_lesson.html", {
        "lessons": lessons,
        "subject": subject,
        "module": module
    })


def mentor_lesson_detail(request, slug):
    # Get lesson by slug
    lesson = TeacherLesson.objects.get(slug=slug)
    
    if request.method == "POST":
        # Mark lesson as completed
        UserLessonProgress.objects.update_or_create(
            user=request.user,
            lesson=lesson,
            defaults={'completed': True}
        )
        return redirect('curriculum:mentor_training_level')

    return render(request, "trainer/mentor_lesson_detail.html", {"lesson": lesson})