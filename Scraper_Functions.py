#################################################################################
################################### HARKLEBOT ###################################
############################## Scraper Functions v1 #############################
##################### https://github.com/hark130/Harklebot ######################
#################################################################################
# Version 1
#   This module contains the necessary functions for Harklebot scrapers to work
#################################################################################
#################################################################################
# Version 1.2
#   ADDING: Extricated imageURL --> filename conversion into a function named
#               find_a_URL(htmlString, [searchPhrase], [searchStart], [searchEnd])
#               get_image_filename(htmlString, [dateSearchPhrase], [nameSearchPhrase], nameEnding, skipDate=False)
#   ADDING: New functionality to fix Ctrl-Alt-Del 'first' relative URL problem
#           make_rel_URL_abs(baseURL, targetURL)
#           is_URL_abs(baseURL, targetURL)
#   MOVING: URL functions from Robot Reader to Scraper Functions
#   ADDING: New functionality to find_the_date() to include YYYY.MM.DD (see: Cyanide & Happiness)
#           is_URL_valid()... basic functionality
#   ADDING: get_URL_parent_path(URL)
#################################################################################
#################################################################################
# Version 1.3
#   ADDING: Image name sizing capability for 'counted' names (see: Cyanide & Happines, XKCD)
#################################################################################


import os
import time
import re
#import htmlentitydefs
import collections
from urllib.parse import urlparse
from urllib.parse import urlunparse


'''
    Purpose: Determine the parent path of a URL
    Input:
        URL - string representation of a URL
    Output:
        String representation of the parent path URL on success
        https://github.com/hark130/Harklebot becomes
        https://github.com/hark130
    Exceptions:
        TypeError('URL is not a string')
        ValueError('URL is empty')
        ValueError('URL is not a URL')
'''
def get_URL_parent_path(URL):
    retVal = ''
    
    # 1. INPUT VALIDATION
    if isinstance(URL, str) is False:
        raise TypeError('URL is not a string')
    elif URL.__len__() == 0:
        raise ValueError('URL is empty')
    elif is_URL_valid(URL) is False:
        raise ValueError('URL is not a URL')
            
    # 2. MODIFY URL
    ## 2.1. Parse the URL
    originalList = list(urlparse(URL))
    
    ## 2.2. Extract the parsed path
    rawPath = originalList[2]
    
    ## 2.3. Split the parse path
    rawPathList = rawPath.split('/')

    if rawPathList.__len__() > 1:    
        ## 2.4. Slice of the end
        rawPathList = rawPathList[:rawPathList.__len__() - 1:]
    
        ## 2.5. Reassemble the path
        originalList[2] = '/'.join(rawPathList)

        ## 2.6. Drop parameters, queries, and fragments
        originalList[3] = ''
        originalList[4] = ''
        originalList[5] = ''
    
        ## 2.7. Reassemble the URL with the modified path
        retVal = urlunparse(originalList)
    else:
        retVal = URL

    return retVal


'''
    Purpose: Determine if a URL is valid or not
    Input:
        URL - string representation of a URL
    Output:
        True - URL is valid
        False - URL is invalid
    Exceptions:
        TypeError('URL is not a string')
        ValueError('URL is empty')
    NOTES:
        This function is not nearly complicated enough to be right.
        All this function does is check for any characters that aren't allowed.
        This function does not verify those characters are being utilized properly.
            Example1: ftp://username:password@domain (the colon (:) should be coded out)
            Example2: http://test.site/wp-admin/post.php?t=1347548645469? (Apparently, trailing question marks are bad)
        As it stands, this function delivers enough value to be left alone for the time being
'''
def is_URL_valid(URL):
    retVal = True
    
    # 1. INPUT VALIDATION
    ## 1.1. Verify URL is a string
    if isinstance(URL, str) is False:
        raise TypeError('URL is not a string')
    ## 1.2. Verify URL is not empty
    elif URL.__len__() == 0:
        raise ValueError('URL is empty')
        
    # 2. CHECK URL FOR VALIDITY
    ########### Vaporware says, "What?" ###########
#    print("\nWhat?  Not checking:\t{}".format(URL)) # DEBUGGING
    ########### EXECUTE REGEX SEPPUKU HERE ###########
    # %[0-9a-fA-F]{2} --> matches on HTML codes
    # [a-zA-Z0-9] --> matches on letters and numbers in an appropriate way
    # ^ matches counter examples
    # Original starting point...
    # re.compile(r"(/^([!#$&-;=?-[]_a-z~]|%[0-9a-fA-F]{2})+&/)")
    ### This gets close but hits on 'Hello%29world=Fun' and it shouldn't
    # re.compile(r"(^[a-zA-Z0-9]|%[^0-9a-fA-F]{2})")
    # if it's None:
    #   print("Invalid entries")
    # else:
    #   print("No invalid entries")
    ### This also gets close but fails on HTML codes
    # re.compile(r"[^A-Za-z0-9-._~:/?#[]@!$&'()*+,;=`]")

# Removing brackets because of Microsoft, of all reasons
#    badChars = re.compile(r"[^A-Za-z0-9-._%~:/?#[\]@!$&'()*+,;=`]")
    badChars = re.compile(r"[^A-Za-z0-9-._%~:/?#[\]@!$&'()*+,;=`]")

    for result in badChars.findall(URL):
#        print(result) # DEBUGGING
        retVal = False
    
    return retVal


'''
    Purpose: Determine if a URL represents an absolute path
    Input:
        baseURL - string representation of the domain name portion of a site
        targetURL - string representation of a URL associated with baseURL
    Output:
        True - targetURL is absolute
        False - targetURL is a relative URL associated with baseURL
    Exceptions:
        TypeError('baseURL is not a string')
        TypeError('targetURL is not a string')
        ValueError('baseURL is empty')
        ValueError('targetURL is empty')   
'''
def is_URL_abs(baseURL, targetURL):
    retVal = False

    # 1. INPUT VALIDATION
    ## 1.1. baseURL
    if isinstance(baseURL, str) is False:
        raise TypeError('baseURL is not a string')
    elif baseURL.__len__() == 0:
        raise ValueError('baseURL is empty')
        
    ## 1.2. targetURL
    if isinstance(targetURL, str) is False:
        raise TypeError('targetURL is not a string')
    elif targetURL.__len__() == 0:
        raise ValueError('targetURL is empty')    
        
    # 2. BUILD INDICATOR LIST
    fullURLIndicatorList = [baseURL, '//', ':', 'www.', 'http:', 'https:']
