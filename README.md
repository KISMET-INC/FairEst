# Fair-EST

## Description
In a world full of mixed breeds, this application generates estimates for grooming services based on weight and coat type instead of breed which is sometimes hard to determine.

## Technologies
The programs backend was written in **Python** and the **Django ORM** was used as a templating engine for creating models that interface with the **SQL Database** and to manipulate the DOM and display database information.

**Python**  was chosen due to its ease of use and it's forgiving syntax. **Django ORM** on the other hand, interfaces extremely well with the database and therefore relationships between database entries are easily defined.

A **SQL** database was utilized because of the nature of the relationships needed between the database models of this project. For example (in this situation): grooming shops have multiple customers, customers have multiple dogs, dogs have only one owner. Using a relational database was important to effectivley and efficiently map these connetions.

## Screenshots

![alt text](/fairest_readme/fairest02.jpg)
![alt text](/fairest_readme/fairest01.jpg)

## Installation

1. Clone the repository down to your local drive by opening up a terminal in the folder of your choice and type the code: 
```bash
git clone https://github.com/KISMET-INC/FairEst.git
```

2. Download and Install **[Python 3.6.4](https://www.python.org/downloads/release/python-364/)** onto your machine.

3. Be sure to Add Python 3.6 to PATH but checking the box at the bottom of the screen 
   - [x] Add Python 3.6 to PATH

1. Create a virtual environment for the project.
```bash
Windows:
python -m venv py3Env

Mac/Linux
python3 -m venv py3Env
```
5. Activate the environment
```bash

Mac/Linux: 
source py3Env/bin/activate                         
 
Windows command prompt : 
call py3Env\Scripts\activate       

Windows git bash :
source py3Env/Scripts/activate         

```
6. With your virtual environment active install Django using PIP package manager
```base
Windows/Mac: 
$ pip install Django==2.2.4 
```
> Note: If PIP isn't installing you may hae to add it to your PATH

7. Now you should be able to work with and edit the file.

8. To run the project navigate to the folder where you cloned this repo and run this in the command line
```bash
python manage.py runserver
```


## Support
Any questions or comments about this repository and it's contents can be emailed to kmoreland909@gmail.com.

## Roadmap
Currently this is a work in progress. As I get better and upgrade my projects or add new ones this website will be constantly updated to reflect that. Bookmark the deployment url for this site, KISMET-INC.github.io to see what I add to it in the future.

## Contributing
I am not accepting contributions to this project at this time.

## Authors and Acknowledgment
Thank you to the amazing staff and instructors at **[Coding Dojo](https://www.codingdojo.com/onsite-boot-camp#dates-and-tuition)** for teaching me the skills and technologies needed for me to complete this project.