from soundcloudpy import Soundcloud
import SoundCloud_Config
import Control_Playback_Soundcloud
import get_soundcloud_lists
from soundcloud_lists import SoundCloud_Data


import logging

#Set log level to INFO to debug (WARNING is default)
logging.basicConfig(level=logging.WARNING)

#########################################################################
#Soundcloud Test Driver for basic functionality
def main():

    #Authenticate Soundcloud API Key
    #Note follow readme in soundcloud-py to figure out how to get API ID and Key. Add to Soundcloud_Config.py
    soundcloud_account = Soundcloud(SoundCloud_Config.SOUNDCLOUD_SECRET, SoundCloud_Config.SOUNDCLOUD_ID)

    #If the soundcloud authentication is succesfull get control of API    
    if(soundcloud_account != None):
        #Control_Playback_Soundcloud.Control_Soundcloud_Playback(remote = soundcloud_account, command = "play")
         
        soundcloud_d = SoundCloud_Data()
                
        get_soundcloud_lists.Get_Soundcloud_lists(remote = soundcloud_account, soundcloud_data_obj = soundcloud_d)



        #print(soundcloud_account.get_account_details())







    #End of the test
    print("\n\nSoundcloud test working")







#########################################################################
#########################################################################
main()