#    fullURLIndicatorList = fullURLIndicatorList.append(get_root_URL(baseURL)) # BROKEN
    fullURLIndicatorList.append(get_root_URL(baseURL))
    
    # 3. BUILD TOP-LEVEL DOMAIN (TLD) LIST
    # https://en.wikipedia.org/wiki/List_of_Internet_top-level_domains
    tldList = [
        # Generic top-level domains
        '.com', '.org', '.net', '.int', 'edu', '.gov', '.mil', '.arpa', 
        # Country code top-level domains
        '.ac', '.ad', '.ae', '.af', '.ag', '.ai', '.al', '.am', '.an', 
        '.ao', '.aq', '.ar', '.as', '.at', '.au', '.aw', '.ax', '.az', 
        '.ba', '.bb', '.bd', '.be', '.bf', '.bg', '.bh', '.bi', '.bj', 
        '.bl', '.bm', '.bn', '.bo', '.bq', '.br', '.bs', '.bt', '.bv', 
        '.bw', '.by', '.bz', '.ca', '.cc', '.cd', '.cf', '.cg', '.ch', 
        '.ci', '.ck', '.cl', '.cm', '.cn', '.co', '.cr', '.cu', '.cv', 
        '.cw', '.cx', '.cy', '.cz', '.de', '.dj', '.dk', '.dm', '.do', 
        '.dz', '.ec', '.ee', '.eg', '.eh', '.er', '.es', '.et', '.eu', 
        '.fi', '.fj', '.fk', '.fm', '.fo', '.fr', '.ga', '.gb', '.gd', 
        '.ge', '.gf', '.gg', '.gh', '.gi', '.gl', '.gm', '.gn', '.gb', 
        '.gd', '.ge', '.gf', '.gg', '.gh', '.gi', '.gl', '.gm', '.gn', 
        '.gp', '.gq', '.gr', '.gs', '.gt', '.gu', '.gw', '.gy', '.hk', 
        '.hm', '.hn', '.hr', '.ht', '.hu', '.id', '.ie', '.il', '.im', 
        '.in', '.io', '.iq', '.ir', '.is', '.it', '.je', '.jm', '.jo', 
        '.jp', '.ke', '.kg', '.kh', '.ki', '.km', '.kn', '.kp', '.kr', 
        '.kw', '.ky', '.kz', '.la', '.lb', '.lc', '.li', '.lk', '.lr', 
        '.ls', '.lt', '.lu', '.lv', '.ly', '.ma', '.mc', '.md', '.me', 
        '.mf', '.mg', '.mh', '.mk', '.ml', '.mm', '.mn', '.mo', '.mp', 
        '.mq', '.mr', '.ms', '.mt', '.mu', '.mv', '.mw', '.mx', '.my', 
        '.mz', '.na', '.nc', '.ne', '.nf', '.ng', '.ni', '.nl', '.no', 
        '.np', '.nr', '.nu', '.nz', '.om', '.pa', '.pe', '.pf', '.pg', 
        '.ph', '.pk', '.pl', '.pm', '.pn', '.pr', '.ps', '.pt', '.pw', 
        '.py', '.qa', '.re', '.ro', '.rs', '.ru', '.rw', '.sa', '.sb', 
        '.sc', '.sd', '.se', '.sg', '.sh', '.si', '.sj', '.sk', '.sl', 
        '.sm', '.sn', '.so', '.sr', '.ss', '.st', '.su', '.sv', '.sx', 
        '.sy', '.sz', '.tc', '.td', '.tf', '.tg', '.th', '.tj', '.tk', 
        '.tl', '.tm', '.tn', '.to', '.tp', '.tr', '.tt', '.tv', '.tw', 
        '.tz', '.ua', '.ug', '.uk', '.um', '.us', '.uy', '.uz', '.va', 
        '.vc', '.ve', '.vg', '.vi', '.vn', '.vu', '.wf', '.ws', '.ye', 
        '.yt', '.za', '.zm', '.zw'	
    ]
    
    # 4. TEST targetURL
    for indicator in fullURLIndicatorList:
        if retVal == True:
            break # Found a match.  Stop looking.
        if targetURL.find(indicator) >= 0:
            for tld in tldList:
                if indicator.find(tld) > 0: # If the indicator contains a tld...
                    retVal = True
                    break # Found a match.  Stop looking.
                if targetURL.find(tld) >= targetURL.find(indicator): # If the URL's tld comes after the indicator
                    retVal = True
                    break # Found a match.  Stop looking.
    
    return retVal


