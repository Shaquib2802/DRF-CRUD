from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['POST','GET','PATCH','DELETE'])
def addStudent(request):
    if request.method=='POST':
        x=StudentSerializer(data=request.POST)
        if x.is_valid():
            x.save()
            return Response({'message':"data add successfully",'response_code':200,'data':x.data})
        return Response({'message':x.errors, 'response_code':400})
    
    """ if request.method=="GET":   #This is simple get without Pagination
        student=Student.objects.all()
        x=StudentSerializer(student,many=True)
        return Response({'message':"Data get successfully", 'response_code':200, "data":x.data}) """
        
        
    if request.method == 'GET':
        search = request.query_params.get('search')
        limit = request.query_params.get('limit',1)
        page = request.query_params.get('page',1)   
        student_id = request.query_params.get('student_id')
        student_name = request.query_params.get('student_name')
        #Search Code Begin
        if search:
            # student = Student.objects.filter(name__icontains = search)  #Search on the basis on name only
            student = Student.objects.filter(Q(name__icontains = search) | Q(mobile_number__contains = search)|Q(address__contains = search)) #Search on the basis of mobile_number,address and name 
            x = StudentSerializer(student,many=True)
            return Response({'message':'data get successfully','response_code':200,'data':x.data})
        if student_id:
            if not Student.objects.filter(id=student_id).exists():
                return Response({'message':'this id does not exist in Database', 'response_code':400})
            student=Student.objects.get(id=student_id)
            x=StudentSerializer(student, many=False)
            return Response({'message':'Data get successfully', 'response_code':200,'data':x.data})
        if student_name:
            if not Student.objects.filter(name = student_name).exists():
                return Response({'message':'This student for this student does not exist','response_code':400})
            student=Student.objects.filter(name = student_name)
            x=StudentSerializer(student,many=True)
            return Response({'message':'Data get successfully','response_code':200, 'data':x.data})
        student = Student.objects.all()
        paginator = Paginator(student,limit)
        x = paginator.get_page(page)
        y= StudentSerializer(x,many = True)
        return Response({'message':'Data get successfully','response_code':200, 'data':y.data,'page':page})
            
    
    if request.method=="PATCH":
        student_id = request.data.get('student_id')
        if student_id:
            if not Student.objects.filter(id=student_id).exists():
               return Response({'message':'ID does not exist in DB' , 'response_code':400})
            student=Student.objects.get(id=student_id)
            x=StudentSerializer(student,data=request.POST,partial=True)
            if x.is_valid():
                x.save()
                return Response({"message":"Data Update Successfully","response_code":200,"data":x.data})
            return Response({"message": x.errors})
        return Response({'message':'ID not found' ,'response_code':400})
    
    if request.method=='DELETE':
        student_id=request.data.get('student_id') 
        if student_id: 
            if not Student.objects.filter(id=student_id).exists():
                return Response({'message':'this id does not exists in database','response_code':400}) 
            student=Student.objects.get(id=student_id).delete()
           
            return Response({'message':'student id deleted successfully','response_code':200})
        return Response({'message':'student id not found','response_code':400})
    
@api_view(['GET','POST','PATCH','DELETE'])
def addSubject(request):   
    if request.method == 'GET':   
        student_id = request.query_params.get('student_id')
        if student_id:
            if not Student.objects.filter(id=student_id).exists():
                return Response({'message':'this id does not exist in Database', 'response_code':400})
            y=Student.objects.get(id=student_id)
            if y:
                if not Subject.objects.filter(student=y).exists():
                    return Response({'message':'This subject for this student does not exist','response_code':400})
                subject=Subject.objects.filter(student=y)
                x=SubjectSerializer(subject,many=True)
                return Response({'message':'Data get successfully','response_code':200, 'data':x.data})
            return Response({'message':'Student not found','response_code': 400})
        return Response({'message':'Student id not found','response_code': 400})
        

    if request.method == 'POST':
        x=SubjectSerializer(data=request.data)
        if x.is_valid():
            x.save()
            return Response({'message':'Data save succesfully','response_code':200,'data':x.data})
        return Response({'message':x.errors})
    if request.method == 'PATCH':
        subject_id = request.data.get('subject_id')
        if subject_id:
            if not Subject.objects.filter(id=subject_id).exists():
                return Response({'message':'Invalid subject ID', 'response_code':400})
            subject = Subject.objects.get(id=subject_id)
            x=SubjectSerializer(subject, data=request.data, partial=True)
            if x.is_valid():
                x.save()
                return Response({'message':'Data Update Successfully','response_code':200, 'data':x.data})
            return Response({'message': x.errors})
        return Response({'message':' subject ID not found' ,'response_code':400})
    if request.method == "DELETE":
        subject_id = request.data.get('subject_id')
        if subject_id:
            if not Subject.objects.filter(id=subject_id).exists():
                return Response({'message':'Invalid subject ID', 'response_code':400})
            subject = Subject.objects.get(id=subject_id).delete()
            return Response({'message':'Data Deleted Successfully', 'response_code':200})
        return Response({'message':"Student ID not found", 'response_code':400})
    
from django.core.paginator import Paginator
@api_view(['GET'])     #Pagination Individual Code
def getstudent(request):
    limit = request.query_params.get('limit',1)
    page = request.query_params.get('page',1)
    student = Student.objects.all()
    paginator = Paginator(student,limit)
    x=paginator.get_page(page)
    y=StudentSerializer(x,many=True)
    return Response({'message':'data get successfully','response_code':200,'data':y.data})
                
            
            
      
            