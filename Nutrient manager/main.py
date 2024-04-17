from flask import Flask, render_template, request, redirect, url_for
import csv, sqlite3

def read_csv(filename):
    with open(filename, 'r') as file:    
        reader = csv.reader(file)
        next(reader)
        recs = []
        for row in reader:
            recs.append(row)
        return recs

def create_plan():
  conn = sqlite3.connect('nutri.db')
  conn.execute('''CREATE TABLE IF NOT EXISTS plan(
              rid INTEGER PRIMARY KEY,
              grams INTEGER,
              FOREIGN KEY(`rid`) REFERENCES `info`(`rid`));''')
  conn.commit()
  conn.close()
  
def display_data():
  conn = sqlite3.connect('nutri.db')
  cur = conn.cursor()
  cur.execute("SELECT * FROM plan;")
  rows = cur.fetchall() 
  conn.close()
  return rows



  
# main
create_plan()

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def home():
  if request.method == 'POST':
      rid = request.form['rid']
      grams = request.form['grams']
      conn = sqlite3.connect('nutri.db')
      cur = conn.cursor()
      cur.execute("INSERT INTO plan(rid, grams) VALUES(?, ?);", (rid, grams))
      conn.commit()
      conn.close()
  recs = display_data()
  kcal = request.args.get('kcal')
  protein = request.args.get('protein')
  sugars = request.args.get('sugars')
  fats = request.args.get('fats')
  carbs = request.args.get('carbs')
  return render_template('index.html', recs=recs, kcal=kcal, protein=protein, sugars=sugars, fats=fats, carbs=carbs)

@app.route('/delete', methods = ['POST'])
def delete():
  conn = sqlite3.connect('nutri.db')
  cur = conn.cursor()
  cur.execute("DELETE FROM plan")
  conn.commit()
  conn.close()
  return render_template('index.html')

@app.route('/calk', methods = ['POST'])
def calk():
      conn = sqlite3.connect('nutri.db')
      cur = conn.cursor()
      cur.execute('''SELECT SUM(info.k * plan.grams)
                    FROM info
                    INNER JOIN plan ON info.rid = plan.rid''')
      kcal = cur.fetchone()[0]
      conn.close()
      conn = sqlite3.connect('nutri.db')
      cur = conn.cursor()
      cur.execute('''SELECT SUM(info.p * plan.grams)
                    FROM info
                    INNER JOIN plan ON info.rid = plan.rid''')
      protein = cur.fetchone()[0]
      conn.close()
      conn = sqlite3.connect('nutri.db')
      cur = conn.cursor()
      cur.execute('''SELECT SUM(info.f * plan.grams)
                    FROM info
                    INNER JOIN plan ON info.rid = plan.rid''')
      fats = cur.fetchone()[0]
      conn.close()
      conn = sqlite3.connect('nutri.db')
      cur = conn.cursor()
      cur.execute('''SELECT SUM(info.s * plan.grams)
                    FROM info
                    INNER JOIN plan ON info.rid = plan.rid''')
      sugars = cur.fetchone()[0]
      conn.close()
      conn = sqlite3.connect('nutri.db')
      cur = conn.cursor()
      cur.execute('''SELECT SUM(info.c * plan.grams)
                    FROM info
                    INNER JOIN plan ON info.rid = plan.rid''')
      carbs = cur.fetchone()[0]
      conn.close()
      return redirect(url_for('home', kcal=kcal, protein=protein, sugars=sugars, fats=fats, carbs=carbs))


    


app.run()

