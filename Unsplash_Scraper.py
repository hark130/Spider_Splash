#########################################################################
################################# TO DO #################################
#########################################################################
# Instead of 'trimming off garbage', utilize urlparse
# Find a way to determine file type instead of hard-coded file extension 
# Determine a unique naming algorithm based on the available information
#########################################################################
#########################################################################
#########################################################################

################
# LOAD MODULES #
################
from urllib.request import urlopen
# from urllib.request import urlretrieve
from urllib.request import Request
import urllib.error
import sys
import os
# import time
# import random
# import re
from Scraper_Functions import is_URL_valid
from Scraper_Functions import find_the_date
# from Scraper_Functions import find_a_URL 
# from Scraper_Functions import get_image_filename
# from Scraper_Functions import make_rel_URL_abs
################
################
################

########################
### STATIC VARIABLES ###
########################
MAX_SKIPS = 2                  # Max number of existing files to skip over before stopping
USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0' # http://www.whoishostingthis.com/tools/user-agent/
#USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0' # http://www.whoishostingthis.com/tools/user-agent/
currentURL = 'https://unsplash.com/'
validFileTypeList = ['.jpeg']   #, '.png', '.jpg', '.gif'] # Site appears to exclusively utilize jpegs
imageSearchPhrase = 'https://images.unsplash.com/photo-'
imageBeginPhrase = 'background-image:url(&quot;'
########################
# Script constants #####
########################

#########################
### DYNAMIC VARIABLES ###
#########################
# Windows 7 home path environment variable
if 'USERPROFILE' in os.environ:
    SAVE_PATH = os.path.join(os.environ['USERPROFILE'], 'Pictures', 'Unsplash')
# Ubuntu 16.04 LTS home path environment variable
elif 'HOME' in os.environ:
    SAVE_PATH = os.path.join(os.environ['HOME'], 'Pictures', 'Unsplash')
# ./Pictures/
else:
    SAVE_PATH = os.path.join('Pictures', 'Unsplash')   
numSkips = 0                    # Variable to store the number of files already found
#########################
# Run time update #######
#########################

######################
### TEMP VARIABLES ###
######################
incomingFilename = ''       # Local filename to save the incoming image download
imageURL = ''               # Trimmed image URL
currentFileExtension = ''   # File extension of current image to download
imageID = ''                # Unique ID assigned to a given image
imageCreationDate = ''      # Date image was created
imageUserID = ''            # Unique user ID of the artist
######################
# Reset each loop ####
######################

print('\nBegin Scraping\n')

# VERIFY SAVE DIRECTORY EXISTS
if os.path.exists(SAVE_PATH):
    if os.path.isdir(SAVE_PATH):
        print("Save directory exists:\t{}".format(SAVE_PATH))
    else:
        print("Save directory is not a directory!\nERROR:\t{}".format(SAVE_PATH))
        sys.exit()
else:
    print("Save directory does not exist!\nERROR:\t{}".format(SAVE_PATH))
    print("Creating save directory at:\t{}".format(SAVE_PATH))
    os.mkdir(SAVE_PATH) 

