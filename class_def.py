from time import sleep # this should go at the top of the file
from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import re

#with open('Master.json', 'r') as f:
    #mast = json.loads(f.read())
    #f.close()

#test = mast[list(mast.keys())[1]]
#test_link = test["Link"]

#base_url = 'http://www.payforsuccess.org'
#with open('test.html', 'r', encoding='utf-8') as f:
    #html = f.read()
    #f.close()

#driver = webdriver.Chrome()
#driver.get(base_url+test_link);

#page_source is a variable created by Selenium - it holds all the HTML
#html = driver.page_source
#with open('project86.html', 'r', encoding='utf-8') as f:
    #html = f.read()
    #f.close()

#bsObj = BeautifulSoup(html, "html.parser")
#bsObj2 = bsObj.prettify()

#with open('test.html', 'w', encoding='utf-8') as f:
    #f.write(bsObj2)
    #f.close()
#driver.quit()
#main = bsObj.find('div', {'class':"main"})
#status = main.find('a').get_text().strip()
#content = bsObj.find('div', {'class':"content"})
#content_sec = main.find('div', {'class':"content__section"})
#description = re.sub(' +',' ', content_sec.get_text().strip())
#aside = bsObj.find('aside', {'class':"sidebar"})
#teaser = main.find('div', {"class":"teasers"})
#interventions = aside.find('div', {'class':"facts__row"})
    ##print(aside)
#content_sec = main.find('div', {'class':"facts__content"})
    #second = content_sec.find_all('div', {'class':"facts__label"})
    #soup = content_sec.find("div", text="Project Scope")
    ##print(description)


class PayforSuccess(object):
    def __init__(self, aside, content_sec):

        self.phase = None
        self.level = None
        self.level_name = None
        self.level_state = None
        self.description = None
        self.scope = None
        self.implementation = None
        self.service_period = None
        self.document_type = None
        self.source_link = None
        self.download_link = None
        self.opportunity_status = None
        self.avail_funding = None
        self.stakeholder = None
        self.interventions = None
        self.np_issue_areas = None
        self.motivation = None
        self.objective = None
        self.population_served = None
        self.geography = None
        self.p_issue_areas = None
        self.service_provider = None
        self.payor = None
        self.transaction_coordinator = None
        self.evaluator = None
        self.validator = None
        self.project_manager = None
        self.external_counsel = None
        self.technical_assist_provider = None
        self.senior_debt = None
        self.junior_debt = None
        self.deferred_fee = None
        self.recoverable_grant = None
        self.non_recoverable = None
        self.guarantor = None
        self.initial_inv = None
        self.max_repayment_by_payor = None
        self.service_term = None
        self.repayment_period = None
        self.interim_outcomes = None
        self.recycling = None

    def __contains__(self, string):
        if string in self.name:
            return True
        else:
            return False

class Legislation(PayforSuccess):
    def __init__(self, aside, content_sec):
        PayforSuccess.__init__(self, aside, content_sec)
        self.name = None
        self.analysis(aside, content_sec)

        #self.description = re.sub(' +',' ', content_sec.get_text().strip())
    def __str__(self):
        return "{} has been uploaded and is now a Legislation instance.".format(self.name)

    def analysis(self, aside, content_sec):
        try:
            doc= aside.find(text=re.compile('Document Type'))
            self.document_type = doc.find_parent('div').find_parent('div').ul.get_text().strip()
            #print("Document Type is: " + self.document_type)
        except:
            self.document_type  = "N/A"

            #print("Document Type is: " + self.document_type)

        try:
            link= aside.find(text=re.compile('View Source'))
            self.source_link = link.find_parent("a").get('href')
            #print("Source Link is : " + self.source_link)
        except:
            self.source_link  = "N/A"
            #print("Source Link is : " + self.source_link)

        try:
            link= aside.find(text=re.compile('Download'))
            self.download_link = link.find_parent("a").get('href')
            #print("Download: " + self.download_link)
        except:
            self.download_link  = "N/A"
            #print("Download : " +self.download_link)

    def __repr__(self):
        self.car

