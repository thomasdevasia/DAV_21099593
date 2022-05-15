DAV_21099593

# CMT218 Data Visualisation Coursework 2

The visulaization is built using Python's Dash Library. This Readme file contains the step to run the program to see the visualization.

## Install
To install the required files make surre you have a python installed on the machine. Then proceed to run the following line on your terminal.

    pip install -r requirement.txt

## To run Server
To run the server change your present working directory to this folder then run following line on your terminal.

    python app.py

Do make a note that the server starts at port 8050 by default. To change the port incase 8050 is already in use, locate app.py and change following line of code.

    app.run_server(debug=True, port={Desired Port}) 