'''
    Purpose: Return the absolute URL of targetURL given the baseURL
    Input:
        baseURL - string representation of the domain name portion of a site
        targetURL - string representation of a URL associated with baseURL
    Output:
        A string which contains the absolute version of targetURL
    Exceptions:
        TypeError('baseURL is not a string')
        TypeError('targetURL is not a string')
        ValueError('baseURL is empty')
        ValueError('targetURL is empty')    
    NOTE:
        targetURL may be absolute or relative
        baseURL may be different than the "root" URL see:
            http://www.cad-comic.com/sillies/ *vs* http://www.cad-comic.com
'''
def make_rel_URL_abs(baseURL, targetURL):
    retVal = ''
    absTargetURLPathList = []
    foundOverlap = False
    
    # 1. INPUT VALIDATION
    ## 1.1. baseURL
    if isinstance(baseURL, str) is False:
        raise TypeError('baseURL is not a string')
    elif baseURL.__len__() == 0:
        raise ValueError('baseURL is empty')
        
    ## 1.2. targetURL
    if isinstance(targetURL, str) is False:
        raise TypeError('targetURL is not a string')
    elif targetURL.__len__() == 0:
        raise ValueError('targetURL is empty')    

    # 2. TEST targetURL
    ## 2.1. Is targetURL already absolute?
    try:
        result = is_URL_abs(baseURL, targetURL)
    except Exception as err:
        raise(err)
    else:
        if result is True: # targetURL is already an absolute URL
            retVal = targetURL
            
    ## 2.2. Is there overlap between baseURL and targetURL
        else:
            ### 2.2.1. Split the baseURL into a list of paths
            baseURLPathList = baseURL.split('/')
            
            ### 2.2.2. Strip the targetURL of any leading slashes
            tempTargetURL = targetURL
            
            while tempTargetURL.find('/') == 0:
                tempTargetURL = tempTargetURL[1:]
            
            ### 2.2.3. Split the targetURL into a list of paths
            targetURLPathList = tempTargetURL.split('/')
            
            ### 2.2.4. Look for overlap while building absolute target URL
            for basePath in baseURLPathList:
                if basePath == targetURLPathList[0]: # Found an overlap
                    foundOverlap = True
                    for targetPath in targetURLPathList: # Copy the overlap
#                        absTargetURLPathList = absTargetURLPathList.append(targetPath) # BROKEN
                        absTargetURLPathList.append(targetPath)

                    break # Done copying
                else: # No overlap
#                    absTargetURLPathList = absTargetURLPathList.append(basePath) # BROKEN
                    absTargetURLPathList.append(basePath)

            ### 2.2.5. Append in targetPath if there was no overlap
            if foundOverlap is False:
                for targetPath in targetURLPathList:
                    absTargetURLPathList.append(targetPath)
                    
            ### 2.2.6. Rebuild the absolute URL
            retVal = '/'.join(absTargetURLPathList)

            ### 2.2.7. Trim the URL
            retVal = trim_a_URL(retVal)
        
    return retVal


'''
    Purpose: Determine a portion of an image URL's eventual filename buried in a string of raw HTML given search criteria
    Input:
        htmlString - a string of raw HTML code (not a list)
        dateSearchPhrase - a string or list of strings that indicate we've found an HTML line that contains the date
        nameSearchPhrase - a string or list of strings that indicate we've found an HTML line that contains the name
        nameEnding - a string that delimits the end of the name (usually '"')
        skipDate - boolean that allows the function to ignore the lack of a date
    Output: 
        A string representing one of the following on success
            'YYYYMMDD-<name>'   # Date and name found
            'YYYYMMDD'          # No name found
            '00000000'          # If skipDate is False and no date was found, regardless of if a name was found or not
            '<name>'            # If skipDate is True and no date was found but a name was found
    Exceptions:
            TypeError('htmlString is not a string')
            TypeError('dateSearchPhrase is not a string or a list')
            TypeError('dateSearchPhrase contains a non string')
            TypeError('nameSearchPhrase is not a string or a list')
            TypeError('nameSearchPhrase contains a non string')
            TypeError('nameEnding is not a string')
            ValueError('htmlString is empty')
            ValueError('dateSearchPhrase is empty')
            ValueError('dateSearchPhrase contains an empty string')
            ValueError('nameSearchPhrase is empty')
            ValueError('nameSearchPhrase contains an empty string')
            ValueError('nameEnding is empty')
    NOTE:
        This functions return value does not constitute a stand-alone filename.
            It will not include a file extension or an appropriate prepended phrase.
'''
def get_image_filename(htmlString, dateSearchPhrase, nameSearchPhrase, nameEnding, skipDate=False):
    
    retVal = '00000000'
    dateSearchList = [] # Will contain all the date phrases to search for
    nameSearchList = [] # Will contain all the name phrases to search for
    imageDate = ''
    imageName = ''

    # 1. INPUT VALIDATION
    ## 1.1. htmlString
    if isinstance(htmlString, str) is False:
        raise TypeError('htmlString is not a string')
    elif htmlString.__len__() == 0:
        raise ValueError('htmlString is empty')

    ## 1.2. dateSearchPhrase
    if isinstance(dateSearchPhrase, list) is False:
        if isinstance(dateSearchPhrase, str) is False:
            raise TypeError('dateSearchPhrase is not a string or a list')
        else:
            if dateSearchPhrase.__len__() == 0:
                raise ValueError('dateSearchPhrase is empty')
            else:
                dateSearchList = [dateSearchPhrase.lower()]
    else:
        for entry in dateSearchPhrase:
            if isinstance(entry, str) is False:
                raise TypeError('dateSearchPhrase contains a non string')
            elif entry.__len__() == 0:
                raise ValueError('dateSearchPhrase contains an empty string')
            else:
                dateSearchList.append(entry.lower())

    if dateSearchList.__len__() == 0:
        raise ValueError('dateSearchPhrase is empty')

    ## 1.3. nameSearchPhrase
    if isinstance(nameSearchPhrase, list) is False:
        if isinstance(nameSearchPhrase, str) is False:
            raise TypeError('nameSearchPhrase is not a string or a list')
        else:
            if nameSearchPhrase.__len__() == 0:
                raise ValueError('nameSearchPhrase is empty')
            else:
                nameSearchList = [nameSearchPhrase.lower()]
    else:
        for entry in nameSearchPhrase:
            if isinstance(entry, str) is False:
                raise TypeError('nameSearchPhrase contains a non string')
            elif entry.__len__() == 0:
                raise ValueError('nameSearchPhrase contains an empty string')
            else:
                nameSearchList.append(entry.lower())

    if nameSearchList.__len__() == 0:
        raise ValueError('nameSearchPhrase is empty')

    ## 1.4. nameEnding
    if isinstance(nameEnding, str) is False:
        raise TypeError('nameEnding is not a string')
    elif nameEnding.__len__() == 0:
        raise ValueError('nameEnding is empty')

    ## 1.5. skipDate
    if isinstance(skipDate, bool) is False:
        raise TypeError('skipDate is not a bool')

    # 2. SPLIT THE HTML
    htmlList = re.split('\n|</a>|</div>', htmlString.lower())

    # 3. GO DATE SEARCHING
    for entry in htmlList:
        if imageDate.__len__() == 8 and imageDate != '00000000':
            break # Found a date.  Stop looking.
        for phrase in dateSearchList:
            if entry.find(phrase) >= 0:
                imageDate = find_the_date(entry)
                # Test the result of find_the_date()
                if imageDate == '00000000':
                    imageDate = ''
                    continue
                elif imageDate.__len__() == 8:
                    htmlList.insert(0, entry) # Put the 'date' hit at the front of the list for 'name' searching
                    break # Found a date.  Stop looking.

    # 4. GO NAME SEARCHING
    if (imageDate.__len__() == 8 and imageDate != '00000000') or skipDate is True:
        for entry in htmlList:
            if imageName.__len__() > 0:
                break # Found a name.  Stop looking.
            for phrase in nameSearchList:
                if entry.find(phrase) >= 0:
                    # 4.1. Slice the entry
                    imageName = entry[entry.find(phrase) + phrase.__len__():]
                    imageName = imageName[:imageName.find(nameEnding)]

                    # 4.2. Trim unwanted characters