class Opportunity(PayforSuccess):
    def __init__(self, aside, content_sec):
        PayforSuccess.__init__(self, aside, content_sec)
        self.name = None
        #self.description = re.sub(' +',' ', content_sec.get_text().strip())
        self.analysis(aside, content_sec)

    def __repr__(self):
        return "{} has been turned into a Oppotunity instance. It status is: {}.".format(self.name, self.opportunity_status)

    def __str__(self):
        return "{} has been uploaded and is now an Opportunity instance.".format(self.name)

    def analysis(self, aside, content_sec):
        try:
            link= aside.find(text=re.compile('Download'))
            self.download_link = link.find_parent("a").get('href')
            #print("Download: " + self.download_link)
        except:
            self.download_link  = "N/A"

            #print("Download : " + self.download_link)


        try:
            link= aside.find(text=re.compile('Opportunity Status'))
            self.opportunity_status = link.find_parent("div").find_parent('div').ul.get_text().strip()
            #print("Opportunity Status is : " + self.opportunity_status)
        except:
            self.opportunity_status  = "N/A"

            #print("Opportunity Status is : " + self.opportunity_status)

        try:
            link= aside.find(text=re.compile('Available Funding'))
            self.avail_funding = link.find_parent("div").find_parent('div').ul.get_text().strip()
            #print("Available Funding : " + self.avail_funding)
        except:
            self.avail_funding  = "N/A"
            #print("Available Funding : " + self.avail_funding)

        try:
            link= aside.find(text=re.compile('Stakeholders'))
            self.stakeholder = link.find_parent("div").find_parent('div').find('ul').find_all('a')
            temp = []
            for each in self.stakeholder:
                temp.append(each.get_text().strip())
            self.stakeholder = ', '.join(map(str, temp))
            #print("Stakeholders : " + self.stakeholder)
        except:
            self.stakeholder  = "N/A"
            #print("Stakeholders : " + self.stakeholder)

        try:
            link= aside.find(text=re.compile('Interventions'))
            self.interventions = link.find_parent("div").find_parent('div').find('ul').find_all('a')
            temp = []
            for each in self.interventions:
                temp.append(each.get_text().strip())
            self.interventions = ', '.join(map(str, temp))
            #print("Interventions: "  + self.interventions)
        except:
            self.interventions  = "N/A"
            #print("Interventions :"  + self.interventions)

        try:
            link= aside.find(text=re.compile('Issue Area'))
            self.np_issue_areas = link.find_parent("div").find_parent('div').find('ul').find_all('a')
            temp = []
            for each in self.np_issue_areas:
                temp.append(each.get_text().strip())
            self.np_issue_areas = ', '.join(map(str, temp))
            #print("Issue Area(s): "  + self.np_issue_areas)
        except:
            self.np_issue_areas  = "N/A"
            #print("Issue Area(s): "  + self.np_issue_areas)
        #Need code for description

