from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import test, apiCall
from django.urls import reverse
import requests
from .forms import ApiForm

# Create your views here.
def index(request):
    #form = ApiForm()
    saved_calls = [i for i in apiCall.objects.all()]
    context = {'testStuff': 'hey WORLD','saved_calls': saved_calls,}# 'form': form}
    return render(request, 'PostmanClone/index.html', context)

def submit(request):
    if 'submitButton' in request.POST:
        myTest = get_object_or_404(test, pk=1)
        baseURL = request.POST['baseURL']
        httpMethod = request.POST['httpMethod']
        headers = {}
        #make this thing its own method since you'll be doing shit with the headers all over the place!!!
        for i in range(3):
            index = i+1
            if (request.POST['headersa' + str(index)] != ""):
                headers[request.POST['headersa' + str(index)]] = request.POST['headersb' + str(index)]


        pythonCode = generatePythonCode(baseURL, httpMethod, headers)

        api_response = requests.request(httpMethod, baseURL, headers = headers).json()
        context = {'headers': headers, 'testObject': myTest, 'baseURL': baseURL, 'api_response': api_response, 'httpMethod': httpMethod, 'pythonCode': pythonCode}
        ##TODO: THIS NEEDS TO BE A REDIRECT!!!! if hettpmethod is post this needs to be a redirect.
        return render(request, 'PostmanClone/results.html', context)
    elif 'saveButton' in request.POST:
        #make a separate method that you pass POST into sometime to clean up this code!!  it can return your entire context
        baseURL = request.POST['baseURL']

        new_api_call = apiCall()
        new_api_call.base_url, new_api_call.headersa1, new_api_call.headersb1, new_api_call.headersa2, new_api_call.headersb2, new_api_call.headersa3, new_api_call.headersb3, new_api_call.httpMethod = request.POST['baseURL'], request.POST['headersa1'],request.POST['headersb1'], request.POST['headersa2'],request.POST['headersb2'], request.POST['headersa3'], request.POST['headersb3'], request.POST['httpMethod']
        new_api_call.save()
        return render(request, 'PostmanClone/index.html')

#method to be used in the submit view.  does this belong in another file by convention?
def generatePythonCode(baseURL, httpMethod, headers):
    pythonCode = "import requests\n\nbaseURL = \"" + baseURL + "\"\nhttpMethod = \"" + httpMethod + "\"\nheaders = " + str(headers) + "\n api_response = requests.request(httpMethod, baseURL, headers = headers).json()"


    #replace my newlines with actual newlines?
    pythonCode = pythonCode.replace(r'\n', '\n')
    return pythonCode