# COMMENCE SCRAPING
while numSkips < MAX_SKIPS:
    # 1. OPEN THE WEB PAGE
    print("\n1. Opening {}".format(currentURL)) # DEBUGGING

    ## 1.1. Verify URL is valid
    try:
        if is_URL_valid(currentURL) is False:
            print("Invalid URL:\t{}".format(currentURL)) # DEBUGGING
            sys.exit()
    except Exception as err:
        print(repr(err)) # DEBUGGING
        sys.exit()

    ## 1.2. Open the URL
    try:
        unsplashRequest = Request(currentURL, headers={'User-Agent': USER_AGENT})
        unsplash = urlopen(unsplashRequest)
    except urllib.error.URLError as error:
        print("\nCannot open URL:\t{}".format(currentURL)) # DEBUGGING
        print("ERROR:\t{} - {}".format(type(error),error)) # DEBUGGING
        sys.exit()
    else:
        print("Opened URL:\t{}".format(currentURL)) # DEBUGGING


    # 2. DETERMINE CHARSET OF PAGE
    print("\n2. Determine {} Charset".format(currentURL)) # DEBUGGING

    ## 2.1. Get the content type from the header
    unsplashContentType = unsplash.getheader('Content-Type')

    ## 2.2. Look for a character set
    if unsplashContentType.find('=') < 0 or unsplashContentType.find('charset') < 0:
        unsplashCharset = 'UTF-8'
    else:
        unsplashContentType = unsplashContentType[unsplashContentType.find('charset'):]
        unsplashCharset = unsplashContentType[unsplashContentType.find('=') + 1:]
        unsplashCharset = unsplashCharset.replace(' ','')
    print("Charset:\t{}".format(unsplashCharset)) # DEBUGGING


    # 3. TRANSLATE PAGE
    print("\n3. Translate {} HTML".format(currentURL)) # DEBUGGING

    ## 3.1. Read the content
    unsplashContent = unsplash.read()

    ## 3.2. Decode the content
    try:
        unsplashContentDecoded = unsplashContent.decode(unsplashCharset, 'ignore')
    except UnicodeError as error:
        print("Unable to decode URL {} with charset {}".format(currentURL, unsplashCharset))
        print("ERROR:\t{}\n{}".format(type(error),error))
        sys.exit()
    else:
#        unsplashHTML = unsplashContentDecoded.split('\n') # No longer necessary in Version 1-2
        print("Successfully decoded the page content") # DEBUGGING
        pass

    while unsplashContentDecoded.__len__() > 0:
#        print("{}".format(unsplashContentDecoded)) # DEBUGGING

        # 4. FIND THE IMAGE URL
        print("\n4. Fetching Image Details") # DEBUGGING

        ## 4.1. Slice to an entry
        if unsplashContentDecoded.find('"id": "') >= 0:
            unsplashContentDecoded = unsplashContentDecoded[unsplashContentDecoded.find('"id": "'):]
        else:
            print("\tDid not find another entry") # DEBUGGING
            break # No more entries.  Stop looking.

        ## 4.2. Read the image ID
        imageID = unsplashContentDecoded[unsplashContentDecoded.find('"id": "') + '"id": "'.__len__():]
#        print("Image ID post-slice #1:\t{}".format(imageID)) # DEBUGGING
        imageID = imageID[:imageID.find('"')]
