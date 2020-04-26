# InferenceTechTest

a Django REST microservice for processing messages (each message is sent from one user to another).

## Use case scenarios
- creating messages
- receiving messages
- change messages
- delete messages


## API Endpoints
### Authentication
- /api/auth/login/
  - POST request - login via token, response: auth_token
- /api/auth/logout/
  - POST request - logout via token / destroy token
### Messaging
- /api/create/
  - POST request - create message
    - data={'body': "message text", 'recipient': recipient_id} 
- /api/all/
  - GET request - get all messages that user allowed to see (sent + recieved messages)
    - response: Queryset[Message]
- /api/all/<int:pk>/
  - GET request - get all the messages from the chat with a particular user with (from/to user with id=pk)
    - response: Queryset[Message]
- /api/detail/<int:pk>/
  - GET request - get particular message with id=pk
    - response: Message
  - PUT/PATCH request - edit message with id=pk
    - data={'body': "edited message text"}
  - DELETE request - delete message with id=pk
  
  
  
# Install
  `pip install -r requirements.txt`
  
# Run
  `python manage.py runserver`
