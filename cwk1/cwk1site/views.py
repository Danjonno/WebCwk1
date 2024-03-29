from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, logout, login
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Stories, Authors
from datetime import datetime as dt
import datetime
from rest_framework.authtoken.models import Token

# Create your views here.

#LOGIN
@csrf_exempt
def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)
        if user is not None:
            #Authentication successful
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'message': 'Welcome, {}!'.format(username)})

        else:
            #Authentication failed
            return HttpResponse('Invalid username or password', status=401)
    else:
        #Wrong Method
        return HttpResponse('POST Method Required', status=405)


#LOGOUT
@csrf_exempt
def Logout(request):
    if request.method == 'POST':
        logout(request)
        request.session.flush()
        return HttpResponse('Succesfully logged out. Goodbye!', status=200)
    else:
        #Wrong Method
        return HttpResponse('POST Method Required', status=405)


#POST A STORY
@csrf_exempt
def Story(request):
    
    #POST METHOD
    if request.method == 'POST':
        #CHECK USER AUTHENTICATED
        if request.user.is_authenticated:
            #get JSON data
            try:
                payload = json.loads(request.body)
            except:
                return JsonResponse("Invalid JSON payload", status = 400)
            
            #extract json data
            headline = payload.get('headline')
            category = payload.get('category')
            region = payload.get('region')
            details = payload.get('details')

            #make sure all fields are filled in
            if all ([headline, category, region, details]):
                #get current user
                author, created = Authors.objects.get_or_create(user=request.user, defaults={'name': request.user.username})

                #create new story in DB
                try: 
                    newStory = Stories.objects.create(
                        headline = headline,
                        category = category,
                        region = region,
                        details = details,
                        date = datetime.date.today(),
                        author = author #use logged in user
                    )
                    return HttpResponse('Story Successfuly Added', status=200)
                except:
                    return HttpResponse('Could not add Story', status=503)
            else:
                return HttpResponse('Missing Data. Headline, Category, Region and Details Required', status=400)
            
        else:
            return HttpResponse('User Not Logged In', status=503)
    
    #GET METHOD
    elif request.method == 'GET':
        #get parameters
        try:
            story_cat = request.GET.get('story_cat', False)
            story_region = request.GET.get('story_region', False)
            story_date = request.GET.get('story_date', False)

            #query stories
            stories = Stories.objects.all()
            if story_cat != '*':
                stories = Stories.objects.filter(category=story_cat)
            if story_region != '*':
                stories = Stories.objects.filter(region=story_region)
            if story_date != '*':
                date_obj = dt.strptime(story_date, "%d/%m/%Y")
                formatted_date = date_obj.strftime("%Y-%m-%d")
                stories = Stories.objects.filter(date__gte=formatted_date)
                
        except:
            #if parameters are not given, send error
            return HttpResponse('Invalid Parameters', status=503)
        
        

         # Check if any stories are found
        if stories.exists():
            # Serialize the stories data
            serialized_stories = []
            for story in stories:
                serialized_story = {
                    'key': story.pk,
                    'headline': story.headline,
                    'story_cat': story.category,
                    'story_region': story.region,
                    'author': story.author.name,
                    'story_date': str(story.date),
                    'story_details': story.details
                }
                serialized_stories.append(serialized_story)

            # Return the serialized stories as JSON response
            return JsonResponse({'stories': serialized_stories}, status=200)
        else:
            # Return 404 status code with a message if no stories are found
            return HttpResponse("No stories found", status=404)
    
    #if neither POST nor GET
    else:
        #Wrong Method
        return HttpResponse('POST Method Required', status=405)
    


#GET A STORY
@csrf_exempt
def DeleteStory(request, key):
    if request.method == 'DELETE':
        if request.user.is_authenticated:
            try:
                story = Stories.objects.get(id = key)
                story.delete()
                return HttpResponse('Story Deleted', status=200)
            except:
                return HttpResponse('Could Not Find Story With key '+ key , status=503)
        else:
            return HttpResponse('User Not Logged In', status=503)
    else:
        #Wrong Method
        return HttpResponse('DELETE Method Required', status=405)