#                    imageName = trim_the_name(imageName) # Save this until *AFTER* finding the original case-sensitive entry
                    
                    # 4.3. Verify work
                    if imageName.__len__() > 0:
                        break # Found a name.  Stop looking.

        ## 5. PUT IT ALL TOGETHER
        #retVal = imageDate

        #if imageName.__len__() > 0:
        #    retVal = retVal + '_' + imageName    

        # 5. Return original case-sensitive entry
        ## 5.1. Find original case-sensitive entry
        if imageName.__len__() > 0:
            temp = htmlString[htmlString.lower().find(imageName):]
            temp = temp[:imageName.__len__()]
            imageName = temp
            # 5.2. Trim unwanted characters
            imageName = trim_the_name(imageName)
            
        ## 5.2. Put it all together
        ### 5.2.1. Image date Found
        if imageDate.__len__() == 8 and imageDate != '00000000':
            retVal = imageDate
            ### 5.2.1. ...and image name found
            if imageName.__len__() > 0:
                retVal = retVal + '_' + imageName    
        ### 5.2.2 Image date NOT found
        elif skipDate is True and imageName.__len__() > 0:
            ### 5.2.2. ...and image name found
            retVal = imageName



    return retVal


'''
    Purpose: Find a URL buried in a string of raw HTML given search criteria
    Input:
        htmlString - a string of raw HTML code (not a list)
        searchPhrase - a string or list of strings that indicate we've found the right HTML line
        searchStart - either a string or list of strings to begin searching with
        searchStop - either a string or list of strings to end the search
    Output: 
        A string representing the given URL on success
        An empty string if:
            No occurrences of searchStart were found
            searchStart and searchStop were sequential in the string
    Exceptions:
            TypeError('htmlString is not a string')
            TypeError('searchPhrase is not a string or a list')
            TypeError('searchPhrase contains a non string')
            TypeError('<searchVar> is not a string or a list')
            TypeError('<searchVar> is not a string or a list')
            TypeError('<searchVar> contains a non string')
            ValueError('htmlString is empty')
            ValueError('searchStart is empty')
            ValueError('searchStart contains an empty string')
            ValueError('<searchVar> is empty')
            ValueError('<searchVar> contains an empty string')
    NOTE:
        This is a bookend search.  This function call:
            find_a_URL('garbagegarbagegarbage<searchStart>needle<searchStop>garbagegarbagegarbage', 'garbagegarbage<searchStart>', <searchStart>, <searchStop>)
            ...will return 'needle<searchStop>'
'''
def find_a_URL(htmlString, searchPhrase, searchStart, searchStop):
    
    retVal = ''
    searchList = [] # Will contain all the phrases to search for
    startList = [] # Will contain all the start delimiters
    stopList = [] # Will contain all the stop delimiters

    # 1. INPUT VALIDATION
    ## 1.1. htmlString
    if isinstance(htmlString, str) is False:
        raise TypeError('htmlString is not a string')
    elif htmlString.__len__() == 0:
        raise ValueError('htmlString is empty')

    ## 1.2. searchPhrase
    if isinstance(searchPhrase, list) is False:
        if isinstance(searchPhrase, str) is False:
            raise TypeError('searchPhrase is not a string or a list')
        else:
            searchList = [searchPhrase.lower()]
    else:
        for entry in searchPhrase:
            if isinstance(entry, str) is False:
                raise TypeError('searchPhrase contains a non string')
            elif entry.__len__() == 0:
                raise ValueError('searchPhrase contains an empty string')
            else:
                searchList.append(entry.lower())

    if searchList.__len__() == 0:
        raise ValueError('searchPhrase is empty')

    ## 1.3. searchStart
    if isinstance(searchStart, list) is False:
        if isinstance(searchStart, str) is False:
            raise TypeError('searchStart is not a string or a list')
        else:
            startList = [searchStart.lower()]
    else:
        for entry in searchStart:
            if isinstance(entry, str) is False:
                raise TypeError('searchStart contains a non string')
            elif entry.__len__() == 0:
                raise ValueError('searchStart contains an empty string')
            else:
                startList.append(entry.lower())

    if startList.__len__() == 0:
        raise ValueError('searchStart is empty')

    ## 1.4. searchStop
    if isinstance(searchStop, list) is False:
        if isinstance(searchStop, str) is False:
            raise TypeError('searchStop is not a string or a list')
        else:
            stopList = [searchStop.lower()]
    else:
        for entry in searchStop:
            if isinstance(entry, str) is False:
                raise TypeError('searchStop contains a non string')
            elif entry.__len__() == 0:
                raise ValueError('searchStop contains an empty string')
            else:
                stopList.append(entry.lower())

    if stopList.__len__() == 0:
        raise ValueError('searchStop is empty')

    # 2. SPLIT THE HTML
    htmlList = re.split('\n|</a>|</div>', htmlString.lower())

    # 3. GO SEARCHING
    for entry in htmlList:
        if retVal.__len__() > 0:
            break # It's been found
        for phrase in searchList:
            if entry.find(phrase) >= 0:
                ## This may be it
                # 3.1. Find the beginning
                for start in startList:
                    if entry.find(start) >= 0:
                        retVal = entry[entry.find(start) + start.__len__():]
                        break # Found the beginning so stop looking

                # 3.2. Find the end
                if retVal.__len__() > 0:
                    for stop in stopList:
                        if entry.find(stop) >= 0:
                            retVal = retVal[:retVal.find(stop) + stop.__len__()]
                            break # Found the end so stop looking

                ### MOVED LOWER... Trim the URL after the original is found in htmlString
                ## 3.3. Trim the URL
                #if retVal.__len__() > 0:
                #    retVal = retVal.replace(' ', '%20') # urlopen() doesn't like spaces in the URL

                # 3.4. Verify work
                if retVal.__len__() > 0:
                    break

    # 4. Return original case-sensitive entry
    ## 4.1. Find original case-sensitive entry
    if retVal.__len__() > 0:
        temp = htmlString[htmlString.lower().find(retVal):]
        temp = temp[:retVal.__len__()]
        retVal = temp

        ## 4.2. Trim the URL
        retVal = retVal.replace(' ', '%20') # urlopen() doesn't like spaces in the URL

    return retVal    


