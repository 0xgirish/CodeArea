**Report file for Templates and the Static features**

Templates
--- 
Templates are strings of text (mainly written in html) that is intended to separate the presentation of a document from its data. A template defines placeholders and various bits of basic logic (template tags) that regulate how the document should be displayed. 

Templates for each entity can be found in ```./backend/src/templates/```

The templates provide the "view" for the following:
1. Feed 
2. Create Page
3. Update Manage
4. Manage Page
5. Leaderboard
6. Problem Page
7. IDE
8. Contest Page
9. Login/Sign up Page

Static features
---
This includes the various CSS and JS libraries used to make the application more user friendly, the files are found in the static folder ```./backend/src/static/```. The technologies used are:
1. [Bootstrap](https://getbootstrap.com/): An open source toolkit for developing with HTML, CSS, and JS. 
2. [Material Kit](http://demos.creative-tim.com/material-kit/index.html): A UI kit that works on top of Bootstraps
3. Ajax(jQuery): for communicating with the judge and backend API to do CRUD operations on the database without reloading the page
4. [Select2](https://select2.org/): Integerated with our self-created backend API to provide autocomplete search
5. Markdownjs: Converts markdown into renderable HTML
