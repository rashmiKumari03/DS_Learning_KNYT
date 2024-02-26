# Welcome to End to End Data Science Project Setup Guide (Student Performance) 🚀


### A. Git and Github Repository Setup

   1. Make README.md, requirements.txt
   2. Initialize the Git Repo in this Folder. 
        ```bash
        git init 
        ```
   3. Add `.gitignore` and `LICENSE` files.
   4. Create a Virtual Environment and activate it.
        ```bash
        conda create -p venv python==3.9 -y
        conda activate venv/
        ```
   5. Add virtual environment (`venv/`) to `.gitignore`.
   6. Update README.md with project details.
   7. Write required packages in `requirements.txt` and install them.
        ```bash
        pip install -r requirements.txt
        ```
   8. Push changes to Github Repo.
        ```bash
        git add .
        git commit -m "Initial commit"
        git remote add origin <repository_url>
        git push -u origin master
        ``
   9. After installing requirements.txt also install ipykernel (to use jupyter notebook).
       ```bash
       pip install ipykernel
       ```
     (if while using ipynb --> importing pandas says --> To install Pyarrow 
      --> then install it also in terminal using --> pip install Pyarrow)


   
   10. Creating `setup.py` and add `-e .` into requirements.txt
      ```
      This setup.py file is very important , because this will make the Folder/application as package...and we can even push it to PyPi and anyone can use it as package.Here we can add various informations about the package also who created it,on which date and so many things.
      ```
      Now , Once we have -e . in requirements.txt --> do pip install -r requirements.txt --> this will create the dir as package.

      Best way --> To comment down -e . for now and make the dir a package at the end of the end to end project...
       

   11. Creating logger.py and exception.py and calling these to app.py and run app.py as oue application and gets the logs.
       
-----------------------------------------------------------------------------------------------------------------------------
### B. Project Setup

   1. Data Ingestion code: Here we use utiles file --> utiles.py (where we read data from mysql database) Then we come to components-->data_ingestion file--> train_test_split the data and store it into artifcats file..also use logging and CustomException to handle the error. Some new packages were installed in requirements.txt --> pymysql and python-dotenv (for reading the sql data from database with proper config information). Output : artifacts folder--> 1.raw_data 2.train_data 3.test_data

   ![alt text](img_extra/01.DataIngestion_and_traintestsplit.png)




   2. Data transformation code:

This setup guide aims to streamline the process of initializing a data science project, ensuring proper version control with Git, and maintaining a clean project structure. Happy coding! 🎉