'''
    Purpose: Trim HTML image name
    Input: A string containing a potential image name
    Output: 
        A string devoid of HTML codes and illegal characters on success
        An emtpy string on failure
'''
def trim_the_name(potentialName):
    retVal = potentialName

    if isinstance(potentialName, str):
        # UNWANTED CHARACTERS
        retVal = retVal.replace(' ', '-')
        retVal = retVal.replace('/', '-')            
        # HTML CODES
        retVal = retVal.replace('&#8211;', "-") # –
        retVal = retVal.replace('&#8212;', "-") # —
        retVal = retVal.replace('&#8213;', "-") # ―
        retVal = retVal.replace('&#8215;', "_") # ‗
        retVal = retVal.replace('&#8216;', "'") # ‘
        retVal = retVal.replace('&#8217;', "'") # ’
        retVal = retVal.replace('&#8218;', "")  # ‚
        retVal = retVal.replace('&#8219;', "'") # ‛
        retVal = retVal.replace('&#8220;', "")  # “
        retVal = retVal.replace('&#8221;', "")  # ”
        retVal = retVal.replace('&#8222;', "")  # „
        retVal = retVal.replace('&#8223;', "")  # ???
        retVal = retVal.replace('&#8224;', "")  # †
        retVal = retVal.replace('&#8225;', "")  # ‡
        retVal = retVal.replace('&#8226;', "-") # •
        retVal = retVal.replace('&#8230;', "")  # …
        retVal = retVal.replace('&#8240;', "")  # ‰
        retVal = retVal.replace('&#8242;', "'")  # ′
        retVal = retVal.replace('&#8243;', "'")  # ″
        retVal = retVal.replace('&#8249;', "")  # ‹
        retVal = retVal.replace('&#8250;', "")  # ›
        retVal = retVal.replace('&#8251;', "")  # ???
        retVal = retVal.replace('&#8252;', "")  # ‼
        retVal = retVal.replace('&#8253;', "")  # ???
        retVal = retVal.replace('&#8254;', "-")  # ‾
        retVal = retVal.replace('&#8260;', "-")  # ⁄
        retVal = retVal.replace('&#8266;', "")  # ⁊
        retVal = retVal.replace('&#8364;', "")  # ???
        retVal = retVal.replace('&#8482;', "")  # ???
        retVal = retVal.replace('nbsp', "")     # non-breaking space
        # CATCH ALL
        retVal = re.sub('[^A-Za-z0-9-_]+', '', retVal) # Catch all
        # Small quirk
        retVal = retVal.replace('39', "'")
        # CLEAN UP
        while retVal.find('__') >= 0:
            retVal = retVal.replace('__','_')
        while retVal.find('--') >= 0:
            retVal = retVal.replace('--','-')  
    else:
        retVal = ''

    return retVal

############### TO DO ###############
# Consider better algorithm for making the guess at the end
#     Even spread? (e.g., 2016:2, 2015:2, 2014:2)
#     None of the entries match?  (e.g., [2016,2015,2014] or [01,02,11]
#     What happens if the best guess indices don't match up? (e.g., 20160231 if days == [31,31,15,1] && months == [3,4,2,2]
#     What happens if there's a tie for most_common()?  (e.g., [31,31,31,8,8,14,14,14,2])
# Build in month vs day validation (e.g., Feb 31 is bad)
# After month vs day validation, build in Leap year check
#####################################
'''
    Purpose: Find and return the date a comic was created on
    Input: A string of HTML
    Output: 'YYYYMMDD' on success, '00000000' on failure
    Exceptions:
        TypeError('pageHTML is not a string or list')
        TypeError('pageHTML contains a non-string')
        ValueError('pageHTML is empty')
'''
def find_the_date(pageHTML):
    currentYear = int(time.strftime("%Y"))
    currentMonth = int(time.strftime("%m"))
    currentDay = int(time.strftime("%d"))
    retVal = '00000000'
    pageList = []
    rawDates = []
    rawYears = []
    rawMonths = []
    rawDays = []    

    if isinstance(pageHTML, list):
        pageList = pageHTML
    elif isinstance(pageHTML, str):
