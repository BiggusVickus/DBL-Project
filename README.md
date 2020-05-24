# DBL-Project

 
To get the local server to work, you need to go to the terminal window. 
First activate the virtual environment by typing ```. venv/bin/activate```. Turns out for Windows you use ```venv\bin\activate```. 

Then to run the server, type ```python main.py``` into the terminal window. If it gives some flask error, then type ```pip install flask```. Run ```python main.py``` again. You might have to do ```pip install bokeh``` as well. Some stuff appears in the terminal window. Click on ```http://127.0.0.1:5000/``` and it will open up a new window on your default web browser. You can upload a jpeg, pdf, csv, png file. The file will then be pushed to ```static/Uploads```. Multiplefiles can be selected. You can go to different pages for different visualizations. Everytime you visit the homepage, a new colored metro map image is randomly selected and displayed as a background. 

Although the upload function works, we haven't added support for files outside of the csv file given to us. Also when you upload your own images, they go to the wrong directory. We have preloaded the required csv and images into the proper place for you. The best way to use this software in it's current state is to use the software as is without uploading any files. Then after checking everthing out, you can upload your own files to check that the upload function works. 
