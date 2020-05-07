# DBL-Project
 
To get the local server to work, you need to go to the terminal window. 
First activate the virtual environment by typing ```. venv/bin/activate```. 
Then you have to do ```pip install flask```
Then to run the server, type ```python main.py```.  
Some stuff appears in the terminal window. Click on ```http://127.0.0.1:5000/``` (or just copy paste this) and it will open up a new window on chrome or whatever. You can upload a jpeg, pdf, csv, png file. The file will then be uploaded to ```/static/Uploads```. On the side are links to different visualizations (no graphs yet :(.. ) Also whenever you visit the home page, a colored image is randomly selected and put on the background (still working on the background part).  

Please create a new branch from main so that any changes made are not reflected upon the whole branch. Then work in that branch, and when you are ready to push a stable change, like adding a functionality that works, then you may push to master. I (Victor) will review it and accept it. 

Structure of the project:  
- ```pycache``` has nothing interesting.  Neither really ```.vscode``` or ```venv```.  
You don't have to do anything in app.py.  

- ```Static``` holds all files that flask will have to access. Inside is the ```CSS``` folder for all CSS files,  ```Stimuli``` folder for all images given to us, plus everytime a user visits the homepage a new color image is randomly selected, ```Uploads``` folder is for user uploads, and ```Visualizations``` is for the visualization files.  
- ```templates``` holds all of the HTML files.  
- ```Main.py``` is where the magic happens. This handles all of the python code.  
- ```test.py``` is where I dump all of my changes, tinker with shit, or if I need to chnage something that I fucked up a long time ago, thats where I copy-paste what I have at the time of noticing the fuck up.   