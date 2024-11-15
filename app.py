from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import face_recognition
import pickle

app = Flask(__name__, template_folder='templates')

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle adding a criminal
@app.route('/add_criminal', methods=['POST'])
def add_criminal():
    name = request.form['name']
    age = request.form['age']
    city = request.form['city']
    image_files = request.files.getlist('images')

    conn = sqlite3.connect('criminal.db')
    cursor = conn.cursor()

    try:
        # Insert the new criminal's details (name, age, city)
        cursor.execute('''
        INSERT INTO known_faces (name, age, city) VALUES (?, ?, ?)
        ''', (name, age, city))

        person_id = cursor.lastrowid  # Get the last inserted row ID

        # Track if any encodings were added
        encoding_added = False

        for image_file in image_files:
            try:
                # Load image and convert to RGB
                image = face_recognition.load_image_file(image_file)
                encodings = face_recognition.face_encodings(image)

                for encoding in encodings:
                    # Insert each encoding into the face_encodings table, linked to the person_id
                    cursor.execute('''
                    INSERT INTO face_encodings (person_id, encoding) VALUES (?, ?)
                    ''', (person_id, pickle.dumps(encoding)))
                    encoding_added = True

            except Exception as e:
                print(f"Error processing image {image_file.filename}: {e}")

        if not encoding_added:
            print("No valid face encodings found for the provided images.")

    except Exception as e:
        print(f"Error adding criminal details to the database: {e}")

    finally:
        # Commit the changes and close the connection
        conn.commit()
        conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
