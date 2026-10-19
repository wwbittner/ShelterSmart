from flask import *     # Flask is the module that allows us to connect Python to HTML. Sort of like a little fake web browser.
import sqlite3      # sqlite3 is the module that allows us to manipulate an SQL (well, a pseudo-SQL) database from Python.

app = Flask(__name__)   #This is a required bit of code that Flask needs to run properly. It sets the name of our app equal to the name of the Python file, I think.

def get_db_connection():    #This function is how we connect to our SQLite database. By making it a function, we can make our code shorter later on by just calling the function instead of typing out all three rows.
    conn = sqlite3.connect("shelter.db")    #shelter.db is the SQLite file that holds all of our tables, such as animals, deleted_animals, and adopted_animals.
    conn.row_factory = sqlite3.Row
    return conn

### Routes to different places on the website ###
@app.route("/")     #This takes you back to the home page. @app.route() runs the following function automatically whenever the "/" address is called in HTML.
def home_page():
    ###
    return(go_to_animal_database())         ### Use this if you want the home page to be the animal database ###
    # return render_template("home_page.html")    ### Use this if you want the home page to be the "Home Page" screen where you choose "Animal Management" or some other tool ###
    ###

@app.route("/go_to_animal_database")    # This takes you to the page with the spreadsheet showing animals currently at the shelter.
def go_to_animal_database():
    conn = get_db_connection()      # This is an example of calling the function to set up our connection instead of having to rewrite lines 7-9.
    animals = conn.execute("SELECT * FROM animals").fetchall()      # This is how we query our SQLite database. Here, we select the whole animals table so we can put it in the spreadsheet display.
    conn.close()    # This just closes the connection to the database. It's good practice to always close your connection when finished.
    return render_template("animal_database.html", animals=animals)     # This displays our spreadsheet page. The animals=animals tells the HTML file what to use as data in the spreadsheet.

@app.route("/go_to_add_animal", methods=["POST"])   # Takes you to the screen where you enter a new dog or cat.
def go_to_add_animal():
    return render_template("add_animal.html")

@app.route("/go_to_edit_animal/<int:id_to_edit>", methods=["GET"])  # Takes you to the screen where you edit an existing dog or cat.
def go_to_edit_animal(id_to_edit):

    conn = get_db_connection()

    animal_to_edit = conn.execute("SELECT * FROM animals WHERE id=?", (id_to_edit,)).fetchone()     # Using the animal's id, which we get from the HTML file (it knows the id in each row because it displays it!), we select the matching row from the SQLite database.

    # This is my roundabout way to turn the data in the SQLite table, which includes vaccines still needed, into a list of vaccines RECEIVED, which we then use to autocheck the appropriate "Vaccines Received" boxes.
    vaccines_needed = animal_to_edit["vaccines_needed"].split(", ")
    dapp_received = "DAPP/DHPP" not in vaccines_needed and animal_to_edit["species"] == "Dog"
    bord_received = "Bordetella" not in vaccines_needed and animal_to_edit["species"] == "Dog"
    rabies_received = "Rabies" not in vaccines_needed
    fvrcp_received = "FVRCP" not in vaccines_needed and animal_to_edit["species"] == "Cat"
    felv_received = "FeLV" not in vaccines_needed and animal_to_edit["species"] == "Cat"

    conn.close()

    # This line displays the page to edit an animal's details. I include all these x=y statements because they allow the HTML file to access the data stored in the row being edited, which allows us to prefill the input boxes in the webpage.
    return render_template("edit_animal.html", animal_to_edit=animal_to_edit, dapp_received = dapp_received, bord_received = bord_received,
                           rabies_received = rabies_received, fvrcp_received=fvrcp_received, felv_received=felv_received)