#        pageHTML.replace('<a', '<A')
# Logic flaw... only splits on '\n'... doesn't split on '<A' at all
#        pageList = pageHTML.split('<A')
#        pageList = pageHTML.split('\n')
#        re.split('<a|<A|\n', pageHTML)
#        pageList = pageHTML
        pageList = re.split('<a|<A|\n', pageHTML)
    else:
        raise TypeError('pageHTML is not a string or list')

    # 1. FIND APPROPRIATE ENTRIES
    if pageList.__len__() == 0:
        raise ValueError('pageHTML is empty')
    else:
        for entry in pageList:
            ## 1.0 INPUT VALIDATION
            if isinstance(entry, str) is False:
                raise TypeError('pageHTML contains a non-string')

            ## 1.1 FIND AN APPROPRIATE STRING OF NUMBERS FOR MMDDYYYY
            dateSearchObjMMDDYYYY = re.search(r'[0-1][0-9][0-3][0-9][1-2][0-9][0-9][0-9]', entry, re.M | re.I)

            try:
                dateFormatMatch = dateSearchObjMMDDYYYY.group()
            except:
                pass
            else:
                rawDates.append(entry)
#                print("FOUND MMDDYYYY:\t{}".format(dateFormatMatch)) # DEBUGGING
                continue     

            ## 1.2 FIND AN APPROPRIATE STRING OF NUMBERS FOR MM[-/.]DD[-/.]YYYY
            dateSearchObjMM_DD_YYYY = re.search(r'[0-1][0-9][-/.][0-3][0-9][-/.][1-2][0-9][0-9][0-9]', entry, re.M | re.I)

            try:
                dateFormatMatch = dateSearchObjMM_DD_YYYY.group()
            except:
                pass
            else:
                rawDates.append(entry)
#                print("FOUND MM_DD_YYYY:\t{}".format(dateFormatMatch)) # DEBUGGING
                continue             

            ## 1.3 FIND AN APPROPRIATE STRING OF NUMBERS FOR YYYY[-/.]MM[-/.]DD
            dateSearchObjYYYY_MM_DD = re.search(r'[1-2][0-9][0-9][0-9][-/.][0-1][0-9][-/.][0-3][0-9]', entry, re.M | re.I)

            try:
                dateFormatMatch = dateSearchObjYYYY_MM_DD.group()
            except:
                pass
            else:
                rawDates.append(entry)
#                print("FOUND YYYY_MM_DD:\t{}".format(dateFormatMatch)) # DEBUGGING
                continue

            ## 1.4 FIND AN APPROPRIATE STRING OF NUMBERS FOR YYYYMMDD
            dateSearchObjYYYYMMDD = re.search(r'[1-2][0-9][0-9][0-9][0-1][0-9][0-3][0-9]', entry, re.M | re.I)

            try:
                dateFormatMatch = dateSearchObjYYYYMMDD.group()
            except:
                pass
            else:
                rawDates.append(entry)
#                print("FOUND YYYYMMDD:\t{}".format(dateFormatMatch)) # DEBUGGING
                continue

            ## 1.5: FIND THE WORD DATE
            if entry.lower().find('date') >= 0:
#                print("FOUND 'DATE':\t{}".format(entry)) # DEBUGGING
                rawDates.append(entry)
                continue

            ## 1.6: FIND THE WORD TIME
            if entry.lower().find('time') >= 0:
#                print("FOUND 'TIME':\t{}".format(entry)) # DEBUGGING
                rawDates.append(entry)   
                continue         

            ## 1.7: FIND THIS YEAR
            elif entry.find(str(currentYear)) >= 0:
#                print("FOUND {}:\t{}".format(currentYear, entry)) # DEBUGGING
                rawDates.append(entry)
                continue
            
#            rawDates.append(entry)

    # 2. DETERMINE THE YEAR
    if rawDates.__len__() > 0:
        for entry in rawDates:

            chewedEntryYYYYMMDD = entry # YYYY-->MM-->DD order
            chewedEntryMMDDYYYY = entry # MM-->DD-->YYYY order

            ## 2.1. FIND THE FIRST OCCURRENCE OF A NUMBER IN chewedEntryYYYYMMDD
            try:
                newIndex = re.search('\d', chewedEntryYYYYMMDD).start()
            except:
                pass
            else:
                #if newIndex == 0: # BUG:  Always starts at index 1.  No need to advance here.
                #    newIndex = 1

                chewedEntryYYYYMMDD = chewedEntryYYYYMMDD[newIndex:]

            ## 2.1.1. FIND A YEAR FORMAT IN YYYY[-/]MM[-/]DD
            while chewedEntryYYYYMMDD.__len__() > 0:
                yearSearchObj = re.search(r'[1-2][0-9][0-9][0-9]', chewedEntryYYYYMMDD, re.M | re.I)

                try:
                    yearMatch = ''
                    yearMatch = yearSearchObj.group()
                except:
                    pass
                else:
                    if int(yearMatch) >= 1993 and int(yearMatch) <= currentYear:
    #                    print("ATTEMPTED YEAR MATCH = {}".format(yearMatch)) # DEBUGGING
    #                    rawYears.append(yearMatch)

                        trimmedEntry = chewedEntryYYYYMMDD[chewedEntryYYYYMMDD.find(yearMatch) + yearMatch.__len__():]
               
                        # 2.1.2. DETERMINE THE MONTH
                        if trimmedEntry[:2].isdecimal() == True:
                            monthMatch = trimmedEntry[:2]
                        else:
                            monthSearchObj = re.search(r'[-/.][0-1][0-9]', trimmedEntry, re.M | re.I)

                            try:
                                monthMatch = ''
                                monthMatch = monthSearchObj.group()
                            except:
                                pass
                            else:
                                monthMatch = monthMatch[1:]

                        # TEST RESULTS
                        if monthMatch.__len__() > 0:
                            if int(monthMatch) >= 1 and int(monthMatch) <= 12:
    #                            print("ATTEMPTED MONTH MATCH = {}".format(monthMatch)) # DEBUGGING
    #                            rawMonths.append(monthMatch[1:])

                                trimmedEntry = trimmedEntry[trimmedEntry.find(monthMatch) + monthMatch.__len__():]

                                # 2.1.3. DETERMINE THE DAY    
                                if trimmedEntry[:2].isdecimal() == True:
                                    dayMatch = trimmedEntry[:2]
                                else:
                                    daySearchObj = re.search(r'[-/.][0-3]\d+(?!\d)', trimmedEntry, re.M | re.I)

                                    try:
                                        dayMatch = ''
                                        dayMatch = daySearchObj.group()
                                    except:
                                        pass
                                    else:
                                        dayMatch = dayMatch[1:]


                                if dayMatch.__len__() > 0:
    #                                print("ATTEMPTED DAY MATCH = {}".format(dayMatch)) # DEBUGGING

                                    # 2.1.4. TEST THE RESULTS
                                    if int(dayMatch) >= 1 and int(dayMatch) <= 31:
    #                                    print("FOUND ONE in {}\nDATE:\t{}{}{}".format(entry, yearMatch, monthMatch, dayMatch)) # DEBUGGING
                                        rawYears.append(yearMatch)
                                        rawMonths.append(monthMatch)
                                        rawDays.append(dayMatch)

                # Chew the entry
