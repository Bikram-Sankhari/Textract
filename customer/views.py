from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import DocumentSet
from django.contrib import messages
from .models import Customer, CustomerDocument
import boto3
import os
import json

# Create your views here.

def analyze_id(file_name):
    session = boto3.Session(profile_name='profile-name')
    client = session.client('textract', region_name='ap-south-1')
    file_path = os.getcwd()+ file_name

    with open(file_path, 'rb') as img_file:
       img_bytes = img_file.read()
       response = client.analyze_id(DocumentPages=[{'Bytes': img_bytes}])

    response_data = {}
    for doc_fields in response['IdentityDocuments']:
        for id_field in doc_fields['IdentityDocumentFields']:
            for key, val in id_field.items():
                if "Type" in str(key):
                    component = str(val['Text'])
            for key, val in id_field.items():
                if "ValueDetection" in str(key):
                    if str(val['Text']):
                        response_data[component] = str(val['Text'])
        
    return response_data

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required(login_url='login')
def upload(request):
    if request.method == 'POST':
        document = DocumentSet.objects.get(name=request.POST['doc_name'])
        if document.has_backside and len(request.FILES.getlist('file')) != 2:
            messages.error(
                request, f"Please upload two files for front and backside of your {document}")
            return redirect('upload')

        if not document.has_backside and len(request.FILES.getlist('file')) != 1:
            messages.error(
                request, f"Please upload only front side of your {document}")
            return redirect('upload')

        for file in request.FILES.getlist('file'):
            if str(file).split('.')[-1] not in ['png', 'jpg', 'jpeg', 'tiff', 'pdf']:
                messages.error(
                    request, f"Please upload only pdf, png, jpg, jpeg or tiff files")
                return redirect('upload')
        
        customer = Customer(createdBy=request.user)
        customer.save()

        customer_doc = CustomerDocument(customer=customer, attached_file1=request.FILES.getlist('file')[0])

        if document.has_backside:
            customer_doc.attached_file2 = request.FILES.getlist('file')[1]
        
        customer_doc.save()

        response = analyze_id(customer_doc.attached_file1.url)
        if document.has_backside:
            response.update(analyze_id(customer_doc.attached_file2.url))

        customer_doc.extracted_json = json.dumps(response)
        customer_doc.save()

        last_name_synonyms = ['LAST_NAME', 'last name', 'surname', 'SURNAME', 'LAST NAME', 'last_name']
        first_name_synonyms = ['FIRST_NAME', 'first name', 'FIRST NAME', 'first_name', 'name', 'NAME']
        nationality_synonyms = ['NATIONALITY', 'nationality']
        sex_synonyms = ['SEX', 'sex', 'gender', 'GENDER']

        for name in last_name_synonyms:
            if name in response:
                customer.surname = response[name]
        
        for name in first_name_synonyms:
            if name in response:
                customer.name = response[name]
            
        for nationality in nationality_synonyms:
            if nationality in response:
                customer.nationality = response[nationality]

        for sex in sex_synonyms:
            if sex in response:
                customer.sex = response[sex]

        customer.save()

        return redirect('upload')

    else:
        docs = request.user.country.documentset_set.all()
        context = {'docs': docs}
        return render(request, 'upload.html', context)