class Project(PayforSuccess):
    def __init__(self, aside, content, teaser, content_sec):
        PayforSuccess.__init__(self, aside, content_sec)
        self.analysis(aside, content, teaser, content_sec)
        self.name = None
        #self.description = re.sub(' +',' ', content_sec.get_text().strip())
    def __repr__(self):
        return "Project {} has been turned into a Project instance. It has the following issues areas: {}. The initial investment is: {}.".format(self.name, self.p_issue_areas, self.initial_inv)

    def __str__(self):
        return "{} has been uploaded and is now a Project instance.".format(self.name)


    def analysis(self, aside, content, teaser, content_sec):
        ### Analysis in Project Page
        try:
            link= aside.find(text=re.compile('Current Phase'))
            phase = link.find_parent("div").find_parent('div').find('ul').get_text()
            self.phase = phase.strip()
            #print("Issue Area(s): "  + self.np_issue_areas)
        except:
            self.phase  = "N/A"
        #### Market Overview
        name = ["Motivation", "Project Objective", "Individuals Served", "Geography", "Domain", "Initial Investment ($ millions)"]
        analysis = ["Motivation", "Project Objective\(s\)", "Individuals Served", "Geography", "Issue Area", "Initial Investment \($ millions\) [Note 2]"]
        analyzed = [self.motivation, self.objective, self.population_served, self.geography, self.p_issue_areas, self.initial_inv]

        for i in range(len(analysis)):
            try:
                link= content.find(text=re.compile(analysis[i]))
                stake = link.find_parent("div").find_parent('li').find_all('div')
                temp = []
                temp.append(stake[1].get_text().strip())
                analyzed[i] = ', '.join(map(str, temp))
                #print(name[i]+": " + analyzed[i])
            except:
                analyzed[i]  = "N/A"
                if analysis[i] == "Issue Area":
                    try:
                        link= aside.find(text=re.compile('Issue Area'))
                        issue = link.find_parent("div").find_parent('div').find('ul').find_all('a')
                        temp = []
                        for each in issue:
                            temp.append(each.get_text().strip())
                        issue = ', '.join(map(str, temp))
                        analyzed[4] = issue
                        #print("Issue Area(s): "  + self.np_issue_areas)
                    except:
                        analyzed[4] = "N/A"
                #print(name[i]+": " + analyzed[i])

        self.motivation = analyzed[0]
        self.objective = analyzed[1]
        self.population_served = analyzed[2]
        self.geography = analyzed[3]
        self.p_issue_areas = analyzed[4]
        self.initial_inv = analyzed[5]
        ### Analysis in Project Page
        #### Project Partners

        name = ["Service Provider(s)", "Payor(s)", "Transaction Coordinator(s)", "Evaluator", "Validator", "Project Manager", "External Legal Counsel", "Technical Assistance Provider(s)"]
        analysis = ["Service Provider\(s\)", "Payor\(s\)", "Transaction Coordinator\(s\)", "Evaluator", "Validator", "Project Manager", "External Legal Counsel", "Technical Assistance Provider\(s\)"]
        analyzed = [self.service_provider, self.payor, self.transaction_coordinator, self.evaluator, self.validator, self.project_manager, self.external_counsel, self.technical_assist_provider]
        for i in range(len(analysis)):
            try:
                link= content.find(text=re.compile(analysis[i]))
                stake = link.find_parent("div").find_parent('li').find_all('div')
                temp = []
                temp.append(stake[1].get_text().strip())
                analyzed[i] = ', '.join(map(str, temp))
                #print(name[i]+": " + analyzed[i])
            except:
                back_up = teaser.find_all('div', {"class":"teaser--listing"})
                analyzed[i] = "N/A"
                for each in back_up:
                    check = each.find('li').get_text()
                    textt = each.find('h2').get_text()
                    if "intermediary" in '**{}**'.format(check.lower()):
                        analyzed[2] = textt.strip()
                    elif "payor" in '**{}**'.format(check.lower()):
                        analyzed[1] = textt.strip()
                    elif "service provider" in '**{}**'.format(check.lower()):
                        analyzed[0] = textt.strip()
                    else:
                        pass
                #print(name[i]+": " + analyzed[i])

        self.service_provider = analyzed[0]
        self.payor = analyzed[1]
        self.transaction_coordinator = analyzed[2]
        self.evaluator = analyzed[3]
        self.validator = analyzed[4]
        self.project_manager = analyzed[5]
        self.external_counsel = analyzed[6]
        self.technical_assist_provider = analyzed[7]

        ### Analysis in Project Page
        #### Financing
        analysis = ["Senior Investor", "Subordinate Investor", "Deferred Fee Source and Total Deferred Fees", "Recoverable Grant Source", "Non-recoverable Grant Source ", "Guarantor"]
        name = ["Senior Investor ($MM)", "Subordinate Investor ($MM)", "Deferred Fee Source and Total Deferred Fees", "Recoverable Grant Source and Total Recoverable Grants ($MM)", "Non-recoverable Grant Source and Total Non-recoverable Grants ($MM)", "Guarantor and Guarantee ($MM)"]
        analyzed = [self.senior_debt, self.junior_debt, self.deferred_fee, self.recoverable_grant, self.non_recoverable, self.guarantor]

        for i in range(len(analysis)):
            try:
                link= content.find(text=re.compile(analysis[i]))
                stake = link.find_parent("div").find_parent('li').find_all('div')
                temp = []
                temp.append(stake[1].get_text().strip())
                analyzed[i] = ', '.join(map(str, temp))
                #print(name[i]+": " + analyzed[i])
            except:
                analyzed[i]  = "N/A"
                #print(name[i]+": " + analyzed[i])

        self.senior_debt = analyzed[0]
        self.junior_debt = analyzed[1]
        self.deferred_fee = analyzed[2]
        self.recoverable_grant = analyzed[3]
        self.non_recoverable = analyzed[4]
        self.guarantor = analyzed[5]


        #### Repayment

        name = ["Initial Investment", "Maximum Repayment Funds", "Full service delivery", "Full repayment period", "Interim outcomes reported and tied to payments?", " Recycling of Funds"]
        analysis = ["Initial Investment", "Maximum Repayment Funds", "Full service delivery", "Full repayment period", "Interim outcomes reported?", " Recycling of Funds"]
        analyzed = [self.initial_inv, self.max_repayment_by_payor, self.service_term, self.repayment_period, self.interim_outcomes, self.recycling]

        for i in range(len(analysis)):
            try:
                link= content.find(text=re.compile(analysis[i]))
                stake = link.find_parent("div").find_parent('li').find_all('div')
                temp = []
                temp.append(stake[1].get_text().strip())
                analyzed[i] = ', '.join(map(str, temp))
                #print(name[i]+": " + analyzed[i])
            except:
                analyzed[i]  = "N/A"
                #print(name[i]+": " + analyzed[i])

        self.initial_inv = analyzed[0]
        self.max_repayment_by_payor = analyzed[1]
        self.service_term = analyzed[2]
        self.repayment_period = analyzed[3]
        self.interim_outcomes = analyzed[4]
        self.recycling = analyzed[5]

#project = Project(aside, content, teaser, content_sec)
#print(project.guarantor)
#print(project.senior_debt)
#print(project.transaction_coordinator)
#print(project.service_provider)
#print(project.p_issue_areas)
#print(project.phase)


##print(project.description)


    ##print(interv_text)s
    ##printed = interv_text.find_all('a').get_text()
    ##print("Project Status is: " + status)
