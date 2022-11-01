import logging
import sys

#Remote controller for playback for Soundcloud API
def Control_Soundcloud_Playback(remote = None, command = None):

    #Get Soundcloud USER ID
    soundcloud_account_dict = remote.get_account_details()
    #print(soundcloud_account_dict)
    #print(type(soundcloud_account_dict))
    #USER_ID = soundcloud_account_dict.userId
    #print("USER_ID: ", USER_ID)

    #If a remote is given and command is given for playback
    if((remote != None) and (command != None)):
        
        #Play Soundcloud    
        if(command == "play"):
            #
            #remote.get_user_details(self, USER_ID)
            print("tempstring")

    ##If a remote is NOT given OR command is NOT given for playback
    else:
        if(remote == None):
            logging.error("No Soundcloud API OBJECT passed in Control_Playback_Soundcloud.py")
        
        elif(command == None):
            logging.error("No COMMAND for Soundcloud given in Control_Playback_Soundcloud.py")

        else:
            logging.error("Problem in Control_Soundcloud_Playback.py Control_Soundcloud_Playback() flow Error Code:")
            sys.exit(0)