**Report file for Entity Model**

Entities
---
Each entity has its separate application found in the directory ./backend/src/

Each application has the following file structure:
1. ```models.py```: all the object models of the entities is declared in this file
2. ```admin.py```: settings for the admin panel is set in this file
3. ```forms.py```: form used to create/update the entity, as well as validations are written in this file
4. ```views.py```: all the views and the controlling part of the application is coded here
5. ```urls.py```: routing and url patterns for the views are set here
6. ```api.py```: API views for the entity is written here
7. ```serializers.py```: The entity model is serialized here for the API

### Accounts
This application takes care of the User Profile. The main model of this entity is the Profile model, which has a one-to-one relationship with the User model inbuilt in Django.

### Contests
This application takes care of the Contest Entity. The models that make up the entity are:
1. Contest: The main model for the application
2. ContestsHaveProblems: A many-to-many relationship with Problems
3. Participants: A many-to-many relationship with Profile.

### Problems
This application takes care of the Problem Entity. The main models are:
1. Problem: The main model enitity
2. TestCase: A many-to-one relationship with Problem

### Posts
This application takes care of the Post Entity. The main model for this entity is Post

### Submissions
This application takes care of the Submissions Enitity. The main models are:
1. Submissions: This takes care of Problem Submissions
2. ContestSubmissions: This takes care of Contest Problem Submissions
3. Languages: The various languages compatible with the application

### Tags
This application takes care of the Tag Enitity. The main model is Tag.