#        print("Image ID post-slice #2:\t{}".format(imageID)) # DEBUGGING
        print("\tImage ID:\t{}".format(imageID)) # DEBUGGING

        ## 4.3. Read the user ID
        if unsplashContentDecoded.find('"userId": "') >= 0:
            imageUserID = unsplashContentDecoded[unsplashContentDecoded.find('"userId": "') + '"userId": "'.__len__():]
            imageUserID = imageUserID[:imageUserID.find('"')]
            print("\tUser ID:\t{}".format(imageUserID)) # DEBUGGING
        else:
            print("\tDid not find a user ID for image ID {}".format(imageID)) # DEBUGGING
            break # No more entries.  Stop looking.

        ## 4.4. Read the image URL
        ### 4.4.1. Slice to the URL
        imageURL = unsplashContentDecoded[unsplashContentDecoded.find('"raw": "') + '"raw": "'.__len__():]
        imageURL = imageURL[:imageURL.find('"')]
        if imageURL.__len__() == 0:
            print("\tDid not find an image URL for image ID {}".format(imageID)) # DEBUGGING
            break # No more entries.  Stop looking.
        else:
            ### 4.4.2. Test the URL
            if imageURL.__len__() > 0:
                #### 4.4.2.1. Clean up any URLs that begin with '//' because Request() doesn't like them
                if imageURL.find('//') == 0:
                    imageURL = 'http:' + imageURL

                #### 4.4.2.2. Trim off garbage
                if imageURL.find('?') > 0:
                    imageURL = imageURL[:imageURL.find('?'):]
                    
                #### 4.4.2.2. Verify URL is valid
                try:
                    if is_URL_valid(imageURL) is False:
                        print("\tInvalid URL:\t{}".format(imageURL)) # DEBUGGING
                        sys.exit()
                except Exception as err:
                    print(repr(err))
                    sys.exit()
                else:
                    print("\tImage URL:\t{}".format(imageURL)) # DEBUGGING
                    pass
            else:
                print("\tCould not find Image URL") # DEBUGGING
                sys.exit()

        ## 4.5. Read the creation date
        if unsplashContentDecoded.find('"created_at"') >= 0:
            imageCreationDate = unsplashContentDecoded[unsplashContentDecoded.find('"created_at"'):]
            imageCreationDate = imageCreationDate[:imageCreationDate.find('width')]
            try:
                imageCreationDate = find_the_date(imageCreationDate)
            except Exception as err:
                print(repr(err))
                sys.exit()
            else:
                if imageCreationDate == '00000000':
                    print('\tUnable to find the creation date for image ID:\t{}'.format(imageURL))
                else:
                    print("\tCreation:\t{}".format(imageCreationDate)) # DEBUGGING
                    pass
        else:
            break # No more entries.  Stop looking.    
        

        # 5. DETERMINE THE IMAGE FILE EXTENSION
        print("\n5. Determining Image File Type") # DEBUGGING
        # But how?  Read the page headers again?  For now, hard-coded.
        currentFileExtension = '.jpeg'
        print("Image file is a {}".format(currentFileExtension))


        # 6. BUILD THE IMAGE FILENAME
        print("\n6. Creating Image File Name") # DEBUGGING
        ## 6.1. Prefix
        incomingFilename = 'Unsplash_'
        ## 6.2. Date
        if imageCreationDate.__len__() == 8 and imageCreationDate != '00000000':
            incomingFilename = incomingFilename + imageCreationDate
        ## 6.3. User ID
        if imageUserID.__len__() > 0:
            incomingFilename = incomingFilename + '-' + imageUserID
        ## 6.4. Image ID
        if imageID.__len__() > 0:
            incomingFilename = incomingFilename + '-' + imageID
        ## 6.5. File extension
        incomingFilename = incomingFilename + currentFileExtension
        print("Image filename will be {}".format(incomingFilename)) # DEBUGGING


        # 7. DOWNLOAD THE FILE
        print("\n7. Downloading {}".format(incomingFilename)) # DEBUGGING
        if imageURL.__len__() > 0 and incomingFilename.__len__() > 0:
            ## 7.1. Verify the file doesn't exist so we're downloading it
            if os.path.exists(os.path.join(SAVE_PATH, incomingFilename)) == False:
                ### 7.1.1. Try to download it
                try:
                    # Utilizing a request-->urlopen-->write() in an attempt to...
                    # ...continue dodging websites that block webscrapers.
                    unsplashRequest = Request(imageURL, headers={'User-Agent': USER_AGENT})
                    with urlopen(unsplashRequest) as unsplash:
                        with open(os.path.join(SAVE_PATH, incomingFilename), 'wb') as outFile:
                            outFile.write(unsplash.read())
                except urllib.error.HTTPError as err:
                    print("Image failed to download:\t{}".format(imageURL))

                    #### 7.1.1.1. Handle 404 errors
                    if err.code == 404:
                        print("404 Error:\t{}".format(imageURL))
                        numSkips += 1
    #                    sys.exit()
                    #### 7.1.1.2. Abort on non 404 errors
                    else:
                        print(repr(err))
                        sys.exit()
                except Exception as err:
                    print("Image failed to download:\t{}".format(imageURL))
                    print(repr(err))
                    sys.exit()
                ### 7.1.2. Success   
                else:
                    print("Image download successful:\t{}".format(incomingFilename)) # DEBUGGING
                    pass
            ## 7.2. The file exists so we're moving on
            else:
                numSkips += 1
                print("Filename {} already exists.".format(incomingFilename)) # DEBUGGING
        else:
            print('Missing download criteria\nImage URL:\t{}\nFilename:\t{}'.format(imageURL, incomingFilename)) # DEBUGGING
            sys.exit()


        # 8. CHECK IF WE'RE DONE
