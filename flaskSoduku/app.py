### AC3 function does not properly work with if not statement. AC3 needs to be revised.


import os
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify, make_response
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
app = Flask(__name__)
import math
import json
import random
from datetime import datetime

db = SQL("sqlite:///soduku.db")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = "70dafd277605675e135ff9e47251fc866ebab4dcbd341f572916b036d517900d"
app.jinja_env.autoescape = True

Session(app)

csrf = CSRFProtect(app)

if __name__ == "__main__":
    app.run(debug=True)



def probability():
    nums = [1, 0]
    probabilities = [(7/9), (8/9)]
    boolean = random.choices(nums, probabilities, k=1)[0]
    if boolean == 1:
        return True
    if boolean == 0:
        return False

TwoBox = {1: [(0, 0), (0, 1), (1, 0), (1, 1)],
2: [(2, 0), (3, 0), (2, 1), (3, 1)],
3: [(0, 2), (0, 3), (1, 2), (1, 3),],
4: [(2, 2), (2, 3), (3, 2), (3, 3)]}



ThreeBox = { 1: [(0, 0), (1, 0), (2, 0), (0, 1),(1, 1), (2, 1), (0, 2), (1, 2), (2, 2)],
 2: [(3, 0), (4, 0), (5, 0), (5, 1), (3,  1), (4, 1), (5, 2), (3, 2), (4, 2)],
 3: [(6, 0), (7, 0), (8, 0), (6, 1), (7, 1), (8, 1), (6, 2), (7, 2), (8, 2)],
 4: [(0, 3), (1, 4), (2, 3), (0, 4), (1, 3), (2, 4), (0, 5), (1, 5), (2, 5)],
 5: [(0, 6), (1, 6), (2, 6), (0, 7), (1, 7), (2, 7), (0, 8), (1, 8), (2, 8)],
 6: [(3, 3), (4, 3), (5, 3), (5, 4), (3, 4), (4, 4), (5, 5), (3, 5), (4, 5)],
 7: [(3, 6), (4, 6), (5, 6), (5, 7), (3, 7), (4, 7), (5, 8), (3, 8), (4, 8)],
 8: [(6, 3), (7, 3), (8, 3), (6, 4), (7,4), (8, 4), (6, 5), (7, 5), (8, 5)],
 9: [(6, 6), (7, 6), (8, 6), (6, 7), (7, 7), (8, 7), (6, 8), (7, 8), (8, 8)],
 }

vertical4 = [2]
vertical9 = [3, 6]
sides4 = [1]
sides9 = [2, 5]
FourBox = None
def horizontalConsistency(assignment):
    print(len(assignment.values()))
    print(assignment)
    for j in range(int(math.sqrt(len(assignment.values())))):
        list = []
        for i in range(int(math.sqrt(len(assignment.values())))):
            list.append(assignment[f"({i}, {j})"])
        if len(list) != len(set(list)):
            return False
        else: 
            return True
        
def verticalConsistency(assignment):
    
    for i in range(int(math.sqrt(len(assignment.values())))):
        list = []
        for j in range(int(math.sqrt(len(assignment.values())))):
            list.append(assignment[f"({i}, {j})"])
        if len(list) != len(set(list)):
            return False
    return True

def boxConsistency(assignment):
    if int(math.sqrt(len(assignment.values()))) == 9:
        box = ThreeBox
    else:
        box = TwoBox
    for i in range(1, (len(box) + 1)):
        list = []
        for value in box[i]:
            list.append(assignment[f"{value}"])
        if len(list) != len(set(list)):
            return False
    return True


def consistency(assignment):
    if horizontalConsistency(assignment) and verticalConsistency(assignment) and boxConsistency(assignment):
        return True
    else:
        False

