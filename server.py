#Backend sever file

import multiprocessing_driver as integration_backend
import logging

#Flask backend imports
from flask import Flask
app = Flask(__name__)

#########################################################################################
#########################################################################################
####   PLACE API ROUTES HERE   ###

#Test: members API route
@app.route("/members")
def members():
    return {"members": ["mem1", "mem2", "mem3"]}

####   END OF API ROUTES   ###
#########################################################################################
#########################################################################################

def main():
    
    #guard for multiprocessing
    if __name__ == '__main__':
        print("backend start")

        #Call Driver file
        integration_backend.driver()


        #Run the Flask
        app.run(debug=True)
main()
