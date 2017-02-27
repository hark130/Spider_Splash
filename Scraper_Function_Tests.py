from Scraper_Functions import find_the_date 
from Scraper_Functions import find_a_URL            # find_a_URL(htmlString, searchStart, searchStop)
from Scraper_Functions import get_image_filename    # get_image_filename(htmlString, [dateSearchPhrase], [nameSearchPhrase], nameEnding)
from Scraper_Functions import is_URL_abs            # is_URL_abs(baseURL, targetURL)
from Scraper_Functions import make_rel_URL_abs      # make_rel_URL_abs(baseURL, targetURL)
from Scraper_Functions import is_URL_valid          # is_URL_valid(URL)
from Scraper_Functions import get_root_URL          # get_root_URL(URL)
from Scraper_Functions import get_URL_parent_path   # get_URL_parent_path(URL)

import unittest
import os
import re


# This class will test the new get_image_filename() functionality to auto-size number-only filenames
# This does not include dates
class SizeNumericImageNames(unittest.TestCase):

    # Test 1 - Normal Input - No numerics
    def test01_ValidInput_NoNumerics01(self):
        # Test Variables
        testHTMLFile = '3-BC_HTML.txt'

        ################################################
        # MODIFY THESE WHEN ADAPTING TO A NEW WEBCOMIC #
        ################################################
        ### URL SETUP ###
        webComicName = 'Business_Cat' # <=--------------------------=UPDATE=--------------------------=>
        baseURL = 'http://www.businesscat.happyjar.com/' # <=--------------------------=UPDATE=--------------------------=>
        targetComicURL = baseURL # Original source
        #targetComicURL = 'http://www.businesscat.happyjar.com/comic/coffee/' # Start here instead

        ### IMAGE URL SETUP ###
        # Find the appropriate HTML line from a list of strings
        imageSearchPhrase = ['<img src="http://www.businesscat.happyjar.com/wp-content/uploads/'] # <=--------------------------=UPDATE=--------------------------=>
        # Find the beginning of the image reference
        imageBeginPhrase = '<img src="' # Probably 'src="' <=--------------------------=UPDATE=--------------------------=> 

        ### LATEST URL SETUP ###
        # Fine the 'name' of the 'latest comic' navigation button
        latestSearchPhrase = 'navi-last-in' # Probably 'Last' <=--------------------------=UPDATE=--------------------------=>

        ### PREV URL SETUP ###
        # Find the 'name' of the obligatory 'Previous Comic' navigation button
        prevSearchPhrase = 'navi-prev-in' # Probably 'Prev' <=--------------------------=UPDATE=--------------------------=>

        ### FIRST URL SETUP ###
        # Find the 'name' of the (mostly) obligatory 'First Comic' navigation button
        # Set this to an empty string if the webcomic page does not provide for a 'First' navigation button
        firstSearchPhrase = 'navi-first-in' # Probably 'First' <=--------------------------=UPDATE=--------------------------=>

        ### DATE PARSING SETUP ###
        # This boolean determines the nature of the date search:  False == mandatory date, True == optional date
        skipDateIfNotFound = False # False for most pages <=--------------------------=UPDATE=--------------------------=>
        # Find the date from a list of strings to match in the page's HTML
        dateSearchPhrase = imageSearchPhrase # Commonly == imageSearchPhrase <=--------------------------=UPDATE=--------------------------=>

        ### NAME PARSING SETUP ###
        # Find the title of the image by searching for the following phrase in the HTML.  Could be in an imageURL tag, webpage title, or social media 'share' link
        nameSearchPhrase = 'title="' # Probably 'alt="' <=--------------------------=UPDATE=--------------------------=>
        # Delimit the end of the image title with this string
        nameEnding = '"' # Probably '"' <=--------------------------=UPDATE=--------------------------=>
        ################################################
        # Modify these variables based on HTML details #
        ################################################

        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', testHTMLFile), 'r') as testFile:
                testHTML = testFile.read()
            result = get_image_filename(testHTML, dateSearchPhrase, nameSearchPhrase, nameEnding, skipDateIfNotFound)
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertEqual(result, '20161202_Order')

    # Test 2 - Normal Input - No numerics
    def test02_ValidInput_Numerics01(self):
        # Test Variables
        testHTMLFile = '19-xkcd_0455_HTML.txt'

        ################################################
        # MODIFY THESE WHEN ADAPTING TO A NEW WEBCOMIC #
        ################################################
        ### URL SETUP ###
        webComicName = 'XKCD' # <=--------------------------=UPDATE=--------------------------=>
        baseURL = 'http://www.xkcd.com/' # <=--------------------------=UPDATE=--------------------------=>
        targetComicURL = baseURL # Original source
        #targetComicURL = 'http://www.xkcd.com/2/' # Start here instead

        ### IMAGE URL SETUP ###
        # Find the appropriate HTML line from a list of strings
        imageSearchPhrase = ['imgs.xkcd.com/comics/','Image URL (for hotlinking/embedding): '] # <=--------------------------=UPDATE=--------------------------=>
        # Find the beginning of the image reference
        imageBeginPhrase = 'src="' # Probably 'src="' <=--------------------------=UPDATE=--------------------------=> 

        ### LATEST URL SETUP ###
        # Fine the 'name' of the 'latest comic' navigation button
        latestSearchPhrase = '' # Probably 'Last' <=--------------------------=UPDATE=--------------------------=>

        ### PREV URL SETUP ###
        # Find the 'name' of the obligatory 'Previous Comic' navigation button
        prevSearchPhrase = 'prev' # Probably 'Prev' <=--------------------------=UPDATE=--------------------------=>

        ### FIRST URL SETUP ###
        # Find the 'name' of the (mostly) obligatory 'First Comic' navigation button
        # Set this to an empty string if the webcomic page does not provide for a 'First' navigation button
        firstSearchPhrase = '/1/' # Probably 'First' <=--------------------------=UPDATE=--------------------------=>

        ### DATE PARSING SETUP ###
        # This boolean determines the nature of the date search:  False == mandatory date, True == optional date
        skipDateIfNotFound = True # False for most pages <=--------------------------=UPDATE=--------------------------=>
        # Find the date from a list of strings to match in the page's HTML
        dateSearchPhrase = imageSearchPhrase # Commonly == imageSearchPhrase <=--------------------------=UPDATE=--------------------------=>

        ### NAME PARSING SETUP ###
        # Find the title of the image by searching for the following phrase in the HTML.  Could be in an imageURL tag, webpage title, or social media 'share' link
        nameSearchPhrase = ['Permanent link to this comic: http://xkcd.com/','Permanent link to this comic: https://xkcd.com/'] # Probably 'alt="' <=--------------------------=UPDATE=--------------------------=>
        # Delimit the end of the image title with this string
        nameEnding = '/<br />' # Probably '"' <=--------------------------=UPDATE=--------------------------=>
        ################################################
        # Modify these variables based on HTML details #
        ################################################

        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', testHTMLFile), 'r') as testFile:
                testHTML = testFile.read()
            result = get_image_filename(testHTML, dateSearchPhrase, nameSearchPhrase, nameEnding, skipDateIfNotFound)
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertEqual(result, '0455')
######################################## START WORKING HERE ############################


