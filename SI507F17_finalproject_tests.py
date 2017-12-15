import unittest
import json
from set_up import *
from SI507_FinalProject import *

###########
class TestingSetup(unittest.TestCase):

	def setUp(self):
		self.set_up = False
		self.test_url = 'http://www.payforsuccess.org/activity/?facets%5B0%5D=activity_type%3Aproject&sort=recent'
		self.test_indicator = "Test"
		self.test_filename = "Test.json"

	def test_Raise_FileError(self):
		with self.assertRaises(FileNotFoundError):
			f = open(self.test_filename, 'r')

	def test_Fail_Raise_FileError(self):
		grabPage(self.test_url, self.test_filename, self.test_indicator)
		with self.assertRaises(FileNotFoundError):
			f = open(self.test_filename, 'r')

	def test_set_up(self):
		self.set_up = set_me_up()
		self.assertTrue(self.set_up, True)

	def test_dictionary_merge(self):
		set_me_up()
		with open('Project.json', 'r') as f:
			proj = json.loads(f.read())
			f.close()

		with open('Opportunity.json', 'r') as f:
			opps = json.loads(f.read())
			f.close()

		with open('Legislation.json', 'r') as f:
			law = json.loads(f.read())
			f.close()

		with open('Master.json', 'r') as f:
			mast = json.loads(f.read())
			f.close()

		z = {**proj, **law}
		a = {**z, **opps}
		self.assertTrue(len(a), len(mast))

class TestingClasses(unittest.TestCase):
	def setUp(self):
		set_me_up()
		with open("Master.json", 'r') as f:
			self.dictionary = json.loads(f.read())
			f.close()
		dic_keys = []
		for key in self.dictionary.keys():
		    dic_keys.append(key)
		self.some_key = dic_keys[4]

		bsObj = connect_cache(self.dictionary[self.some_key])
		main = bsObj.find('div', {'class':"main"})
		content = bsObj.find('div', {'class':"content"})
		aside = bsObj.find('aside', {'class':"sidebar"})
		teaser = main.find('div', {"class":"teasers"})
		content_sec = main.find('div', {'class':"facts__content"})

		self.project_instance = Project(aside, content, teaser, content_sec)


	def test_filename_in_Dict(self):
		try:
		    attempt = self.dictionary[self.some_key]["filename"]
		except:
		    counter = 0
		    for each in self.dictionary:
		        self.dictionary[each]["filename"] = "project{}.html".format(counter)
		        counter += 1
		obj = connect_cache(self.dictionary[self.some_key])
		self.assertTrue(type(obj), "<class 'bs4.BeautifulSoup'>")

	def test_return_BSObj(self):
		try:
		    attempt = self.dictionary[self.some_key]["filename"]
		except:
		    counter = 0
		    for each in self.dictionary:
		        self.dictionary[each]["filename"] = "project{}.html".format(counter)
		        counter += 1

		obj = connect_cache(self.dictionary[self.some_key])
		self.assertTrue(type(obj), "<class 'bs4.BeautifulSoup'>")

	def test_project_Instance(self):
		try:
		    attempt = self.dictionary[self.some_key]["filename"]
		except:
		    counter = 0
		    for each in self.dictionary:
		        self.dictionary[each]["filename"] = "project{}.html".format(counter)
		        counter += 1
		bsObj = connect_cache(self.dictionary[self.some_key])
		main = bsObj.find('div', {'class':"main"})
		content = bsObj.find('div', {'class':"content"})
		aside = bsObj.find('aside', {'class':"sidebar"})
		teaser = main.find('div', {"class":"teasers"})
		content_sec = main.find('div', {'class':"facts__content"})

		projectw = Project(aside, content, teaser, content_sec)
		project = sendInstances()
		self.assertEqual(type(project[0]), type(projectw))

	def test_repr_method(self):
		string = "Project {} has been turned into a Project instance. It has the following issues areas: {}. The initial investment is: {}.".format(self.project_instance.name, self.project_instance.p_issue_areas, self.project_instance.initial_inv)
		self.assertEqual(print(self.project_instance.__repr__(), string))

	def test_contains(self):
		temp = self.project_instance.name
		temp = check.split()
		self.assertTrue(temp[0] in self.project_instance)

	def test_access_to_DB(self):
		db_user = "nomyusername"
		db_password = "notmypassword"
		conn = None
		cur = None
		with self.assertRaises(Exception):
			conn, cur = get_connection_and_cursor()
			setup_database(conn, cur)

	def test_approved_access_to_DB(self):
		##PLease enter you crendential for this test to workforce
		b_user = "nomyusername"
		db_password = "notmypassword"
		conn = None
		cur = None
		with self.assertRaises(Exception):
			conn, cur = get_connection_and_cursor()
			setup_database(conn, cur)

class TestingFilesExist(unittest.TestCase):

		def setUp(self):
		self.master = open("Master.json")
		self.project = open("Project.json")
		self.legislation = open("Legislation.json")
		self.opportunity = open("Opportunity.json")

	def test_files_exist(self):
		self.assertTrue(json.loads(self.master.read()))
		self.assertTrue(json.loads(self.project.read()))
		self.assertTrue(json.loads(self.legislation.read()))
		self.assertTrue(json.loads(self.opportunity.read()))

	def database_name(self):
		self.assertEqual(dbname, "payforsuccessprojects")


	def test_base_url(self):
		self.assertEqual(base_url1, 'http://www.payforsuccess.org/activity/?facets%5B0%5D=activity_type%3Aproject&sort=recent')
		self.assertEqual(base_url2, 'http://www.payforsuccess.org/activity/?facets%5B0%5D=activity_type%3Aopportunity&sort=recent')
		self.assertEqual(base_url3, 'http://www.payforsuccess.org/activity/?facets%5B0%5D=activity_type%3Aresource&sort=recent')

	def test_viz_file_exists(self):
		with self.assertRaises(Exception):
			self.master = open("Master.json")

	def test_chrome_selenium_driver(self):
		with self.assertRaises(Exception):
			base_url = 'http://www.payforsuccess.org/activity/?facets%5B0%5D=activity_type%3Aproject&sort=recent'
			driver = webdriver.Chrome()
		    driver.get(base_url)
			html = driver.page_source
			driver.quit()

	def test_viz_datafile_exists(self):
		with self.assertRaises(Exception):
			self.master = open("viz_data.json")

	def tearDown(self):
		self.master.close()
		self.project.close()
		self.legislation.close()
		self.opportunity.close()

#comment
if __name__ == "__main__":
    unittest.main(verbosity=4)