#        print("\n8. Done yet?") # DEBUGGING
        ## 8.1. Verify the script hasn't exceeded the maximum number of skips
        if numSkips >= MAX_SKIPS and MAX_SKIPS > 0:
            print("\n{} URLs skipped.\nEnding scrape.".format(numSkips))
            break

        # 9. Slice past this entry
        unsplashContentDecoded = unsplashContentDecoded['"id": "'.__len__():]

        # 10. RESET TEMP VARIABLES TO AVOID DUPE DOWNLOADS AND OTHER ERRORS
        incomingFilename = ''       # Local filename to save the incoming image download
        imageURL = ''               # Trimmed image URL
        currentFileExtension = ''   # File extension of current image to download
        imageID = ''                # Unique ID assigned to a given image
        imageCreationDate = ''      # Date image was created
        imageUserID = ''            # Unique user ID of the artist


# DONE SCRAPING
print("Done scraping {}".format(currentURL))


    # The following HTML format is being used to find and identify each individual image URL

    # "asyncPropsPhotos": {
    #   "okzxVsJNxXc": {
#-->#     "id": "okzxVsJNxXc",
#-->#     "created_at": "2015-05-14T15:34:32-04:00",
    #     "width": 7360,
    #     "height": 4912,
    #     "color": "#7E8887",
    #     "likes": 792,
    #     "liked_by_user": false,
#-->#     "userId": "7VotA9sc3vQ",
    #     "current_user_collection_ids": [],
    #     "urls": {
#-->#       "raw": "https://images.unsplash.com/photo-1431631927486-6603c868ce5e",
    #       "full": "https://images.unsplash.com/photo-1431631927486-6603c868ce5e?ixlib=rb-0.3.5&q=80&fm=jpg&crop=entropy&cs=tinysrgb&s=0fea28ab03f5eb3910a742c5574c3a2e",
    #       "regular": "https://images.unsplash.com/photo-1431631927486-6603c868ce5e?ixlib=rb-0.3.5&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=1080&fit=max&s=9421042a5b27dcf4a53e2dc9032308fc",
    #       "small": "https://images.unsplash.com/photo-1431631927486-6603c868ce5e?ixlib=rb-0.3.5&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=400&fit=max&s=1046c0d52d89381d4b5db930b78ccd42",
    #       "thumb": "https://images.unsplash.com/photo-1431631927486-6603c868ce5e?ixlib=rb-0.3.5&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=200&fit=max&s=234b2d1ff3217e3999b021f640122d11"
    #     },
    #     "categories": [
    #       {
    #         "id": 2,
    #         "title": "Buildings",
    #         "photo_count": 22897,
    #         "links": {
    #           "self": "https://api.unsplash.com/categories/2",
    #           "photos": "https://api.unsplash.com/categories/2/photos"
    #         }
    #       },
    #       {
    #         "id": 4,
    #         "title": "Nature",
    #         "photo_count": 54184,
    #         "links": {
    #           "self": "https://api.unsplash.com/categories/4",
    #           "photos": "https://api.unsplash.com/categories/4/photos"
    #         }
    #       }
    #     ],
    #     "links": {
    #       "self": "https://api.unsplash.com/photos/okzxVsJNxXc",
    #       "html": "http://unsplash.com/photos/okzxVsJNxXc",
    #       "download": "http://unsplash.com/photos/okzxVsJNxXc/download",
    #       "download_location": "https://api.unsplash.com/photos/okzxVsJNxXc/download"
    #     }
    #   },
