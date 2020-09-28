# COVID-19-Self-Diagnosis-Web
This project is for diagnosing contagious disease from symptoms written in natural language. Symptoms will be compared with data, which is already classified by disease, and used to show the probability of infection to the user. The goal of this project is to reduce time to decide to visit the hospital when the user suspects oneself on a contagious infection and helps patients to describe their symptoms in a familiar way.   

# Components   
- /static : configuration, javascript(maps.js), css file(style.css)    
- /templates : html file
- app.py : flask server
- test.py : symptom word extraction tool (show RAD values of symptoms in CSV)
- testing.py : unit test
- word.py : generate symptom word model (words from related articles), executed in Jupytor notebook 


# Screenshots   
### Step 1: Get description of symptom   
When the user clicked the submit button, client sends GET request to web server and Step 2 appears. Responded data contains symptom words extracted from description in Step 1.   
![screenshot1](https://user-images.githubusercontent.com/35682236/90317645-e4b54f80-df65-11ea-9ed0-3498f6373263.png)
### Step 2: Get period of symptom   
User can set the range of periods that symptom appeared. Each date form is applied per symptom.      
![screenshot2](https://user-images.githubusercontent.com/35682236/90317648-e848d680-df65-11ea-89e0-9cf11f03fc4b.png)         
### Step 3: Questionnaire about exposure to the virus        
![screenshot3](https://user-images.githubusercontent.com/35682236/90317652-ec74f400-df65-11ea-9773-f44c2efa9bb4.png)            
### Step 4: Result        
![screenshot4](https://user-images.githubusercontent.com/35682236/90317653-ee3eb780-df65-11ea-9c66-e5f2e3804408.png)           