@app.route("/go_to_deleted_animal_database", methods=["POST"]) #Takes you to the screen where you can view animals deleted from the main spreadsheet (sort of a Recyle Bin).
def go_to_deleted_animal_database():
    conn = get_db_connection()
    deleted_animals = conn.execute("SELECT * FROM deleted_animals").fetchall()
    conn.close()
    return render_template("deleted_animals_database.html", deleted_animals=deleted_animals)

@app.route("/go_to_adopt_animal/<int:id_to_adopt>", methods=["GET"])
def go_to_adopt_animal(id_to_adopt):
    conn = get_db_connection()

    animal_to_adopt = conn.execute("SELECT * FROM animals WHERE id=?", (id_to_adopt,)).fetchone()
    conn.close()
    return render_template("adopt_animal.html", animal_to_adopt=animal_to_adopt)

@app.route("/go_to_adopted_animal_database", methods=["POST"])
def go_to_adopted_animal_database():
    conn = get_db_connection()
    adopted_animals = conn.execute("SELECT * FROM adopted_animals").fetchall()
    conn.close()
    return render_template("adopted_animals_database.html", adopted_animals=adopted_animals)

### Routes that perform actions with the data ###
@app.route("/add_animal", methods=["POST"])     # This code is what will actually update the SQLite database of animals when the user clicks "Submit" on the add_animal page.
def add_animal():
    conn = get_db_connection()

    animal_name = request.form["animal_name"]       # request.form lets us get a value from the html file (say, what the user typed) and assign it to a Python variable.
    animal_species = request.form.get("animal_species")     # Sometimes I have to use .get() and I honestly couldn't tell you why.
    animal_breed = request.form["animal_breed"]
    animal_sex = request.form.get("animal_sex")
    animal_age = request.form["animal_age"]
    animal_status = request.form["animal_status"]
    spay_neuter = request.form.get("spay_neuter")
    date_arrived = request.form["date_arrived"]
    how_acquired = request.form["how_acquired"]
    
    vaccines_received = request.form.getlist("vaccines_received")   # This code chunk takes the list of vaccines the user marked as "received" and turns it into a list of vaccines the animal still needs.
    cat_vaccines = ["Rabies", "FVRCP", "FeLV"]      # Some vaccines are only for cats or dogs, so we want to make sure not to mark a vaccine as needed by one if the reason the user didn't mark it "Received" is because it is only for the other species!
    dog_vaccines = ["DAPP/DHPP", "Bordetella", "Rabies"]
    if animal_species == "Dog":
        vaccines_needed = list(set(dog_vaccines) - set(vaccines_received))
        vaccines_needed = ", ".join(vaccines_needed)
    elif animal_species == "Cat":
        vaccines_needed = list(set(cat_vaccines) - set(vaccines_received))
        vaccines_needed = ", ".join(vaccines_needed)
    else:
        vaccines_needed = "See Notes"   # The user needs to manually type the vaccine history of any other species.
    
    medical_conditions = request.form["medical_conditions"]
    animal_location = request.form["animal_location"]
    animal_sponsored = request.form["animal_sponsored"]
    animal_notes = request.form["animal_notes"]

    conn.execute("""INSERT INTO animals (name, species, breed, sex, age, status, spay_neuter, date_arrived, how_acquired, 
        vaccines_needed, medical_conditions, location, sponsored, notes)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (animal_name, animal_species, animal_breed, animal_sex, animal_age, animal_status, spay_neuter, date_arrived, how_acquired,
         vaccines_needed, medical_conditions, animal_location, animal_sponsored, animal_notes))
    # Using the (?,?,?), (x,y,z) method of assigning values is just an SQLite best practice.

    conn.commit()

    animals = conn.execute("""SELECT * FROM animals""").fetchall()
    conn.close()
    return render_template("animal_database.html", animals=animals)

@app.route("/edit_animal", methods=["POST"])
def edit_animal():      # This code lets the user modify the details of a selected animal. It works very similar to add_animal.
    conn = get_db_connection()

    id_to_edit = request.form["id_to_edit"]

    animal_name = request.form["animal_name"]
    animal_species = request.form.get("animal_species")
    animal_breed = request.form["animal_breed"]
    animal_sex = request.form.get("animal_sex")
    animal_age = request.form["animal_age"]
    animal_status = request.form["animal_status"]
    spay_neuter = request.form.get("spay_neuter")
    date_arrived = request.form["date_arrived"]
    how_acquired = request.form["how_acquired"]
    
    vaccines_received = request.form.getlist("vaccines_received")
    cat_vaccines = ["Rabies", "FVRCP", "FeLV"]
    dog_vaccines = ["DAPP/DHPP", "Bordetella", "Rabies"]
    if animal_species == "Dog":
        vaccines_needed = list(set(dog_vaccines) - set(vaccines_received))
        vaccines_needed = ", ".join(vaccines_needed)
    elif animal_species == "Cat":
        vaccines_needed = list(set(cat_vaccines) - set(vaccines_received))
        vaccines_needed = ", ".join(vaccines_needed)
    else:
        vaccines_needed = "See Notes"
    
    medical_conditions = request.form["medical_conditions"]
    animal_location = request.form["animal_location"]
    animal_sponsored = request.form["animal_sponsored"]
    animal_notes = request.form["animal_notes"]

    # This code block is the main difference from add_animal. We simply modify a row instead of creating one, and COALESCE allows us to fill in only the cells that we actually want to edit, so that when we edit some details and leave others blank the blank "inputs" won't override previous data in the SQLite database. Technically this is redundant because we autofill all the input boxes with the previous data anyway.
    conn.execute("""UPDATE animals
        SET name = COALESCE(NULLIF(?, ''), name),
        species = COALESCE(NULLIF(?, ''), species),
        breed = COALESCE(NULLIF(?, ''), breed),
        sex = COALESCE(NULLIF(?, ''), sex),
        age = COALESCE(NULLIF(?, ''), age),
        status = COALESCE(NULLIF(?, ''), status),
        spay_neuter = COALESCE(NULLIF(?, ''), spay_neuter),
        date_arrived = COALESCE(NULLIF(?, ''), date_arrived),
        how_acquired = COALESCE(NULLIF(?, ''), how_acquired),
        vaccines_needed = COALESCE(NULLIF(?, ''), vaccines_needed),
        medical_conditions = COALESCE(NULLIF(?, ''), medical_conditions),
        location = COALESCE(NULLIF(?, ''), location),
        sponsored = COALESCE(NULLIF(?, ''), sponsored),
        notes = COALESCE(NULLIF(?, ''), notes)
        WHERE id = ?""",
        (animal_name, animal_species, animal_breed, animal_sex, animal_age, animal_status, spay_neuter, date_arrived, how_acquired,
         vaccines_needed, medical_conditions, animal_location, animal_sponsored, animal_notes, id_to_edit))

    conn.commit()

    animals = conn.execute("""SELECT * FROM animals""").fetchall()
    conn.close()
    return render_template("animal_database.html", animals=animals)

@app.route("/adopt_animal", methods=["POST"])
def adopt_animal():
    conn = get_db_connection()

    id_to_adopt = request.form['id_to_adopt']

    animal_name = request.form["animal_name"]
    animal_species = request.form.get("animal_species")
    animal_breed = request.form["animal_breed"]
    animal_sex = request.form.get("animal_sex")
    animal_age = request.form["animal_age"]
    animal_status = request.form["animal_status"]
    spay_neuter = request.form.get("spay_neuter")
    date_arrived = request.form["date_arrived"]
    how_acquired = request.form["how_acquired"]
    
    vaccines_received = request.form.getlist("vaccines_received")
    cat_vaccines = ["Rabies", "FVRCP", "FeLV"]
    dog_vaccines = ["DAPP/DHPP", "Bordetella", "Rabies"]
    if animal_species == "Dog":
        vaccines_needed = list(set(dog_vaccines) - set(vaccines_received))
        vaccines_needed = ", ".join(vaccines_needed)
    elif animal_species == "Cat":
        vaccines_needed = list(set(cat_vaccines) - set(vaccines_received))
        vaccines_needed = ", ".join(vaccines_needed)
    else:
        vaccines_needed = "See Notes"
    
    medical_conditions = request.form["medical_conditions"]
    animal_location = request.form["animal_location"]
    animal_sponsored = request.form["animal_sponsored"]
    animal_notes = request.form["animal_notes"]

    adoption_date = request.form["adoption_date"]
    adopter_first_name = request.form["adopter_first_name"]
    adopter_last_name = request.form["adopter_last_name"]
    adopter_address = request.form["adopter_address"]
    adopter_phone = request.form["adopter_phone"]

    conn.execute("""INSERT INTO adopted_animals
        (id, name, species, breed, sex, age, status, spay_neuter, date_arrived, how_acquired, 
        vaccines_needed, medical_conditions, location, sponsored, notes, adoption_date, adopter_first_name, adopter_last_name,
        adopter_address, adopter_phone)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (id_to_adopt, animal_name, animal_species, animal_breed, animal_sex, animal_age, animal_status, spay_neuter, date_arrived, how_acquired,
         vaccines_needed, medical_conditions, animal_location, animal_sponsored, animal_notes, adoption_date, adopter_first_name,
          adopter_last_name, adopter_address, adopter_phone))

    conn.execute("""DELETE FROM animals WHERE id=?""", (id_to_adopt,))

    conn.commit()

    adopted_animals = conn.execute("""SELECT * FROM adopted_animals""").fetchall()
    conn.close()
    return render_template("adopted_animals_database.html", adopted_animals=adopted_animals)

