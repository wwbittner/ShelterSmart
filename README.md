### ShelterSmart ###
ShelterSmart is a database app to help animal shelters manage the animals now and previously under their care.

### Features ###
- A database and display of animals at your shelter, adopted animals, and deleted animals (like a Recycle Bin)
- Add and delete animals at the click of a button
- Register adoptions and store the name and contact info of adopters
- Automatically determine needed vaccines

### Technologies Used ###
Languages: Python, HTML, CSS
Libraries: Flask, SQLite3
Database: SQLite

### Installation

1. Download and extract the project folder.
2. Open a terminal and navigate to the directory containing the application files.
3. Run the following command: pip install Flask.
4. Initialize the database. If you see a file called "shelter.db," then no initialization needed. If you don't, or if you want to delete and reset the database, then open "reset_shelter_database.py" and run it. This will create the database.
5. Run "app.py" and use your web browser to open the local address displayed in the terminal.

### Future Improvements ###
1. Allow user to export database to Excel using the pandas library.
2. Allow user to manage employees/volunteers as well as animals - e.g., shift scheduling, leave requests, etc.

### Author ###
Made by me, William Bittner

If you have any questions, suggestions, or issues while using ShelterSmart, shoot me an email at anationoverwatch@gmail.com and I will do my best to help!

### License ###

MIT License

Copyright (c) [2026] [William Bittner]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