#                chewedEntryYYYYMMDD = chewedEntryYYYYMMDD[1:]
                try:
                    newIndex = re.search('\d', chewedEntryYYYYMMDD).start()
                except:
                    break
                else:
                    if newIndex == 0:
                        newIndex = 1

                    chewedEntryYYYYMMDD = chewedEntryYYYYMMDD[newIndex:]

            ## 2.2. FIND THE FIRST OCCURRENCE OF A NUMBER IN chewedEntryMMDDYYYY
            try:
                newIndex = re.search('\d', chewedEntryMMDDYYYY).start()
            except:
                pass
            else:
                #if newIndex == 0: # BUG:  Always starts at index 1.  No need to advance here.
                #    newIndex = 1

                chewedEntryMMDDYYYY = chewedEntryMMDDYYYY[newIndex:]

            ## 2.2.1. FIND A MONTH FORMAT IN MM[-/]DD[-/]YYYY
            while chewedEntryMMDDYYYY.__len__() > 0:
                monthSearchObj = re.search(r'[0-1][0-9]', chewedEntryMMDDYYYY, re.M | re.I)

                try:
                    monthMatch = ''
                    monthMatch = monthSearchObj.group()
                except:
                    pass
                else:
                    if int(monthMatch) >= 1 and int(monthMatch) <= 12:

                        trimmedEntry = chewedEntryMMDDYYYY[chewedEntryMMDDYYYY.find(monthMatch) + monthMatch.__len__():]
               
                        # 2.2.2. DETERMINE THE DAY
                        if trimmedEntry[:2].isdecimal() == True:
                            dayMatch = trimmedEntry[:2]
                        else:
                            daySearchObj = re.search(r'[-/.][0-3][0-9]', trimmedEntry, re.M | re.I)

                            try:
                                dayMatch = ''
                                dayMatch = daySearchObj.group()
                            except:
                                pass
                            else:
                                dayMatch = dayMatch[1:]

                        # TEST RESULTS
                        if dayMatch.__len__() > 0:
                            if int(dayMatch) >= 1 and int(dayMatch) <= 31:

                                trimmedEntry = trimmedEntry[trimmedEntry.find(dayMatch) + dayMatch.__len__():]

                                # 2.2.3. DETERMINE THE YEAR    
                                if trimmedEntry[:4].isdecimal() == True:
                                    yearMatch = trimmedEntry[:4]
                                else:
                                    yearSearchObj = re.search(r'[-/.][1-2][0-9][0-9]\d+(?!\d)', trimmedEntry, re.M | re.I)

                                    try:
                                        yearMatch = ''
                                        yearMatch = yearSearchObj.group()
                                    except:
                                        pass
                                    else:
                                        yearMatch = yearMatch[1:]


                                if yearMatch.__len__() > 0:
                                    # 2.2.4. TEST THE RESULTS
                                    if int(yearMatch) >= 1993 and int(yearMatch) <= currentYear:
#                                        print("FOUND ONE in {0}:\t{2}{3}{1}".format('MMDDYYYY', yearMatch, monthMatch, dayMatch)) # DEBUGGING
                                        rawYears.append(yearMatch)
                                        rawMonths.append(monthMatch)
                                        rawDays.append(dayMatch)

                # Chew the entry
#                chewedEntryMMDDYYYY = chewedEntryMMDDYYYY[1:]
                try:
                    newIndex = re.search('\d', chewedEntryMMDDYYYY).start()
                except:
                    break
                else:
                    if newIndex == 0:
                        newIndex = 1

                    chewedEntryMMDDYYYY = chewedEntryMMDDYYYY[newIndex:]         

    # MAKE THE BEST GUESS
    ## YEAR
    if rawYears.__len__() > 0:
        guessYear = collections.Counter(rawYears)
        guessYear = guessYear.most_common(1)
        guessYear = guessYear[0]
        guessYear = guessYear[0]
        retVal = guessYear

        ## MONTH
        if rawMonths.__len__() > 0:
            guessMonth = collections.Counter(rawMonths)
            guessMonth = guessMonth.most_common(1)
            guessMonth = guessMonth[0]
            guessMonth = guessMonth[0]
            retVal = retVal + guessMonth

            if rawDays.__len__() > 0:
                ## DAY
                guessDay = collections.Counter(rawDays)
                guessDay = guessDay.most_common(1)
                guessDay = guessDay[0]
                guessDay = guessDay[0]
                retVal = retVal + guessDay
            else:
                retVal = '000000'
        else:
            retVal = '000000'
    else:
        retVal = '00000000'




#    print("ALL THE YEARS:\t{}".format(rawYears))
#    print("ALL THE MONTHS:\t{}".format(rawMonths))
#    print("ALL THE DAYS:\t{}".format(rawDays))

# NOTES:
#       Choose published over modified

    return retVal


