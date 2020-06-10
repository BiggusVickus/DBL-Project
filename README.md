# DBL-Project

 It's best to start this porject with Visual Studio Code, although terminal/command prompt or another editor/IDE should work. 
To get the local server to work, you need to go to the terminal window (either command prompt or VSCode) and change your directory to the project location. 
Activate the virtual environment by typing ```. venv/bin/activate```. Turns out for Windows you use ```venv\bin\activate```. 

Before you can run the server you have to make sure that you have all the necessary libraries installed for python. You can install libraries by typing ```pip install {library name}``` in your terminal/command prompt. You will need the following libraries: ```flask, bokeh, numpy, pandas, matplotlib, seaborn``` and ```PIL ```.

Then to run the server, make sure to direct to the proper folder in your terminal/command prompt and type ```python main.py``` into the terminal window. As of right now, you will get a lot of text, but somewhere you will find a line that says ```* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)```. Copy this address into a browser and you will be directed to the site. 

On the homepage of our site you can upload a jpeg, pdf, csv or png file*. The file will then be uploaded to ```static/Visualizations/Uploads```. Every time you revisit or reload the homepage, a new colored metro map image is randomly selected and displayed as a background. Multiple files can be uploaded by holding cmd or ctrl. You can go to different pages for different visualizations. All the visualizations are working on the site, however the heatmap takes a long time to load and the sliders next to the visualization do not have an implemented function yet.

*Although the upload function works, we haven't added support for files outside of the csv file given to us. Also when you upload your own images, they go to the wrong directory. We have preloaded the required csv and images into the proper place for you. The best way to use this software in it's current state is to use the software as is without uploading any files. Then after checking everthing out, you can upload your own files to check that the upload function works. 
