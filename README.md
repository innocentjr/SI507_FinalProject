### Non-profit Finance Fund Pay for Success Database Scrubbing

The goal of this project is to scrub the website of the Non-profut Finance Fund to grab every possible bit of information on the various Pay for Success projects in the United States. This requires visiting 185 projects pages, classifying them by type (project, funding opportunity, or legislation), grabbing all unique classifiers for them (scope, issue area, location, etc) and then save the data into a set of database tables. The end result is a database of all these projects and a really great visualization of the issue area's of projects by state and government level(state, county, and city). 

I will be caching and parsing the list of 'Pay for Success' projects from the Nonprofit Finance Hub website. After doing so, I will used the cached information to create a database of Pay for Success Projects in the United States. I will create a couple of table, at least three: the first being a masterlist of all projects, second of general, non-financial characteristics of the projects, and third of financial characteristics of the projects.

See Link here: http://www.payforsuccess.org/projects

### Milestones for Final Project

- Part 0: `Create Git Repository`
    - Create GIT repository for Nonprofit Finance Fund 'Pay for Success Projects Database Project'

- Part 1: `Cache Data`
    - Get from cache with BeautifulSoup:
        - The first task to is grab an intial cache of the first page of the activity map. Since the page only load 99 project, it is necessary to cache pages by their types (Project, Legislation, and Opportunity)
        - In order to grab this page, you must install Selenium web driver and especially the Chrome driver. If you do not want to download the chrome driver, please edit the code in the set_up file. 
        - With the driver install, the three initial pages will be cache and fromt eh cache Beautiful Soup objects will be created to gather the list of projects from each cache. These list will be save to threes JSON files and merged into a Master JSPN file.
        - With this MASTER.json file (which has all the projects and their links), the web driver will open each and cache them individually. This will take some time, so make sure you free up space on your computer memory. A total fo 185 pages will be cached and saved to your folder. 
        - We then create Beautiful instances of each of the html files and parse them for the revelant information 
          - Much of this parsing occurs in the classes

- Part 2: `Class definition to store parsed objects`
    - class `PayfSuccess_Project`
        - This class initializes each of the variables with a default value of 'None'. It also constains a __contain__ function that each other class will have access to as they will inherit this class. 
        - What does it represent? This class represents the information generation from the cache that defines a PFS project
        - Constructor
            - the construct should instantiate and define these variables:
              - self.name ( Project Name)
              - self.location (city, country)
              - self.level (the level of government - i.e state, county, federal)
              - self.targetPop (the target population)
              - self.dealSize (the deal size)
              - self.issueareas (the area, i.e Health, Juvenile Justice, Recidivism)
              - self.description (a description of the project)
              - self.serviceProvider (the service provider)
              - self.funders (non-grant layers of the capital stack - senior and junior debt)
              - self.intermediary (the deal structurer)
              - self.currentphase
              - self.
            - Each of these variables should have a default value of 'None'
            - From the JSON file of the cache, parse for the variables listed above, (with Soup instances) and save into the class variables
    - Method: ` __repr__`
        - This should print out all the relevant variables from above to allow the for check that variable properly defined.
    - Method: `__contains__`
        - Checks to see it a given is an Project/Legislation/Opportunity instance.
Other classes: There are three other classes (class Project, class, Legislation, class Opportunity)
    - Each of process their respective variables.  

- Part 3: `Create Database tables`
    - Create Tables:
        - After processes, the data is read from the classes and store in a database named "payforsuccessprojects". This database has 6 table:
           - Master, Projects, Legislation, Opportunity, Project_Financing, Project_Partners
        - Master: has general characteristics on all the pfs material rojects, it has a uniquie serial id that Projects, Legislation and Oppotunity reference.
        - Project, Legislation, Opportunity contain the information store in the class variables respectively. 
        - Project_Partners and Project_Financing have foreign keys that point to Project, rather than Master. 
            - Financing Characteristics of Project (populated with variable related to financing)
            - Project Partners has a table of all the projects partners and stakeholders

- Part 4: `Create Test Suite` =
    -  Test caching
    -  Test class Definitions
    -  Test Database setups and and Flask application
    - Test, since they require calling the driver are a bit tedious, so again, approach with care.
    
- Part 5: Visualization
    - A dyanmic HTML is rendered that queries the database for the number of different issue areas a city, country, and state has. The data is processed and saved to a file. A Flask application is used to read the data into the template HTML file. This will all automatically be processed when you run teh final project file: All you need to know is that the host is set to '127.0.0.1' and the port to 5000. To see the visualization, visit http://localhost:5000/.

- Submission
    - Files to be included
        - [ ] All `.html` files used for caching
        - [ ] Include `README.md` and `requirements.txt` files
        - [ ] Include some visual representation of Data. (Project by states, projects by issue area, projects completed)