'''
Purpose: Remove extraneous garbage from any URL
Input: URL - a string representing the URL to trim
Exceptions: TypeError('URL is not a string')
NOTE:   
        Removes any double slashes (//) except from http://
        Removes any spaces
        Removes any trailing slashes (/)
'''
def trim_a_URL(URL):

    retVal = ''

    if isinstance(URL, str):
        retVal = URL

        # 1. FIX ANY ERRONEOUS DOUBLE SLASHES
        while retVal.count('://') != retVal.count('//'):
            retVal = retVal.replace('//','/').replace(':/','://')

        # 2. REMOVE ANY SPACES
        retVal.replace(' ','')
        
        # 3. REMOVE TRAILING SLASHES
        if retVal[retVal.__len__() - 1:] == '/':
            retVal = retVal[:retVal.__len__() - 1]     
    
    else:
        raise TypeError('URL is not a string')       

    return retVal


'''
Purpose: Extract the root URL from any properly formed URL
Input: URL - a string representing the URL from which to extricate a root URL
Exceptions: 
        ValueError('URL is not a URL')
        TypeError('URL is not a string')
NOTE: Calls trim_a_URL() on URL  
'''
def get_root_URL(URL):

    retVal = ''
    # Ordered list (most restrictive to least restrictive) of website beginnings
#    SITE_DELIMITER_START = ['www.', '//', ':', 'https', 'http']
    # Unordered list of website TLDs
    SITE_DELIMITER_STOP = [
        # Generic top-level domains
        '.com', '.org', '.net', '.int', 'edu', '.gov', '.mil', '.arpa', 
        # Country code top-level domains
        '.ac', '.ad', '.ae', '.af', '.ag', '.ai', '.al', '.am', '.an', 
        '.ao', '.aq', '.ar', '.as', '.at', '.au', '.aw', '.ax', '.az', 
        '.ba', '.bb', '.bd', '.be', '.bf', '.bg', '.bh', '.bi', '.bj', 
        '.bl', '.bm', '.bn', '.bo', '.bq', '.br', '.bs', '.bt', '.bv', 
        '.bw', '.by', '.bz', '.ca', '.cc', '.cd', '.cf', '.cg', '.ch', 
        '.ci', '.ck', '.cl', '.cm', '.cn', '.co', '.cr', '.cu', '.cv', 
        '.cw', '.cx', '.cy', '.cz', '.de', '.dj', '.dk', '.dm', '.do', 
        '.dz', '.ec', '.ee', '.eg', '.eh', '.er', '.es', '.et', '.eu', 
        '.fi', '.fj', '.fk', '.fm', '.fo', '.fr', '.ga', '.gb', '.gd', 
        '.ge', '.gf', '.gg', '.gh', '.gi', '.gl', '.gm', '.gn', '.gb', 
        '.gd', '.ge', '.gf', '.gg', '.gh', '.gi', '.gl', '.gm', '.gn', 
        '.gp', '.gq', '.gr', '.gs', '.gt', '.gu', '.gw', '.gy', '.hk', 
        '.hm', '.hn', '.hr', '.ht', '.hu', '.id', '.ie', '.il', '.im', 
        '.in', '.io', '.iq', '.ir', '.is', '.it', '.je', '.jm', '.jo', 
        '.jp', '.ke', '.kg', '.kh', '.ki', '.km', '.kn', '.kp', '.kr', 
        '.kw', '.ky', '.kz', '.la', '.lb', '.lc', '.li', '.lk', '.lr', 
        '.ls', '.lt', '.lu', '.lv', '.ly', '.ma', '.mc', '.md', '.me', 
        '.mf', '.mg', '.mh', '.mk', '.ml', '.mm', '.mn', '.mo', '.mp', 
        '.mq', '.mr', '.ms', '.mt', '.mu', '.mv', '.mw', '.mx', '.my', 
        '.mz', '.na', '.nc', '.ne', '.nf', '.ng', '.ni', '.nl', '.no', 
        '.np', '.nr', '.nu', '.nz', '.om', '.pa', '.pe', '.pf', '.pg', 
        '.ph', '.pk', '.pl', '.pm', '.pn', '.pr', '.ps', '.pt', '.pw', 
        '.py', '.qa', '.re', '.ro', '.rs', '.ru', '.rw', '.sa', '.sb', 
        '.sc', '.sd', '.se', '.sg', '.sh', '.si', '.sj', '.sk', '.sl', 
        '.sm', '.sn', '.so', '.sr', '.ss', '.st', '.su', '.sv', '.sx', 
        '.sy', '.sz', '.tc', '.td', '.tf', '.tg', '.th', '.tj', '.tk', 
        '.tl', '.tm', '.tn', '.to', '.tp', '.tr', '.tt', '.tv', '.tw', 
        '.tz', '.ua', '.ug', '.uk', '.um', '.us', '.uy', '.uz', '.va', 
        '.vc', '.ve', '.vg', '.vi', '.vn', '.vu', '.wf', '.ws', '.ye', 
        '.yt', '.za', '.zm', '.zw'	
    ]

    if isinstance(URL, str):
        # 1. CLEAN UP THE URL
        try:
            retVal = trim_a_URL(URL)
        except Exception as err:
            print(repr(err))

        # 2. REMOVE ANY SUBDIRECTORIES
        ## 2.1. Check for 'http://'
        urlIndex = retVal.find('//')
        ## 2.2. Set the starting index as apporpriate
        if urlIndex >= 0:
            urlIndex += 2 # String length
        else:
            urlIndex = 0

        # 2.3. Starting after any occurrences of 'http://', find the first subdirectory...
        urlIndex = retVal.find('/', urlIndex)
        if urlIndex >= 0:
            ## ...and slice it out
            retVal = retVal[:urlIndex]

        # 3. GET TO THE TLD
        foundSuffix = '' # Holds the TLD suffix found in the URL
        for suffix in SITE_DELIMITER_STOP:
            if retVal.find(suffix) >= 0:
                foundSuffix = suffix
                retVal = retVal[:retVal.find(suffix) + suffix.__len__()]
                break # There should only be one so stop looking for more

        # Didn't find a suffix
        if foundSuffix.__len__() == 0:
            raise ValueError('URL is not a URL')
    else:
        raise TypeError('URL is not a string')        

    return retVal
