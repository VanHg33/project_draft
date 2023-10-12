from flask import Flask, jsonify, render_template

import pandas as pd
import numpy as np

import sqlite3


conn = sqlite3.connect("JSearchdata.sqlite")

# Check to see if the connection to db is successful.
test_df = pd.read_sql('SELECT * FROM json_data', conn)
print("\n================== CHECK ==========================\n")
print(test_df.head(2))
print("\n===================================================\n")


#Create an app
app = Flask(__name__)

#Define routes
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/map")
def map():
    return render_template("map.html")

@app.route("/employment")
def employment():
    return render_template("employment.html")



@app.route("/api/city_count")
def city_count():
    print("\n================== /api/city_count ==========================\n")
    
    conn = sqlite3.connect("JSearchdata.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT job_city, COUNT(*) as count FROM json_data GROUP BY job_city")
    
    # Fetch all the data
    results = cursor.fetchall()
    # Close the database connection
    conn.close()
    
    print("\n================== city count ==========================\n")
    print(results)
    print("\n===================================================\n")

    data = []
    
    for result in results:
        row = {
            'city': result[0],
            'count': result[1]
        }
        
        data.append(row)
    
    return jsonify(data)

@app.route("/api/job_category/<job_city>")
def job_category(job_city=None):
    print("\n================== /api/job_category/<job_city> ==========================\n")
    
    conn = sqlite3.connect("JSearchdata.sqlite")
    cursor = conn.cursor()
    
    sql_string = f"SELECT job_employment_type, count(*) FROM json_data where job_city='{job_city}' group by job_employment_type"
    cursor.execute(sql_string)

    # Fetch all the data
    results = cursor.fetchall()
    # Close the database connection
    conn.close()
    
    print("\n================== job type count ==========================\n")
    print(results)
    print("\n===================================================\n")

    data = []
    
    for result in results:
        row = {
            'title': result[7],
            'count': result[1]
        }
        
        data.append(row)
    
    return jsonify(data)

@app.route("/api/job_info/<job_city>")
def job_info(job_city=None):
    print("\n================== /api/job_info/<job_city> ==========================\n")
    
    conn = sqlite3.connect("JSearchdata.sqlite")
    cursor = conn.cursor()
    
    sql_string = f"SELECT * FROM json_data where job_city='{job_city}'"
    cursor.execute(sql_string)

    # Fetch all the data
    results = cursor.fetchall()
    # Close the database connection
    conn.close()
    
    print("\n================== detail ==========================\n")
    print(results)
    print("\n===================================================\n")

    data = []
    
    for result in results:
        row = {
            'Company_Name': result[1],
            'Job_Title': result[4],
            'Job_Apply_Link': result[5],
            'Job_Type': result[3],
            'Job_State': result[7],
            'Job_Description': result[6]
            
        }
        
        data.append(row)
    
    return jsonify(data)

@app.route("/api/mapping")
def mapping():
    print("\n================== /api/map ==========================\n")
    
    conn = sqlite3.connect("JSearchdata.sqlite")
    cursor = conn.cursor()
    
    sql_string = f"SELECT job_city, COUNT(*) as count, job_latitude, job_longitude FROM json_data GROUP BY job_city"
    cursor.execute(sql_string)

    # Fetch all the data
    results = cursor.fetchall()
    # Close the database connection
    conn.close()
    
    print("\n================== city_count ==========================\n")
    print(results)
    print("\n===================================================\n")

    data = []
    
    for result in results:
        row = {
            'city': result[7],
            'count': result[1],
            'latitude': result[9],
            'longitude': result[10]
        }
        
        data.append(row)
    
    return jsonify(data)











# # Define a route to retrieve data with state and job employment type information
# @app.route("/employment")
# def get_data():
#     try:
#         # # Connect to the SQLite database
#         conn = sqlite3.connect('JSearchdata.sqlite')  # Updated with the correct database file name
#         cursor = conn.cursor()

#         # Execute a query to retrieve data with state and job employment type information
#         cursor.execute("SELECT job_state, job_employment_type, COUNT(*) FROM json_data GROUP BY job_state, job_employment_type")

#         # Fetch all the data
#         data = cursor.fetchall()

#         # Close the database connection
#         conn.close()

#         # Prepare data for sending as JSON
#         result = [{'state': row[0], 'employment_type': row[1], 'count': row[2]} for row in data]

#         return jsonify(result)

#     except Exception as e:
#         return jsonify({'error': str(e)})



# Define the first API route to get all rows from the "jobs" table
# @app.route('/api/v1.0/jobs')
# def get_jobs():
#     # Create a database engine
#     engine = create_engine()

#     # Query the "jobs" table and load the results into a Pandas DataFrame
#     df = pd.read_sql_table('jobs', engine)

#     # Convert the DataFrame to a JSON object and return it
#     return jsonify(df.to_dict(orient='records'))


# @app.route("/api/v1.0/employment")
# def stations():
#     companies = session.query(data.employment_name).all()
#     result_comp = list(np.ravel(companies))
#     session.close()
#     return jsonify(result_comp)

# @app.route("/api/v1.0/education")







# @app.route("/api/v1.0/companies")
# def stations():
#     companies = session.query(data.employment_name).all()
#     result_comp = list(np.ravel(companies))
#     session.close()
#     return jsonify(result_comp)






if __name__ == '__main__':
    app.run(debug=True)

