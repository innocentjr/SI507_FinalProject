### 507 F17 Final Project

I will be caching and parsing the list of 'Pay for Success' projects from the Nonprofit Finance Hub website. After doing so, I will used the cached information to create a database of Pay for Success Projects in the United States. I will create a couple of table, at least three: the first being a masterlist of all projects, second of general, non-financial characteristics of the projects, and third of financial characteristics of the projects.

See Link here: http://www.payforsuccess.org/projects

### Milestones for Final Project

- Part 0: `Create Git Repository`
    - Create GIT repository for Nonprofit Finance Fund 'Pay for Success Projects Database Project'

- Part 1: `Cache Data`
    - Get from cache with BeautifulSoup:
        - From the site cache the full list of projects (the href links to their project pages) from the homepage.
        - For each project:
          - Create ` Beautiful Soup` instance from the html
          - Extract links to project pages for all 99 projects

- Part 2: `Class definition to store parsed objects`
    - class `PayfSuccess_Project`
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
        - Written to ensure that there are instances of the variable listed above.

- Part 3: `Create Database tables`
    - Create Tables:
        - All Projects (project name, serial id)
        - Financing Characteristics of Project (populated with variable related to financing)
        - General characteristics of Projects (all non-financing related variables)

- Part 4: `Create Test Suit` =
    -  Test caching
    -  Test class Definition
    -  Test Database setup and insert statements

- Submission
    - Files to be included
        - [ ] All `.html` files used for caching
        - [ ] Include `README.md` and `requirements.txt` files
        - [ ] Include some visual representation of Data. (Project by states, projects by issue area, projects completed)