class soduku():
    def __init__(self, type):
        self.variables = set()
        for i in range(type):
            for j in range(type):
                self.variables.add((i,j))
        self.length = type + 1
        self.height = type + 1
        self.type = type
        self.nums = range(1, ((type ** 2) + 1))
        ### Remember to fix this logic right here
        if type == 16:
            self.box = FourBox
            self.boxNum = 17
            self.boxHeight = 4
        elif type == 9:
            self.box = ThreeBox
            self.boxHeight = 3
            self.boxNum = 10
        elif type == 4:
            self.boxHeight = 2
            self.boxNum = 5
            self.box = TwoBox


class sodukuCreator():
    def __init__(self, soduku):
        self.soduku = soduku

        self.domains = {}
        for var in self.soduku.variables:
            self.domains[var] = []
            for num in range(1, self.soduku.height):
                self.domains[var].append(num)
            random.shuffle(self.domains[var])
        self.base = list(range(1, self.soduku.height))
        self.playerBoard = self.solve()
        self.incomplete = self.unsolve(self.playerBoard)

    #Checks each column is arc consistent
    def verticalCheck(self, var, assignment):
        i, j = var
        list = []
        revised = True
        # For value in column if value is equal to another value in the column return False
        for s in range(self.soduku.type):
            if (i, s) in assignment.keys():
                list.append(assignment[i,s])
                if assignment[i,s] in self.domains[var]:
                    self.domains[var].remove(assignment[i, s])
        if (self.soduku.type - len(list)) < len(self.domains[var]):
            revised = False
        return revised
    
    def assignment_complete(self, assignment):
        if len(assignment.keys()) == (self.soduku.type ** 2):
           return True
        return False

    def random_var(self, assignment):
        count = math.inf
        matches = []
        for var in self.soduku.variables:
            if var not in assignment.keys():
                if len(self.domains[var]) < count:
                    matches.clear()
                    matches.append(var)
                    count = len(self.domains[var])
                elif len(self.domains[var]) == count:
                    matches.append(var)
        return random.choice(matches)
 
    def assignmentConvert(self, assignment):
        new = dict()
        print(assignment)
        for i in range(self.soduku.type):
            new[i] = dict()
        for key in assignment:
            i, j = key
            new[i][j] = assignment[key]
        return new


    def printAssignment(self, assignment):
        print("Board: ")
        for i in range(self.soduku.type):
            for j in range(self.soduku.type):
                if (i, j) in assignment.keys():
                    print(f"{assignment[i, j]}",end="")
                else:
                    print(" ",end="")
            print()
        print()
        print()

    def verticalConsistency(self, assignment, var):
        i, j = var
        list = []
        for s in range(self.soduku.type):
            if (i, s) in assignment.keys():
                list.append(assignment[i, s])
        if len(list) != len(set(list)):
            return False
        else:
            return True
            


    def horizontalConsistency(self, assignment, var):
        i, j = var
        list = []
        for s in range(self.soduku.type):
            if (s, j) in assignment.keys():
                list.append(assignment[s, j])
        if len(list) != len(set(list)):
            return False
        else:
            return True
    
    def boxConsistency(self, assignment, var):
        l = 0
        list = []
        for box in self.soduku.box: 
            if var in self.soduku.box[box]:
                l = box
        for var in self.soduku.box[l]:
            if var in assignment:
                list.append(assignment[var])
        if len(list) != len(set(list)):
            return False
        else:
            return True
            

    
    def consistency(self, assignment, var):
        if self.verticalConsistency(assignment, var) and self.horizontalConsistency(assignment, var) and self.boxConsistency(assignment, var):
            return True
        else:
            return False
    
    # Checks each row is arc consistent
    def horizontalCheck(self, var, assignment):
        i, j = var
        list = []
        revised = True
        # For value in row if value is equal to another value in the column return False
        for s in range(self.soduku.type):
            if (s, j) in assignment.keys():
                list.append(assignment[s, j])
                if assignment[s, j] in self.domains[var]:
                    self.domains[var].remove(assignment[s, j])
        if (self.soduku.type - len(list)) < len(self.domains[var]):
            revised = False
        return revised

    def boxCheck(self, var, assignment):
        l = 0
        list = []
        revised = True
        for key in self.soduku.box.keys():
            if var in self.soduku.box[key]:
                l = key
                break

        for slot in self.soduku.box[l]:
            if slot in assignment.keys():
                list.append(assignment[slot])
                if assignment[slot] in self.domains[var]:
                    self.domains[var].remove(assignment[slot])
        if (self.soduku.type - len(list)) < len(self.domains[var]):
            revised = False

        return revised

    def inferences(self, assignment):
        fh = []
        for var in self.soduku.variables:
            if len(self.domains[var]) == 1 and var not in assignment.keys():
                assignment[var] = self.domains[var][0]
                fh.append(var)
        
        return assignment, fh


    def revise(self, var, assignment):
        if self.verticalCheck(var, assignment) and self.horizontalCheck(var, assignment) and self.boxCheck(var, assignment):
            return True
        else:
            return False
            


    def reset(self):
        for var in self.soduku.variables:
            self.domains[var] = list(range(1, self.soduku.height))
            random.shuffle(self.domains[var])
    def properReset(self, prev):
        for var in prev:
            self.domains[var] = prev[var]


    def ac3(self, assignment):
        for var in self.soduku.variables:
            if var not in assignment.keys():
                if not self.revise(var, assignment):
                    return False
        return True

    def consistent(self, assignment, var):
        if self.ac3(assignment):
            return True

        return False

    def backtrack(self, assignment):
        if self.assignment_complete(assignment):
            self.printAssignment(assignment)
            for var in self.soduku.variables:
                print(var)
                if not self.consistency(assignment, var):
                    raise ValueError
            return assignment
        var = self.random_var(assignment)
        list = self.domains[var]
        for value in list:
            test = assignment.copy()
            test[var] = value
            if self.ac3(test):
                assignment[var] = value
                assignment, fh = self.inferences(assignment)
                self.ac3(assignment)
                new = self.backtrack(assignment)
                if new is not None:
                    return assignment
                else:
                    del assignment[var]
                    for val in fh:
                        del assignment[val]
            self.reset()
        return None


    def solve(self):
        return self.backtrack(dict())

    def unsolve(self, complete):
        use = complete.copy()
        for box in range(1, self.soduku.boxNum):
            for var in self.soduku.box[box]:
                if probability():
                    del use[var]
        return use


        



