# Corrector

This is a small flask program that can be used to correct submissions to the ILIAS system.

Corrector is being developed on archlinux with the latest released python and chromium versions.

Below are all available commands that can be run from the shell. These are given for archlinux, you might need to adjust them to your system.
```
# create a python 3 virtualenv
virtualenv env
source env/bin/activate

# install requirements
pip install -r requirements.txt

# create database
python create_db.py

# run the web interface
python runserver.py

# create migrations (only needed if you change the models)
python create_migrations.py

# update database to the latest migration
python update_db.py

# downgrade database one migration
python downgrade_db.py
```


## How to use

* Create the directory `corrector/data`
* Start the web interface

* For each assignment you want to correct, extract the submissions of the students into a subdirectory of `corrector/data` (`corrector/data/assignment_1` for example)

* Go to http://localhost:5000/
* Press `Synchronize Exercises` to read `corrector/data` and create entries for the submissions in the database.  
Note that each exercise (subdirectory) can only be imported one time. Currently exercises can not be updated. So make sure the directory contains all the necessary files.
* You can import grades from a csv file of the following format:
```
<Last Name>_<First Name>_<First Name><Last Name>_<Matriculation Number>;<Grade>|<Remarks>
```
Here are a couple of sample entries:
```
Doe_John_JohnDoe_123456789;12; well Done
Doe_Jane_JaneDoe_987654321;---;-- keine Bemerkung --
```
* Exporting produces a csv formatted file as described above

## Warning
Nearly no error checking is done. Please make sure the grades you import are correctly formatted and that the files you place inside `corrector/data` follow the scheme of files that are downloaded from ILIAS when using the function to download all submissions in a single archive.
You are advised to inspect the code yourself before actually using it.

## License
This is published under the MIT license. This means it is published as is with absolutely no guarantees
