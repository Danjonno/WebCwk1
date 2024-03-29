import requests
session = requests.Session()
globalUrl = ''
token = ''

#login command
def login(url):
    global session, token
    #prompt user for username and password
    username = input("\nEnter your Username: ")
    password = input("Enter your password: ")

    #make payload
    payload = {'username' :username, 'password': password}

    #send the POST request
    response = session.post(url + '/api/login', data = payload)
    token = response.json().get('token')

    #print response
    print(response.text)

#logout command
def logout():
    global session, token
     #POST request to logout
    response = session.post(globalUrl + '/api/logout', headers={'Authorization': f'Token {token}'})
    #print response
    print(response.text)

#post story command
def post():
    global session, token
    #prompt the user for story headline, category, region and details
    headline = input("\nEnter the headline of the story: ")
    category = input("Enter the category of the story: ")
    region = input("Enter the region of the story: ")
    details = input("Enter the details of the story: ")


    # Construct the payload
    payload = {
        'headline': headline,
        'category': category,
        'region': region,
        'details': details
    }

    #send POST request
    headers = {'Authorization': token}
    response = session.post(globalUrl + '/api/stories', json=payload, headers=headers)

    #print response
    print(response.text)

#news command
def news(userInput):
    splitCommand = userInput.split(' ')
    id = ''
    cat = '*'
    reg = '*'
    date = '*'
    for type in splitCommand:
        if "-id" in type:
            id = type.split("=")[1]
            id = id[1:-1]
        elif "-cat" in type:
            cat = type.split("=")[1]
            cat = cat[1:-1]
        elif "-reg" in type:
            reg = type.split("=")[1]
            reg = reg[1:-1]
        elif "-date" in type:
            date = type.split("=")[1]
            date = date[1:-1]
    urls = []
    response = requests.get("https://newssites.pythonanywhere.com/api/directory")
    responseData = response.json()

    if id:
        for agency in responseData:
            if agency["agency_code"] == id:
                urls.append(agency["url"])
    else:
        for agency in responseData:
            urls.append(agency["url"])
    
    for url in urls:
        response = session.get(url+"/api/stories?story_cat=" + cat + "&story_region=" + reg + "&story_date=" + date)
        if response.status_code == 200:
            stories = response.json()
            for story in stories["stories"]:
                print("Headline:" + story['headline'])
                print("Category:" + story['story_cat'])
                print("Region:" + story['story_region'])
                print("Author:" + story['author'])
                print("Date:" + story['story_date'])
                print("Details:" + story['story_details'] + "\n")
        else:
            print("Failed to retrive stories")

def list():
    response = requests.get("http://newssites.pythonanywhere.com/api/directory")
    agencies = response.json()
    for agency in agencies:
        print("Name: ", agency['agency_name'])

def delete(key):
    global session
    response = session.delete(globalUrl+"/api/stories/"+key)
    print(response.text)

#while loop with functions to handle requests
while(True):
    userInput = input("\nServices offered:\n login <your URL> \n logout \n post \n news \n list \n delete \n Please Enter a Service: ")
    command = userInput.split(' ')[0]

    if  command == 'login':
        globalUrl = userInput.split(' ')[1]
        login(userInput.split(' ')[1])
    elif command == 'logout':
        logout()
    elif command == 'post':
        post()
    elif command == 'news':
        news(userInput)
    elif command == 'list':
        list()
    elif command == 'delete':
        delete(userInput.split(' ')[1])