@app.route("/delete_animal", methods=["POST"])      # This code lets the user delete an animal from the main spreadsheet.
def delete_animal():
    conn = get_db_connection()
    id_to_delete = request.form["id_to_delete"]

    conn.execute("""INSERT INTO deleted_animals 
        SELECT * FROM animals
        WHERE id=?""", (id_to_delete,))     # This code adds the about-to-be-deleted row to a backup SQLite table, which serves as a sort of Recycle Bin.

    conn.execute("""DELETE FROM animals WHERE id=?""", (id_to_delete,))

    conn.commit()

    animals = conn.execute("""SELECT * FROM animals""").fetchall()
    conn.close()
    return render_template("animal_database.html", animals=animals)

@app.route("/restore_deleted_animal", methods=["POST"])     # This code lets us return an animal from the Recycle Bin to the main spreadsheet. Basically the reverse of /delete_animal.
def restore_deleted_animal():
    conn = get_db_connection()
    id_to_restore = request.form["id_to_restore"]

    conn.execute("""INSERT INTO animals SELECT * FROM deleted_animals WHERE id=?""", (id_to_restore))
    conn.execute("DELETE FROM deleted_animals WHERE id=?", (id_to_restore))
    conn.commit()
    deleted_animals=conn.execute("SELECT * FROM deleted_animals").fetchall()
    conn.close()
    return render_template("deleted_animals_database.html", deleted_animals=deleted_animals)
    
@app.route("/perm_delete_animal", methods=["POST"])     # This code lets us remove an animal from the Recycle Bin, deleting it forever.
def perm_delete_animal():
    conn = get_db_connection()

    id_to_perm_delete = request.form["id_to_perm_delete"]

    conn.execute("""DELETE FROM deleted_animals WHERE id=?
        """, (id_to_perm_delete))
    conn.commit()
    deleted_animals=conn.execute("SELECT * FROM deleted_animals").fetchall()
    conn.close()
    return render_template("deleted_animals_database.html", deleted_animals = deleted_animals)

###
if __name__=="__main__":        # This is just standard code that allows you to launch the app directly from Python.
    app.run(debug=True)