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

Workflow
---
The software architecture that is practiced is the MVC architecture. As a concept, the MVC design pattern is really simple to understand:

The model(M) is a model or representation of your data. It’s not the actual data, but an interface to the data. The model allows you to pull data from your database without knowing the intricacies of the underlying database. The model usually also provides an abstraction layer with your database, so that you can use the same model with multiple databases.

The view(V) is what you see. It’s the presentation layer for your model. On your computer,
the view is what you see in the browser for a Web app, or the UI for a desktop app. The view also provides an interface to collect user input.

The controller(C) controls the flow of information between the model and the view. It uses programmed logic to decide what information is pulled from the database via the model and what information is passed to the view. It also gets information from the user via the view and implements business logic: either by changing the view, or modifying data through the model, or both.



