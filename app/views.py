from django.shortcuts import render,redirect,get_object_or_404
from .models import Student
from .forms import StudentForm
from django.contrib import messages
# Create your views here.

def show(request):
    data=Student.objects.filter(isdelete=False)
    return render(request,'index.html',{'a':data})

def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.warning(request, "Successfully data added")
            return redirect('index')   # go back to student list
        else:
            print(form.errors)
    else:
        form = StudentForm()


    return render(request, 'add_student.html', {'form': form})

def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":  # <--- Added colon here
        form = StudentForm(request.POST, instance=student) # <--- Moved to new line + Indented
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'add_student.html', {'form': form, 'edit_mode': True})

def delete_data(request,id):
     data=Student.objects.get(id=id)
     data.isdelete=True
     data.save()
     messages.warning(request, f"Student {data.name} moved to Recycle Bin.")
     #data.delete()
     return redirect('index')


def recycle_bin(request):
    data = Student.objects.filter(isdelete=True)
    return render(request, 'recycle_bin.html', {'data': data})

def restore_data(request,id):
     data=Student.objects.get(id=id)
     data.isdelete=False
     data.save()
     #data.delete()
     return redirect('index')
def permanent_delete(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete() # This actually removes it from the DB
    return redirect('recycle_bin')