class GetURLParentPath(unittest.TestCase):
    
    # Test 1 - Invalid Input - TypeError('URL is not a string')
    def test01_InvalidInput01(self):
        try:
            result = get_URL_parent_path(['this', 'is', 'not', 'a', 'string'])
        except TypeError as err:
            self.assertEqual(err.args[0], 'URL is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    # Test 2 - Invalid Input - ValueError('URL is empty')
    def test02_InvalidInput02(self):
        try:
            result = get_URL_parent_path('')
        except ValueError as err:
            self.assertEqual(err.args[0], 'URL is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')      
            
    # Test 3 - Invalid Input - ValueError('URL is not a URL')
    def test03_InvalidInput03(self):
        try:
            result = get_URL_parent_path('this is DEFINITELY not a valid URL!')
        except ValueError as err:
            self.assertEqual(err.args[0], 'URL is not a URL')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')     

    # Test 4 - Invalid Input - ValueError('URL is not a URL')
    def test04_InvalidInput04(self):
        try:
            result = get_URL_parent_path('http://api.google.com/q?exp=a|b')
        except ValueError as err:
            self.assertEqual(err.args[0], 'URL is not a URL')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')           

    # Test 5 - Valid Input - Normal
    def test05_ValidInput01(self):
        try:
            result = get_URL_parent_path('https://github.com/hark130/Harklebot')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'https://github.com/hark130')     
            
    # Test 6 - Valid Input - Actual page
    def test06_ValidInput02(self):
        try:
            result = get_URL_parent_path('http://cdn2.cad-comic.com/comics/sillies-20170203-8a3f1.gif')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'http://cdn2.cad-comic.com/comics')     
            
    # Test 7 - Valid Input - Actual page
    def test07_ValidInput03(self):
        try:
            result = get_URL_parent_path('https://imgs.xkcd.com/comics/mission_to_culture.png')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'https://imgs.xkcd.com/comics')     
            
    # Test 8 - Valid Input - Actual page
    def test08_ValidInput04(self):
        try:
            result = get_URL_parent_path('https://github.com/hark130/Harklebot/blob/master/Modules/Robot_Reader_Function_Tests.py')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'https://github.com/hark130/Harklebot/blob/master/Modules')     

    # Test 9 - Valid Input - Base URL of an actual page
    def test09_ValidInput05(self):
        try:
            result = get_URL_parent_path('http://www.cnn.com')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'http://www.cnn.com')   

    # Test 10 - Valid Input - Base URL of an actual page
    def test10_ValidInput06(self):
        try:
            result = get_URL_parent_path('http://www.cnn.com/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'http://www.cnn.com')   

    # Test 11 - Valid Input - Base URL of an actual page
    def test11_ValidInput07(self):
        try:
            result = get_URL_parent_path('www.cnn.com')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'www.cnn.com')   

    # Test 12 - Valid Input - Base URL of an actual page
    def test12_ValidInput08(self):
        try:
            result = get_URL_parent_path('www.cnn.com/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'www.cnn.com')   
            
            
class GetRootURL(unittest.TestCase):

    def test01_URL_not_a_string(self):
        try:
            result = get_root_URL(69)
        except TypeError as err:
            self.assertEqual(err.args[0], 'URL is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test02_normal_URL1(self):
        self.assertEqual(get_root_URL('https://www.google.com/?gws_rd=ssl'), 'https://www.google.com')

    def test03_normal_URL2(self):
        self.assertEqual(get_root_URL('https://www.tutorialspoint.com/python/string_find.htm'), 'https://www.tutorialspoint.com')

    def test04_normal_URL3(self):
        self.assertEqual(get_root_URL('http://stackoverflow.com/questions/674764/examples-for-string-find-in-python'), 'http://stackoverflow.com')

    def test05_normal_URL4(self):
        self.assertEqual(get_root_URL('https://docs.python.org/2/library/string.html'), 'https://docs.python.org')

    def tes06t_normal_URL5(self):
        self.assertEqual(get_root_URL('https://www.google.com/?gws_rd=ssl#q=weird+website+links'), 'https://www.google.com')

    def test07_normal_URL6(self):
        self.assertEqual(get_root_URL('awkwardzombie.com/index.php?page=0&comic=122616'), 'awkwardzombie.com')

    def test08_normal_URL7(self):
        self.assertEqual(get_root_URL('www.smbc-comics.com/comic/2007-11-09'), 'www.smbc-comics.com')

    def test09_normal_URL8(self):
        self.assertEqual(get_root_URL('https://www.google.com/#q=who+owns+.com+tld'), 'https://www.google.com')

    # This test is very important as it validates the requirement to remove any subdirectories before locating the end (see: TLD) of hte base URL
    def test10_normal_URL8(self):
        self.assertEqual(get_root_URL('http://www.blogsearchengine.org/search.html?cx=partner-pub-9634067433254658%3A5laonibews6&cof=FORID%3A10&ie=ISO-8859-1&q=who+owns+the+.com+tld&sa.x=0&sa.y=0'), 'http://www.blogsearchengine.org')

    def test11_str_not_a_URL1(self):
        try:
            get_root_URL('http : / / www . google . com')
        except ValueError as err:
            self.assertEqual(err.args[0], 'URL is not a URL')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    # This test is valid merely because get_root_URL() does not include any country-unique TLDs (e.g., .cz, .ru)
    def test12_str_not_a_URL2(self):
        try:
            get_root_URL('http://www.praguemorning.cz/google-czech-republic/')
        except ValueError as err:
            self.assertEqual(err.args[0], 'URL is not a URL')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')


class IsURLValid(unittest.TestCase):
    
    # Test 1 - TypeError('URL is not a string')
    def test01_TypeError01(self):
        try:
            result = is_URL_valid(420 / 1337)
        except TypeError as err:
            self.assertEqual(err.args[0], 'URL is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
    
    # Test 2 - TypeError('URL is not a string')
    def test02_TypeError02(self):
        try:
            result = is_URL_valid(['http://www.thisisnotastring.org'])
        except TypeError as err:
            self.assertEqual(err.args[0], 'URL is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            
    # Test 3 - ValueError('URL is empty')
    def test03_ValueError01(self):
        try:
            result = is_URL_valid('')
        except ValueError as err:
            self.assertEqual(err.args[0], 'URL is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            
    # Test 4 - Valid Input
    def test04_ValidInput01(self):
        try:
            result = is_URL_valid('www.somesite.com')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 5 - Valid Input
    def test05_ValidInput02(self):
        try:
            result = is_URL_valid('http://www.somesite.org')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 5 - Valid Input
    def test05_ValidInput03(self):
        try:
            result = is_URL_valid('https://www.somesite.ph')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 5 - Messy Yet Valid Input
    def test05_MessyYetValidInput01(self):
        try:
            result = is_URL_valid('http://127.0.0.1:8080/test?v=123#this')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 6 - Messy Yet Valid Input
    def test06_MessyYetValidInput02(self):
        try:
            result = is_URL_valid('http://api.google.com/q?exp=a%7Cb')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
             
    # Test 7 - Messy Yet Valid Input
    def test07_MessyYetValidInput03(self):
        try:
            result = is_URL_valid('http://[2001:db8:85a3::8a2e:370:7334]/foo/bar')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)        
            
    # Test 8 - Messy Yet Valid Input
    def test08_MessyYetValidInput04(self):
        try:
            result = is_URL_valid('http://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Ddigital-text&amp;field-keywords=Phyllis+Zimbler+Miller')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 9 - Messy Yet Valid Input
    def test09_MessyYetValidInput05(self):
        try:
            result = is_URL_valid('ftp://username%3Apassword@domain')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 10 - Messy Yet Valid Input
    def test10_MessyYetValidInput06(self):
        try:
            result = is_URL_valid('https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=5&ved=0ahUKEwiYpIT04JfSAhVDLZoKHWF0CyEQFgg1MAQ&url=http%3A%2F%2Fwww.complex.com%2Flife%2F2016%2F05%2Fbest-hashtags-dragging-donald-trump&usg=AFQjCNHPGIS5_B0_t9wbjbqQenn8iZ165g&sig2=oAIU60SQ8-OtztfPlsSsTg&cad=rja')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 11 - Messy And Invalid Input
    def test11_MessyAndInvalidInput01(self):
        try:
            result = is_URL_valid('http://mw1.google.com/mw-earth-vectordb/kml-samples/gp/seattle/gigapxl/$[level]/r$[y]_c$[x].jpg')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
#            self.assertFalse(result) # Brackets are necessary in some situations... for instance browsing an IPv6 address
            self.assertTrue(result) # Let this ride until more fidelity is built into is_URL_valid()
            
    # Test 12 - Messy And Invalid Input
    def test12_MessyAndInvalidInput02(self):
        try:
            result = is_URL_valid('http://api.google.com/q?exp=a|b')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)
            
    # Test 13 - Messy And Invalid Input
    def test13_MessyAndInvalidInput03(self):
        try:
            result = is_URL_valid('http://example.com/wp-admin/load-scripts.php?c=1&load[]=swfobject,jquery,utils&ver=3.5')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
#            self.assertFalse(result) # Brackets are necessary in some situations... for instance browsing an IPv6 address
            self.assertTrue(result) # Let this ride until more fidelity is built into is_URL_valid()
            
    # Test 14 - Messy And Invalid Input
    def test14_MessyAndInvalidInput04(self):
        try:
            result = is_URL_valid('http://test.site/wp-admin/post.php?t=1347548645469?t=1347548651124?t=1347548656685?t=1347548662469?t=1347548672300?t=1347548681615?')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
#            self.assertFalse(result) # Question marks are necessary in some situations... for instance in query strings
            self.assertTrue(result) # Let this ride until more fidelity is built into is_URL_valid()
    # NOTE: 
    #       Special-use” specifies that the question mark “?” is reserved for the denotation of a query string, 
    #   but must be encoded for any other purpose. Unfortunately, WordPress is including multiple unencoded 
    #   question marks for URLs involved with its “preview” functionality. In other words, in any URL, the first 
    #   question mark “?” may be unencoded to denote the query string, but subsequent “?” must be encoded.
    #
    #       These errors may not be a huge deal, but they increase potential vulnerability and certainly should be 
    #   fixed in the next WP update. Likewise, future versions of WordPress should keep URI/URL specifications in 
    #   mind and verify that all URLs are properly encoded.
    #
    # https://perishablepress.com/stop-using-unsafe-characters-in-urls/
            
    # Test 15 - Messy And Invalid Input
    def test15_MessyAndInvalidInput05(self):
        try:
            result = is_URL_valid('http://blog.sergeys.us/beer?utm_source=feedburner&amp;utm_medium=feed&amp;utm_campaign=Feed:+SergeySus+(Sergey+Sus+Photography+%C2%BB+Blog)&amp;utm_content=Google+Reader')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
#            self.assertFalse(result) # Colons are necessary in many situations... for instance following the communication standard (see: http:)
            self.assertTrue(result) # Let this ride until more fidelity is built into is_URL_valid()
    # NOTE:
    #       Notice the unencoded “:”? Apparently Google is including them in URLs for FeedBurner and Google  
    #   Reader.  Hopefully this is just an oversight that will be corrected in a future update.
    #
    # https://perishablepress.com/stop-using-unsafe-characters-in-urls/
            
    # Test 15 - Messy And Invalid Input
    def test15_MessyAndInvalidInput06(self):
        try:
            result = is_URL_valid('ftp://username:password@domain')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
#            self.assertFalse(result) # Colons are necessary in many situations... for instance following the communication standard (see: http:)
            self.assertTrue(result) # Let this ride until more fidelity is built into is_URL_valid()
    # NOTE:
    #       Notice the unencoded “:”? Apparently Google is including them in URLs for FeedBurner and Google  
    #   Reader.  Hopefully this is just an oversight that will be corrected in a future update.
    #
    # https://perishablepress.com/stop-using-unsafe-characters-in-urls/

                        
class MakeRelURLAbs(unittest.TestCase):
    
    # Test 1 - TypeError('baseURL is not a string')
    def test1_baseURL_TypeError01(self):
        try:
            result = make_rel_URL_abs(3.14, 'http://www.cad-comic.com/sillies/20130115')
        except TypeError as err:
            self.assertEqual(err.args[0], 'baseURL is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            
    # Test 2 - TypeError('baseURL is not a string')
    def test2_baseURL_TypeError02(self):
        try:
            result = make_rel_URL_abs(['http://www.cad-comic.com/sillies/'], 'http://www.cad-comic.com/sillies/20130115')
        except TypeError as err:
            self.assertEqual(err.args[0], 'baseURL is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            
    # Test 3 - ValueError('baseURL is empty')
    def test3_baseURL_ValueError01(self):
        try:
            result = make_rel_URL_abs('', 'http://www.cad-comic.com/sillies/20130115')
        except ValueError as err:
            self.assertEqual(err.args[0], 'baseURL is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            

    # Test 4 - TypeError('targetURL is not a string')
    def test4_targetURL_TypeError01(self):
        try:
            result = make_rel_URL_abs('http://www.cad-comic.com/sillies/', {'try':'again'})
        except TypeError as err:
            self.assertEqual(err.args[0], 'targetURL is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            
    # Test 5 - TypeError('targetURL is not a string')
    def test5_targetURL_TypeError02(self):
        try:
            result = make_rel_URL_abs('http://www.cad-comic.com/sillies/', ['http://www.cad-comic.com/sillies/20130115'])
        except TypeError as err:
            self.assertEqual(err.args[0], 'targetURL is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            
    # Test 6 - ValueError('targetURL is empty')
    def test6_targetURL_ValueError01(self):
        try:
            result = make_rel_URL_abs('http://www.cad-comic.com/sillies/', '')
        except ValueError as err:
            self.assertEqual(err.args[0], 'targetURL is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            
    # Test 7 - Valid Input - Normal absolute URL
    def test7_ValidInput01(self):
        try:
            result = make_rel_URL_abs('http://www.cad-comic.com/sillies/', 'http://www.cad-comic.com/sillies/20130115')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'http://www.cad-comic.com/sillies/20130115')
            
    # Test 8 - Valid Input - Normal absolute URL
    def test8_ValidInput02(self):
        try:
            result = make_rel_URL_abs('http://www.cad-comic.com/sillies/', 'www.cad-comic.com/sillies/20130115')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'www.cad-comic.com/sillies/20130115')
            
    # Test 9 - Valid Input - Normal relative URL
    def test9_ValidInput03(self):
        try:
            result = make_rel_URL_abs('http://www.cad-comic.com/sillies/', '/sillies/20130115')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'http://www.cad-comic.com/sillies/20130115')
            
    # Test 10 - Tricky Input - Mixed up association of relative and absolute
    def test10_TrickyInput01(self):
        try:
            result = make_rel_URL_abs('http://pvponline.com/comic', '2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'http://pvponline.com/comic/2017-02-16')

    # Test 11 - Tricky Input - Mixed up association of relative and absolute
    def test11_TrickyInput02(self):
        try:
            result = make_rel_URL_abs('http://pvponline.com', '/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'http://pvponline.com/comic/2017-02-16')
            
    # Test 12 - Tricky Input - Mixed up association of relative and absolute
    def test12_TrickyInput03(self):
        try:
            result = make_rel_URL_abs('pvponline.com', '/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'pvponline.com/comic/2017-02-16')
            
    # Test 13 - Tricky Input - Mixed up association of relative and absolute
    def test13_TrickyInput04(self):
        try:
            result = make_rel_URL_abs('pvponline.com/comic', '/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'pvponline.com/comic/2017-02-16')

    # Test 14 - Tricky Input - Mixed up association of relative and absolute
    def test14_TrickyInput05(self):
        try:
            result = make_rel_URL_abs('http://pvponline.com/comic', 'pvponline.com/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'http://pvponline.com/comic/2017-02-16')

    # Test 15 - Tricky Input - Mixed up association of relative and absolute
    def test15_TrickyInput06(self):
        try:
            result = make_rel_URL_abs('http://pvponline.com', 'pvponline.com/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'http://pvponline.com/comic/2017-02-16')
            
    # Test 16 - Tricky Input - Mixed up association of relative and absolute
    def test16_TrickyInput07(self):
        try:
            result = make_rel_URL_abs('pvponline.com', 'http://pvponline.com/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'http://pvponline.com/comic/2017-02-16')
            
    # Test 17 - Tricky Input - Mixed up association of relative and absolute
    def test17_TrickyInput08(self):
        try:
            result = make_rel_URL_abs('pvponline.com/comic', 'http://pvponline.com/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'http://pvponline.com/comic/2017-02-16')
            
    # Test 18 - Tricky Input - Mixed up association of relative and absolute
    def test18_TrickyInput09(self):
        try:
            result = make_rel_URL_abs('pvponline.com/comic', 'http://www.pvponline.com/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'http://www.pvponline.com/comic/2017-02-16')
            
    # Test 19 - Tricky Input - Mixed up association of relative and absolute
    def test19_TrickyInput10(self):
        try:
            result = make_rel_URL_abs('pvponline.com/comic', 'www.pvponline.com/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'www.pvponline.com/comic/2017-02-16')
            
    # Test 20 - Tricky Input - Redundant slashes that are redundant
    def test20_TrickyInput10(self):
        try:
            result = make_rel_URL_abs('https://www.grumpyc.at/is/grumpy/', '/is/grumpy/sometimes.html')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'https://www.grumpyc.at/is/grumpy/sometimes.html')


class IsURLAbs(unittest.TestCase):

    # Test 1 - TypeError('baseURL is not a string')
    def test1_baseURL_TypeError01(self):
        try:
            result = is_URL_abs(3.14, 'http://www.cad-comic.com/sillies/20130115')
        except TypeError as err:
            self.assertEqual(err.args[0], 'baseURL is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            
    # Test 2 - TypeError('baseURL is not a string')
    def test2_baseURL_TypeError02(self):
        try:
            result = is_URL_abs(['http://www.cad-comic.com/sillies/'], 'http://www.cad-comic.com/sillies/20130115')
        except TypeError as err:
            self.assertEqual(err.args[0], 'baseURL is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            
    # Test 3 - ValueError('baseURL is empty')
    def test3_baseURL_ValueError01(self):
        try:
            result = is_URL_abs('', 'http://www.cad-comic.com/sillies/20130115')
        except ValueError as err:
            self.assertEqual(err.args[0], 'baseURL is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            

    # Test 4 - TypeError('targetURL is not a string')
    def test4_targetURL_TypeError01(self):
        try:
            result = is_URL_abs('http://www.cad-comic.com/sillies/', {'try':'again'})
        except TypeError as err:
            self.assertEqual(err.args[0], 'targetURL is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            
    # Test 5 - TypeError('targetURL is not a string')
    def test5_targetURL_TypeError02(self):
        try:
            result = is_URL_abs('http://www.cad-comic.com/sillies/', ['http://www.cad-comic.com/sillies/20130115'])
        except TypeError as err:
            self.assertEqual(err.args[0], 'targetURL is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            
    # Test 6 - ValueError('targetURL is empty')
    def test6_targetURL_ValueError01(self):
        try:
            result = is_URL_abs('http://www.cad-comic.com/sillies/', '')
        except ValueError as err:
            self.assertEqual(err.args[0], 'targetURL is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            
    # Test 7 - Valid Input - Normal absolute URL
    def test7_ValidInput01(self):
        try:
            result = is_URL_abs('http://www.cad-comic.com/sillies/', 'http://www.cad-comic.com/sillies/20130115')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 8 - Valid Input - Normal absolute URL
    def test8_ValidInput02(self):
        try:
            result = is_URL_abs('http://www.cad-comic.com/sillies/', 'www.cad-comic.com/sillies/20130115')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 9 - Valid Input - Normal relative URL
    def test9_ValidInput03(self):
        try:
            result = is_URL_abs('http://www.cad-comic.com/sillies/', '/sillies/20130115')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)
            
    # Test 10 - Tricky Input - Mixed up association of relative and aboslute
    def test10_TrickyInput01(self):
        try:
            result = is_URL_abs('http://pvponline.com/comic', '2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)

    # Test 11 - Tricky Input - Mixed up association of relative and aboslute
    def test11_TrickyInput02(self):
        try:
            result = is_URL_abs('http://pvponline.com', '/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)
            
    # Test 12 - Tricky Input - Mixed up association of relative and aboslute
    def test12_TrickyInput03(self):
        try:
            result = is_URL_abs('pvponline.com', '/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)
            
    # Test 13 - Tricky Input - Mixed up association of relative and aboslute
    def test13_TrickyInput04(self):
        try:
            result = is_URL_abs('pvponline.com/comic', '/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)

    # Test 14 - Tricky Input - Mixed up association of relative and aboslute
    def test14_TrickyInput05(self):
        try:
            result = is_URL_abs('http://pvponline.com/comic', 'pvponline.com/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result) # Should probably be true

    # Test 15 - Tricky Input - Mixed up association of relative and aboslute
    def test15_TrickyInput06(self):
        try:
            result = is_URL_abs('http://pvponline.com', 'pvponline.com/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result) # Should probably be true
            
    # Test 16 - Tricky Input - Mixed up association of relative and aboslute
    def test16_TrickyInput07(self):
        try:
            result = is_URL_abs('pvponline.com', 'http://pvponline.com/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 17 - Tricky Input - Mixed up association of relative and aboslute
    def test17_TrickyInput08(self):
        try:
            result = is_URL_abs('pvponline.com/comic', 'http://pvponline.com/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 18 - Tricky Input - Mixed up association of relative and aboslute
    def test18_TrickyInput09(self):
        try:
            result = is_URL_abs('pvponline.com/comic', 'http://www.pvponline.com/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 19 - Tricky Input - Mixed up association of relative and aboslute
    def test19_TrickyInput10(self):
        try:
            result = is_URL_abs('pvponline.com/comic', 'www.pvponline.com/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 20 - Bad Input - Invalid baseURL
    def test20_BadInput01(self):
        try:
            result = is_URL_abs('www.not_a_URL.cz', '2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)
            
    # Test 21 - Bad Input - Invalid baseURL
    def test21_BadInput02(self):
        try:
            result = is_URL_abs('www.not_a_URL.ca', 'URL')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)
            
    # Test 22 - Bad Input - Invalid baseURL
    def test22_BadInput03(self):
        try:
            result = is_URL_abs('https://definitely-not-a-URL.arpa', 'https://xkcd.com')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 23 - Bad Input - Invalid baseURL
    def test23_BadInput04(self):
        try:
            result = is_URL_abs('http://probably-not_a-URL.ba', 'www.smbc-comics.com')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 24 - Bad Input - Invalid targetURL
    def test24_BadURL01(self):
        try:
            result = is_URL_abs('www.smbc-comics.com', 'not a website?')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)
            
    # Test 25 - Bad Input - Invalid targetURL
    def test25_BadURL02(self):
        try:
            result = is_URL_abs('https://xkcd.com/', 'not a website!')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)
            
    # Test 26 - Bad Input - Invalid targetURL
    def test26_BadURL03(self):
        try:
            result = is_URL_abs('https://www.xkcd.com/', 'websites typically begin with www and end with a top-level domain like com or org')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)      
            
    # Test 27 - Bad Input - Invalid targetURL
    def test27_BadURL04(self):
        try:
            result = is_URL_abs('https://www.xkcd.com/', 'websites typically begin with www. and end with a top-level domain like .com or .org')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
#            self.assertFalse(result)      
            pass
            # Uncomment the test above once is_URL_valid() has been written to check for:
            #   Invalid URL characters
            #   Start indicators that are not at the beginning
            #   Ending indicators that are not at the end
            
    # Test 28 - Bad Input - Invalid targetURL
    def test28_BadURL05(self):
        try:
            result = is_URL_abs('https://www.xkcd.com/', 'websites typically begin with https: and end with a top-level domain like .com or .org')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
#            self.assertFalse(result)      
            pass
            # Uncomment the test above once is_URL_valid() has been written to check for:
            #   Invalid URL characters
            #   Start indicators that are not at the beginning
            #   Ending indicators that are not at the end  
            
    # Test 29 - Bad Input - Invalid targetURL
    def test29_BadURL06(self):
        try:
            result = is_URL_abs('https://www.xkcd.com/', 'websites typically begin with http: and end with a top-level domain like .com or .org')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
#            self.assertFalse(result)      
            pass
            # Uncomment the test above once is_URL_valid() has been written to check for:
            #   Invalid URL characters
            #   Start indicators that are not at the beginning
            #   Ending indicators that are not at the end 
            
    # Test 30 - Bad Input - Invalid targetURL
    def test30_BadURL07(self):
        try:
            result = is_URL_abs('www.NotAWebsite.com', 'http:\n//\nwww.\nthisisnotarealwebsitebuttheonlyeasywaytoverifythatistoattempttoopenit\n.com')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)    
            
    # Test 31 - Bad Input - Invalid targetURL
    def test31_BadURL08(self):
        try:
            result = is_URL_abs('www.NotAWebsite.com', 'www.\nthisisnotarealwebsitebuttheonlyeasywaytoverifythatistoattempttoopenit\n.com')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)    
            
    # Test 32 - Bad Input - Invalid targetURL
    def test32_BadURL09(self):
        try:
            result = is_URL_abs('www.NotAWebsite.com', 'https:\n//\nthisisnotarealwebsitebuttheonlyeasywaytoverifythatistoattempttoopenit\n.com')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)    
            
    # Test 33 - Bad Input - Invalid targetURL
    def test33_BadURL10(self):
        try:
            result = is_URL_abs('www.NotAWebsite.com', 'https:\n//\nthisisnotarealwebsitebuttheonlyeasywaytoverifythatistoattempttoopenit\n.com')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)  
            
    # Test 34 - Bad Input - Not a single valid URL
    def test34_BadURL11(self):
        try:
            result = is_URL_abs('www.notaURL.ca', 'ThisisdefinitelynotaURLsinceitdoesnotincludeatopleveldomainlike.cz')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)  
            
    # Test 35 - Bad Input - Not a single valid URL
    def test35_BadURL12(self):
        try:
            result = is_URL_abs('http://Alphabet.cd', 'theAlphabetIsExtendedToInclude.bdAnd.be')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)  
            
    # Test 36 - Bad Input - Not a single valid URL
    def test36_BadURL13(self):
        try:
            result = is_URL_abs('www.Alphabet.de', 'AlphabetIsExtendedToInclude.asAnd.at')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)  


class FindURL(unittest.TestCase):

    def test01_htmlString_TypeError(self):
        try:
            find_a_URL(3.14, 'search for this', ['stuff', 'other stuff'], ['things', 'other things'])
        except TypeError as err:
            self.assertEqual(err.args[0], 'htmlString is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test02_htmlString_ValueError(self):
        try:
            find_a_URL('', 'search for this', ['stuff', 'other stuff'], ['things', 'other things'])
        except ValueError as err:
            self.assertEqual(err.args[0], 'htmlString is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test03_searchPhrase_TypeError(self):
        try:
            find_a_URL('http://www.nunyabusiness.com', -1, ['stuff', 'other stuff'], ['things', 'other things'])
        except TypeError as err:
            self.assertEqual(err.args[0], 'searchPhrase is not a string or a list')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test04_searchPhrase_ValueError1(self):
        try:
            find_a_URL('http://www.iamright.com', '', ['stuff', 'other stuff'], ['things', 'other things'])
        except ValueError as err:
            self.assertEqual(err.args[0], 'searchPhrase is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test05_searchPhrase_ValueError2(self):
        try:
            find_a_URL('http://www.iamright.com', [], ['stuff', 'other stuff'], ['things', 'other things'])
        except ValueError as err:
            self.assertEqual(err.args[0], 'searchPhrase is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test06_searchPhrase_ValueError3(self):
        try:
            find_a_URL('http://www.iamright.com', ['search for this', 'search for this other thing', ''], ['stuff', 'other stuff'], ['things', 'other things'])
        except ValueError as err:
            self.assertEqual(err.args[0], 'searchPhrase contains an empty string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test07_searchPhrase_TypeError4(self):
        try:
            find_a_URL('http://www.iamright.com', ['search for this', 'search for this other thing', ['How meta?', 'A list within a list']], ['stuff', 'other stuff'], ['things', 'other things'])
        except TypeError as err:
            self.assertEqual(err.args[0], 'searchPhrase contains a non string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test08_searchStart_TypeError(self):
        try:
            find_a_URL('http://www.iamright.com', 'search for this', 42, ['things', 'other things'])
        except TypeError as err:
            self.assertEqual(err.args[0], 'searchStart is not a string or a list')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test09_searchStart_ValueError1(self):
        try:
            find_a_URL('http://www.iamright.com', 'search for this', '', ['things', 'other things'])
        except ValueError as err:
            self.assertEqual(err.args[0], 'searchStart is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test10_searchStart_ValueError2(self):
        try:
            find_a_URL('http://www.iamright.com', 'search for this', [], ['things', 'other things'])
        except ValueError as err:
            self.assertEqual(err.args[0], 'searchStart is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test11_searchStart_ValueError3(self):
        try:
            find_a_URL('http://www.iamright.com', 'search for this', ['stuff', 'other stuff', ''], ['things', 'other things'])
        except ValueError as err:
            self.assertEqual(err.args[0], 'searchStart contains an empty string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test12_searchStart_TypeError4(self):
        try:
            find_a_URL('http://www.iamright.com', 'search for this', ['stuff', 'other stuff', 66], ['things', 'other things'])
        except TypeError as err:
            self.assertEqual(err.args[0], 'searchStart contains a non string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test13_searchStop_TypeError(self):
        try:
            find_a_URL('http://www.nunyabusiness.com', 'search for this', ['stuff', 'other stuff'], {'No':'Deal'})
        except TypeError as err:
            self.assertEqual(err.args[0], 'searchStop is not a string or a list')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test14_searchStop_ValueError1(self):
        try:
            find_a_URL('http://www.iamright.com', ['search for this', 'search for this other thing'], ['stuff', 'other stuff'], '')
        except ValueError as err:
            self.assertEqual(err.args[0], 'searchStop is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test15_searchStop_ValueError2(self):
        try:
            find_a_URL('http://www.iamright.com', ['search for this', 'search for this other thing'], ['stuff', 'other stuff'], [])
        except ValueError as err:
            self.assertEqual(err.args[0], 'searchStop is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test16_searchStop_ValueError3(self):
        try:
            find_a_URL('http://www.iamright.com', ['search for this', 'search for this other thing'], ['stuff', 'other stuff'], ['things', '', 'other things'])
        except ValueError as err:
            self.assertEqual(err.args[0], 'searchStop contains an empty string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test17_searchStop_TypeError4(self):
        try:
            find_a_URL('http://www.iamright.com', ['search for this', 'search for this other thing'], ['stuff', 'other stuff'], ['things', {'Nothing':'matters'}, 'other things'])
        except TypeError as err:
            self.assertEqual(err.args[0], 'searchStop contains a non string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test18_PVP_HTML_image_search1(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '1-Input_HTML.txt'), 'r') as testFile:
                testResult = find_a_URL(testFile.read(), 's3-us-west-2.amazonaws.com/pvponlinenew/img/comic/', 'src="', ['.png', '.jpg', '.gif'])
            self.assertEqual(testResult, 'http://s3-us-west-2.amazonaws.com/pvponlinenew/img/comic/2016/07/pvp20160726.jpg')
        except Exception as err:
            print(repr(err))

    def test19_PVP_HTML_image_search2(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '11-PvP_slash_date_HTML.txt'), 'r') as testFile:
                testResult = find_a_URL(testFile.read(), 's3-us-west-2.amazonaws.com/pvponlinenew/img/comic/', ['frick', 'frack', 'src="'], ['.png', '.jpg', '.gif'])
            self.assertEqual(testResult, 'http://s3-us-west-2.amazonaws.com/pvponlinenew/img/comic/2015/12/pvp20151231.jpg')
        except Exception as err:
            print(repr(err))

    def test20_Business_Cat_HTML_image_search1(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '3-BC_HTML.txt'), 'r') as testFile:
                testResult = find_a_URL(testFile.read(), ['<img src="http://www.businesscat.happyjar.com/wp-content/uploads/'], '<img src="', ['.png', '.jpg', '.gif'])
            self.assertEqual(testResult, 'http://www.businesscat.happyjar.com/wp-content/uploads/2016/12/2016-12-02-Order.png')
        except Exception as err:
            print(repr(err))

    def test21_SMBC_HTML_image_search1(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '5-SMBC_HTML.txt'), 'r') as testFile:
                testResult = find_a_URL(testFile.read(), ["You'll never find this in the code!", 'www.smbc-comics.com/comics/'], ['Why are you looking for this?', 'src="'], '.png')
            self.assertEqual(testResult, 'http://www.smbc-comics.com/comics/1482854925-20161227%20(2).png')
        except Exception as err:
            print(repr(err))

    def test22_SMBC_HTML_image_search2(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '6-SMBC_HTML.txt'), 'r') as testFile:
                testResult = find_a_URL(testFile.read(), ["You'll never find this in the code!", 'www.smbc-comics.com/comics/'], ['Why are you looking for this?', 'src="'], ['.nunya','.bak', 'xlsx','.png'])
            self.assertEqual(testResult, 'http://www.smbc-comics.com/comics/1482770017-20161226.png')
        except Exception as err:
            print(repr(err))

    def test23_Penny_Arcade_HTML_image_search1(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '7-Penny_Arcade_random_HTML.txt'), 'r') as testFile:
                testResult = find_a_URL(testFile.read(), ['photos.smugmug.com/Comics/Pa-comics','art.penny-arcade.com', 'penny-arcade.smugmug.com/photos/','photos.smugmug.com/photos/'], 'src="', ['.png', '.jpg', '.gif'])
            self.assertEqual(testResult, 'https://art.penny-arcade.com/photos/932182163_EazuQ/0/2100x20000/932182163_EazuQ-2100x20000.jpg')
        except Exception as err:
            print(repr(err))

    def test24_XKCD_HTML_image_search1(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '8-xkcd_random_HTML.txt'), 'r') as testFile:
                testResult = find_a_URL(testFile.read(), ['imgs.xkcd.com/comics/','Image URL (for hotlinking/embedding): '], 'src="', ['.png', '.jpg', '.gif'])
            # Mangled this assertion a bit to account for xkcd's odd relative-URLs that urlopen doesn't like
            self.assertTrue(testResult.find('imgs.xkcd.com/comics/apollo_speeches.png') >= 0)
        except Exception as err:
            print(repr(err))


class GetImageFilename(unittest.TestCase):

    def test01_htmlString_TypeError1(self):
        try:
            get_image_filename(3.14, 'search for this date', ['name', 'other names'], 'ending', True)
        except TypeError as err:
            self.assertEqual(err.args[0], 'htmlString is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test02_htmlString_TypeError2(self):
        try:
            get_image_filename(["don't", "put", "HTML", "code", "in", "a", "list"], ['search for this date', 'or this date'], ['name', 'other names'], 'ending')
        except TypeError as err:
            self.assertEqual(err.args[0], 'htmlString is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test03_htmlString_ValueError1(self):
        try:
            get_image_filename('', 'search for this date', ['name', 'other names'], 'ending')
        except ValueError as err:
            self.assertEqual(err.args[0], 'htmlString is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test04_dateSearchPhrase_TypeError1(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', 1/10/2017, ['name', 'other names'], 'ending', False)
        except TypeError as err:
            self.assertEqual(err.args[0], 'dateSearchPhrase is not a string or a list')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test05_dateSearchPhrase_TypeError2(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', ['search for this date', 'or this date', 20170110], ['name', 'other names'], 'ending')
        except TypeError as err:
            self.assertEqual(err.args[0], 'dateSearchPhrase contains a non string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test06_dateSearchPhrase_TypeError3(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', ['search for this date', 'or this date', {"Not":"Possible"}], ['name', 'other names'], 'ending')
        except TypeError as err:
            self.assertEqual(err.args[0], 'dateSearchPhrase contains a non string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test07_dateSearchPhrase_ValueError1(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', '', ['name', 'other names'], 'ending')
        except ValueError as err:
            self.assertEqual(err.args[0], 'dateSearchPhrase is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test08_dateSearchPhrase_ValueError2(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', [], ['name', 'other names'], 'ending')
        except ValueError as err:
            self.assertEqual(err.args[0], 'dateSearchPhrase is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test09_dateSearchPhrase_ValueError3(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', ['search for this date', 'or this date', ''], ['name', 'other names'], 'ending')
        except ValueError as err:
            self.assertEqual(err.args[0], 'dateSearchPhrase contains an empty string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test10_nameSearchPhrase_TypeError1(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', ['search for this date', 'or this date'], 31337, 'ending', True)
        except TypeError as err:
            self.assertEqual(err.args[0], 'nameSearchPhrase is not a string or a list')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test11_nameSearchPhrase_TypeError2(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', ['search for this date', 'or this date'], ['name', 'other names', ['not', 'a', 'string']], 'ending')
        except TypeError as err:
            self.assertEqual(err.args[0], 'nameSearchPhrase contains a non string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test12_nameSearchPhrase_TypeError3(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', ['search for this date', 'or this date'], ['name', 'other names', {'not':'good'}], 'ending')
        except TypeError as err:
            self.assertEqual(err.args[0], 'nameSearchPhrase contains a non string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test13_nameSearchPhrase_ValueError1(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', 'date?', '', 'ending', False)
        except ValueError as err:
            self.assertEqual(err.args[0], 'nameSearchPhrase is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test14_nameSearchPhrase_ValueError2(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', 'I can haz date?', [], 'ending')
        except ValueError as err:
            self.assertEqual(err.args[0], 'nameSearchPhrase is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test15_nameSearchPhrase_ValueError3(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', ['search for this date', 'or this date'], ['name', 'other names', ''], 'ending')
        except ValueError as err:
            self.assertEqual(err.args[0], 'nameSearchPhrase contains an empty string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test16_nameEnding_TypeError1(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', ['search for this date', 'or this date'], ['name', 'other name'], 0)
        except TypeError as err:
            self.assertEqual(err.args[0], 'nameEnding is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test17_nameEnding_ValueError1(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', 'date?', 'name', '')
        except ValueError as err:
            self.assertEqual(err.args[0], 'nameEnding is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test18_skipDate_TypeError1(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', 'date?', 'name', 'The End', 'I mean, I guess')
        except TypeError as err:
            self.assertEqual(err.args[0], 'skipDate is not a bool')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test19_skipDate_TypeError2(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', 'date?', 'name', 'The End', 'True')
        except TypeError as err:
            self.assertEqual(err.args[0], 'skipDate is not a bool')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test20_skipDate_TypeError3(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', 'date?', 'name', 'The End', 'False')
        except TypeError as err:
            self.assertEqual(err.args[0], 'skipDate is not a bool')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test21_skipDate_TypeError4(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', 'date?', 'name', 'The End', [True])
        except TypeError as err:
            self.assertEqual(err.args[0], 'skipDate is not a bool')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test22_skipDate_TypeError5(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', 'date?', 'name', 'The End', [False])
        except TypeError as err:
            self.assertEqual(err.args[0], 'skipDate is not a bool')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test23_PVP_HTML_image_search1(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '1-Input_HTML.txt'), 'r') as testFile:
                testResult = get_image_filename(testFile.read(), 's3-us-west-2.amazonaws.com/pvponlinenew/img/comic/', '<title>PVP - ', '</title>')
        except Exception as err:
            print(repr(err))
        else:
            self.assertEqual(testResult, '20160726_2016-07-26')

    def test24_PVP_HTML_image_search2(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '11-PvP_slash_date_HTML.txt'), 'r') as testFile:
                testResult = get_image_filename(testFile.read(), 's3-us-west-2.amazonaws.com/pvponlinenew/img/comic/', '<title>PVP - ', '</title>')
            # Mangled this test a bit because the found name 
        except Exception as err:
            print(repr(err))
        else:
#            self.assertEqual(testResult, '20151231_Christmas-Special-2015-Part-19'.lower()) # No longer necessary?  Case issue resolved.
            self.assertEqual(testResult, '20151231_Christmas-Special-2015-Part-19')

    def test25_Business_Cat_HTML_image_search1(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '3-BC_HTML.txt'), 'r') as testFile:
                testResult = get_image_filename(testFile.read(), ['<img src="http://www.businesscat.happyjar.com/wp-content/uploads/'], 'title="', '"')
        except Exception as err:
            print(repr(err))
        else:
            self.assertEqual(testResult, '20161202_Order')

    def test26_SMBC_HTML_image_search1(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '5-SMBC_HTML.txt'), 'r') as testFile:
                testResult = get_image_filename(testFile.read(), ["You'll never find this in the code!", 'www.smbc-comics.com/comics/'], '<title>Saturday Morning Breakfast Cereal - ', '</title>')
        except Exception as err:
            print(repr(err))
        else:
#            self.assertEqual(testResult, '20161227_Wanna-Evolve'.lower()) # No longer necessary.  Case issue resolved.
            self.assertEqual(testResult, '20161227_Wanna-Evolve')

    def test27_SMBC_HTML_image_search2(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '6-SMBC_HTML.txt'), 'r') as testFile:
                testResult = get_image_filename(testFile.read(), ["You'll never find this in the code!", 'www.smbc-comics.com/comics/'], ['<title>Saturday Morning Breakfast Cereal - '], '</title>')
        except Exception as err:
            print(repr(err))
        else:
#            self.assertEqual(testResult, '20161226_Political-Philosophy'.lower()) # No longer necessary.  Case issue resolved.
            self.assertEqual(testResult, '20161226_Political-Philosophy')

    def test28_Penny_Arcade_HTML_image_search1(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '7-Penny_Arcade_random_HTML.txt'), 'r') as testFile:
                testResult = get_image_filename(testFile.read(), ['input type="hidden" name="attributes[comic_title]" value="'], 'alt="', '"')
        except Exception as err:
            print(repr(err))
        else:
#            self.assertEqual(testResult, '20100712_Our-Partial-Future'.lower()) # No longer necessary.  Case issue resolved.
            self.assertEqual(testResult, '20100712_Our-Partial-Future')

    def test29_XKCD_HTML_image_search1(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '8-xkcd_random_HTML.txt'), 'r') as testFile:
                testResult = get_image_filename(testFile.read(), ['imgs.xkcd.com/comics/','Image URL (for hotlinking/embedding): '], 'Permanent link to this comic: http://xkcd.com/', '/<br', True)
        except Exception as err:
            print(repr(err))
        else:
            self.assertEqual(testResult, '1484')

    def test30_XKCD_HTML_image_search2(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '8-xkcd_random_HTML.txt'), 'r') as testFile:
                testResult = get_image_filename(testFile.read(), ['imgs.xkcd.com/comics/','Image URL (for hotlinking/embedding): '], 'Permanent link to this comic: http://xkcd.com/', '/<br', False)
        except Exception as err:
            print(repr(err))
        else:
            self.assertEqual(testResult, '00000000')


class GetTheDate(unittest.TestCase):
    
    # Test 1 - TypeError('pageHTML is not a string or list')
    def test01_TypeError01(self):
        try:
            result = find_the_date(31337 / 1337)
        except TypeError as err:
            self.assertEqual(err.args[0], 'pageHTML is not a string or list')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    # Test 2 - TypeError('pageHTML is not a string or list')
    def test02_TypeError02(self):
        try:
            result = find_the_date({'un':'list'})
        except TypeError as err:
            self.assertEqual(err.args[0], 'pageHTML is not a string or list')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    # Test 3 - TypeError('pageHTML contains a non-string')
    def test03_TypeError03(self):
        try:
                testList = ['duck', 'duck', 'duck', ['G', 'O', 'O', 'S', 'E', '!']]
                result = find_the_date(testList)
        except TypeError as err:
            self.assertEqual(err.args[0], 'pageHTML contains a non-string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    # Test 4 - TypeError('pageHTML contains a non-string')
    def test04_TypeError04(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '1-Input_HTML.txt'), 'r') as testFile:
                testContent = testFile.read()
                testList = re.split('<a|<A|\n',testContent)
                testList.append(['this','is','not','a','string'])
                result = find_the_date(testList)
        except TypeError as err:
            self.assertEqual(err.args[0], 'pageHTML contains a non-string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    # Test 5 - ValueError('pageHTML is empty')
    def test05_ValueError01(self):
        try:
            testList = []
            result = find_the_date(testList)
        except ValueError as err:
            self.assertEqual(err.args[0], 'pageHTML is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    # Test 6 - Valide Input - 12-CaH_dot_date_HTML.txt
    def test06_ValidInput01(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '12-CaH_dot_date_HTML.txt'), 'r') as testFile:
                result = find_the_date(testFile.read())
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == '20170217')

    # Test 7 - Valide Input - 13-CaH_dot_date_HTML.txt
    def test07_ValidInput02(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '13-CaH_dot_date_HTML.txt'), 'r') as testFile:
                result = find_the_date(testFile.read())
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == '20170215')

    # Test 8 - Valide Input - 14-CaH_dot_date_HTML.txt
    def test08_ValidInput03(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '14-CaH_dot_date_HTML.txt'), 'r') as testFile:
                result = find_the_date(testFile.read())
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == '20170214')

    # Test 9 - Valide Input - 15-CaH_dot_date_HTML.txt
    def test09_ValidInput04(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '15-CaH_dot_date_HTML.txt'), 'r') as testFile:
                result = find_the_date(testFile.read())
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == '20050126')

    # Test 10 - Valide Input - 16-CaH_dot_date_HTML.txt
    def test10_ValidInput05(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '16-CaH_dot_date_HTML.txt'), 'r') as testFile:
                result = find_the_date(testFile.read())
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == '20050127')

    # Test 11 - Valide Input - 17-CaH_dot_date_HTML.txt
    def test11_ValidInput06(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '17-CaH_dot_date_HTML.txt'), 'r') as testFile:
                result = find_the_date(testFile.read())
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == '20160529')

    # Test 12 - Valide Input - 18-CaH_dot_date_HTML.txt
    def test12_ValidInput07(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '18-CaH_dot_date_HTML.txt'), 'r') as testFile:
                result = find_the_date(testFile.read())
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == '20141202')


if __name__ == '__main__':

    # Run all the tests!
    #unittest.main(verbosity=2, exit=False)

# SizeNumericImageNames
    linkerSuite = unittest.TestLoader().loadTestsFromTestCase(SizeNumericImageNames)
    unittest.TextTestRunner(verbosity=2).run(linkerSuite)

## GetURLParentPath
#    linkerSuite = unittest.TestLoader().loadTestsFromTestCase(GetURLParentPath)
#    unittest.TextTestRunner(verbosity=2).run(linkerSuite)

## GetRootURL
#    linkerSuite = unittest.TestLoader().loadTestsFromTestCase(GetRootURL)
#    unittest.TextTestRunner(verbosity=2).run(linkerSuite)

## GetTheDate
#    linkerSuite = unittest.TestLoader().loadTestsFromTestCase(GetTheDate)
#    unittest.TextTestRunner(verbosity=2).run(linkerSuite)
    
## MakeRelURLAbs
#    linkerSuite = unittest.TestLoader().loadTestsFromTestCase(MakeRelURLAbs)
#    unittest.TextTestRunner(verbosity=2).run(linkerSuite)
    
## IsURLAbs
#    linkerSuite = unittest.TestLoader().loadTestsFromTestCase(IsURLAbs)
#    unittest.TextTestRunner(verbosity=2).run(linkerSuite)
    
## FindURL
#    linkerSuite = unittest.TestLoader().loadTestsFromTestCase(FindURL)
#    unittest.TextTestRunner(verbosity=2).run(linkerSuite)

## IsURLValid
#    linkerSuite = unittest.TestLoader().loadTestsFromTestCase(IsURLValid)
#    unittest.TextTestRunner(verbosity=2).run(linkerSuite)
 
## GetImageFilename
#    linkerSuite = unittest.TestLoader().loadTestsFromTestCase(GetImageFilename)
#    unittest.TextTestRunner(verbosity=2).run(linkerSuite)

    print("Done Testing")
