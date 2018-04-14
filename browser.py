from selenium import webdriver
import time
import webbrowser
from pykeyboard import PyKeyboard
from six.moves import html_parser
import string


def log_in():
	sign_in_url="https://courses.edx.org/login"
	email=""
	pswrd=""

	driver.get(sign_in_url)
	time.sleep(2)
	driver.find_element_by_id("login-email").send_keys(email)
	driver.find_element_by_id("login-password").send_keys(pswrd)

	signInButton = driver.find_element_by_class_name("login-button") 
	signInButton.click() 


def scroll(driver):
	#set it to more that 2s, to render the page
	SCROLL_PAUSE_TIME = 2

	# Get scroll height
	last_height = driver.execute_script("return document.body.scrollHeight")

	while True:
	    # Scroll down to bottom
	    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

	    # Wait to load page
	    time.sleep(SCROLL_PAUSE_TIME)

	    # Calculate new scroll height and compare with last scroll height
	    new_height = driver.execute_script("return document.body.scrollHeight")
	    if new_height == last_height:
	        break
	    last_height = new_height


def auto_enroll(driver, course_category):

	course_category_url=course_category.replace("&","%20%26%20")
	
	url = "https://www.edx.org/course?subject="+course_category_url+"&availability=archived&language=English"
	driver.get(url) #navigate to the page

	#scroll down the page to retrive all courses
	#scroll(driver)

	courses = driver.find_elements_by_class_name("course-link")

	
	course_urls=[] # all retreived courses
	for course in courses:
		course_url=course.get_attribute("href")
		course_urls.append(course_url);

	count=0
	print ("Total number of courses: {0}".format(len(course_urls)))

	file_course_categ= open(course_category+".txt","a+")# append a new text to the already existing file or the new file
	for url in course_urls:
		
		print(count)
		print (url)
		driver.get(url)#navigate to the page

		try:
			time.sleep(1)
			link_to_enroll=driver.find_element_by_class_name("js-enroll-btn ").get_attribute("href")#btn btn-cta txt-center js-enroll-btn
			link_to_enroll=link_to_enroll.replace("email_opt_in=true", "email_opt_in=false")
			print(link_to_enroll)
			course_title=driver.find_element_by_class_name("course-intro-heading").text
			print (course_title)
			course_title=clean_filename(course_title)
			file_course_categ.write('{0:80}  {1}\n'.format(course_title, course_category))	
			# Open URL in a new tab, if a browser window is already open.
			webbrowser.open(link_to_enroll)
			time.sleep(10)
			#keyboard.send('ctrl+w')
			keyboard = PyKeyboard()
			keyboard.press_keys(['Command','w'])

			count+=1
		except Exception as e: 
			print(e)
			pass
	

#function from edx_crawler/lib/utils.py
def clean_filename(s, minimal_change=False):
    """
    Sanitize a string to be used as a filename.
    If minimal_change is set to true, then we only strip the bare minimum of
    characters that are problematic for filesystems (namely, ':', '/' and
    '\x00', '\n').
    """

    # First, deal with URL encoded strings
    h = html_parser.HTMLParser()
    s = h.unescape(s)

    # strip paren portions which contain trailing time length (...)
    s = (
        s.replace(':', '-')
        .replace('/', '-')
        .replace('\x00', '-')
        .replace('\n', '')
    )

    if minimal_change:
        return s

    s = s.replace('(', '').replace(')', '')
    s = s.rstrip('.')  # Remove excess of trailing dots

    s = s.strip().replace(' ', '_')
    valid_chars = '-_.()%s%s' % (string.ascii_letters, string.digits)
    return ''.join(c for c in s if c in valid_chars)


def main():
	chromedriver_loc = '/Users/zarina/Desktop/Temp/chromedriver'
	driver = webdriver.Chrome(executable_path=chromedriver_loc)
	#log_in()
	course_category="Business&Management"
	auto_enroll(driver, course_category)


if __name__== "__main__":
	main()		
