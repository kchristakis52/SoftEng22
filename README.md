# Software Engineering Project 2022-2023

## Group: softeng2022-21

## Members: 
+Ιωάννης Μπέλλος el19067
+Κωνσταντίνος Χριστάκης el19646
+Βασίλειος Αλιφραγκής el19952
+Στέφανος Αβράμης el21724
+Γεώργιος Αναστασίου el19112
+Σπύρος Παπαδόπουλος el19058

## Stack:

+Database: MongoDB
+Backend: Flask Python
+CLI: Click Python
+Frontend: HTML/CSS/JS
+Postman (for testing the endpoints)

## Instructions

1. Clone the repository
2. Open the folder
3. Make sure that MongoDB Server Service is running and that you have installed MongoDB Command Line Database Tools
4. Open a terminal and execute: 
```
mongorestore -d queDB ./data
```
5. Create and activate a virtual environment
6. Execute: 
```
pip install -r requirements.txt
```
7. Execute
```
flask --app api-backend/QuestionnaireApp.py run -h 127.0.0.1 -p 9103
```
8. Navigate to http://127.0.0.1:9103 to use the frontend

