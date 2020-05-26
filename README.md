# DBL-Project

 It's best to start this porject with Visual Studio Code, although terminal/command prompt or another editor/IDE should work. 
To get the local server to work, you need to go to the terminal window (either command prompt or VSCode) and change your directory to the project location. 
Activate the virtual environment by typing ```. venv/bin/activate```. Turns out for Windows you use ```venv\bin\activate```. 

Then to run the server, type ```python main.py``` into the terminal window. If it gives some flask error, then type ```pip install flask```. Run ```python main.py``` again. You might have to do ```pip install bokeh``` as well. 

Please note that you might see a list of problems and errors. You have to find ```http://127.0.0.1:5000/``` and it will open up a new window on your default web browser. You can upload a jpeg, pdf, csv, png file*. The filse will then be uploaded to ```static/Visualizations/Uploads```. Multiple files can be selected and uploaded by holding cmd or ctrl. You can go to different pages for different visualizations. Everytime you visit the homepage, a new colored metro map image is randomly selected and displayed as a background. Each visualizations should be working 

*Although the upload function works, we haven't added support for files outside of the csv file given to us. Also when you upload your own images, they go to the wrong directory. We have preloaded the required csv and images into the proper place for you. The best way to use this software in it's current state is to use the software as is without uploading any files. Then after checking everthing out, you can upload your own files to check that the upload function works. 