today = sodukuCreator(soduku(4))
playerboard = today.incomplete

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html" )
    else:
        if "4" in request.form:
            primary = sodukuCreator(soduku(4))
            return render_template("sodukuPage.html", playerBoard = primary.incomplete, cols=range(4), rows=range(4), vertical=vertical4, sides=sides4, max=4)
        else: 
            primary = sodukuCreator(soduku(9))
            return render_template("sodukuPage.html", playerBoard = primary.incomplete, cols=range(9), rows=range(9), vertical=vertical9, sides=sides9, max=9)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = db.execute("SELECT * FROM users")
        if user["password"] != password:
            return ValueError
            
        return render_template("index.html")

    else:
        return render_template("login.html")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if password != confirmation:
            placeholder = 0 #!!!!!!!!
        password = generate_password_hash(password)
        db.execute("INSERT INTO users (username, email, password) Values(?,?,?) ", username, email, password)
        return redirect("index.html")
    else: 
        return render_template("register.html")
    
@app.route("/sodukuPage", methods=["POST"])
def sodukuPage():
    req = request.get_json()
    print(req)
    checkVars = req["checkVars"]
    print(checkVars)
    board = {}
    if consistency(checkVars):
        res = make_response(jsonify({
                "code": "green"
        }), 200)
        return res
    else:
        res = make_response(jsonify({
            "code": "red"
        }), 200)
        return res