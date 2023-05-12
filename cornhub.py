import flask, sqlite3
from flask import Flask, url_for, render_template, request


app = Flask(__name__,static_url_path='/static')

connection = sqlite3.connect("cornhub.db",check_same_thread=False)

qcorn,qcorndog,qbiofuel,qcornseeds,qbuttercorn,qcorncake,qstarch,qpopcorn,qunicorn = 0,0,0,0,0,0,0,0,0

megalist = []

def linearSearch(Arr,Value):
    if Arr==[]:
        return -1
    index = 0
    while Arr[index][0] != Value:
        index += 1
        if index==len(Arr):
            return -1
    return index

@app.route("/cornhub/")
def home():
    return render_template("cornhub.html")

@app.route("/cornhub/ourproducts", methods = ["GET","POST"])
def ourproducts():
    global qcorn,qcorndog,qbiofuel,qcornseeds,qbuttercorn,qcorncake,qstarch,qpopcorn,qunicorn
    if request.method == "GET":
        return render_template("ourproducts.html")
    
    elif request.method =="POST":  
        if "qcorn" in request.form:
            try:    
                qcorn += int(request.form["qcorn"])
                if linearSearch(megalist,'corn')==-1:
                    megalist.append(['corn',qcorn,round(int(qcorn)*float(0.60),2)])
                else:
                    index=linearSearch(megalist,'corn')
                    megalist[index] = ['corn',qcorn,round(int(qcorn)*float(0.60),2)]
            except:
                pass
            
        
        if "qcorndog" in request.form:
            try:
                qcorndog += int(request.form["qcorndog"])
                if 'corndog' not in megalist:
                    megalist.append(['corndog',qcorndog,int(qcorndog)*float(2.00)])
                else:
                    index=linearSearch(megalist,'corndog')
                    megalist[index] = ['corndog',qcorndog,int(qcorndog)*float(2.00)]
            except:
                pass
            
        
       
        if "qbiofuel" in request.form:
            try:
                qbiofuel += int(request.form["qbiofuel"])
                if 'biofuel' not in megalist:
                    megalist.append(['biofuel',qbiofuel,int(qbiofuel)*float(20.00)])
                else:
                    index=linearSearch(megalist,'biofuel')
                    megalist[index] = ['biofuel',qbiofuel,int(qbiofuel)*float(20.00)]
            except:
                pass
            
            
        if "qcornseeds" in request.form:
            try:
                qcornseeds += int(request.form["qcornseeds"])
                if 'cornseeds' not in megalist:
                    megalist.append(['cornseeds',qcornseeds,int(qcornseeds)*float(1.00)])
                else:
                    index=linearSearch(megalist,'cornseeds')
                    megalist[index] = ['cornseeds',qcornseeds,int(qcornseeds)*float(1.00)]
            except:
                pass
            
       
        if "qbuttercorn" in request.form:
            try:
                qbuttercorn += int(request.form["qbuttercorn"])
                if 'buttercorn' not in megalist:
                    megalist.append(['buttercorn',qbuttercorn,round(int(qbuttercorn)*float(1.20),2)])
                else:
                    index=linearSearch(megalist,'buttercorn')
                    megalist[index] = ['buttercorn',qbuttercorn,round(int(qbuttercorn)*float(1.20),2)]
            except:
                pass
            
                
            
        if "qcorncake" in request.form:
            try:
                qcorncake += int(request.form["qcorncake"])
                if 'corncake'not in megalist:
                    megalist.append(['corncake',qcorncake,int(qcorncake)*float(6.00)])
                else:
                    index=linearSearch(megalist,'corncake')
                    megalist[index] = ['corncake',qcorncake,int(qcorncake)*float(6.00)]
            except:
                pass
            
        
       
        if "qstarch" in request.form:
            try:
                qstarch += int(request.form["qstarch"])
                if 'starch' not in megalist:
                    megalist.append(['starch',qstarch,int(qstarch)*float(3.00)])
                else:
                    index=linearSearch(megalist,'starch')
                    megalist[index] = ['starch',qstarch,int(qstarch)*float(3.00)]
            except:
                pass
        
            
        if "qpopcorn" in request.form:
            try:
                qpopcorn += int(request.form["qpopcorn"])
                if 'popcorn' not in megalist:
                    megalist.append(['popcorn',qpopcorn,int(qpopcorn)*float(4.00)])
                else:
                    index=linearSearch(megalist,'popcorn')
                    megalist[index] = ['popcorn',qpopcorn,int(qpopcorn)*float(4.00)]
            except:
                pass
            
        
        if "qunicorn" in request.form:
            try:
                qunicorn += int(request.form["qunicorn"])
                if 'unicorn' not in megalist:
                    megalist.append(['unicorn',qunicorn,int(qunicorn)*float(4.00)])
                else:
                    index=linearSearch(megalist,'unicorn')
                    megalist[index] = ['unicorn',qunicorn,int(qunicorn)*float(4.00)]
            except:
                pass
            
        
        return render_template("ourproducts.html")    

            
@app.route("/cornhub/shoppingcart", methods = ["GET","POST"])
def shoppingcart():
    global receipt
    total_price = 0
    cursor = connection.execute("SELECT MAX(ReceiptID) FROM Cornhub")
    fetch = cursor.fetchone()
    receipt = fetch[0]
    if receipt is None:
        ReceiptID = 1
    else:
        ReceiptID = int(receipt) + 1
    for alist in megalist:
        total_price += alist[2]
    if request.method=="GET":
        return render_template("shoppingcart.html",megalist = megalist, total_price = total_price, ReceiptID = ReceiptID)
    else:
        connection.execute("INSERT INTO Cornhub(ReceiptID,corn,corndog,biofuel,cornseeds,buttercorn,corncake,starch,popcorn,unicorn,total) VALUES(?,?,?,?,?,?,?,?,?,?,?)",(ReceiptID,qcorn,qcorndog,qbiofuel,qcornseeds,qbuttercorn,qcorncake,qstarch,qpopcorn,qunicorn,total_price))
        connection.commit()
        outfile=open('receipt.txt','w')
        outfile.write("Receipt\n")
        stbf="{:<20}{:<5}{:<8}\n"
        outfile.write(stbf.format('Item','Quantity','Price'))
        for alist in megalist:
            outfile.write(stbf.format(alist[0],alist[1],alist[2]))
        outfile.write('\n')
        outfile.write("Subtotal:"+str(total_price)+'\n')
        if "location" in request.form:
            outfile.write('\n')
            outfile.write("Thank you for ordering, please collect your order at "+request.form["location"])
        outfile.close()
        return render_template('thankyou.html')
    
@app.route("/cornhub/ourlocations")
def ourlocations():
    return render_template("ourlocations.html")

@app.route("/cornhub/supportus")
def supportus():
    return render_template("supportus.html")

@app.route("/cornhub/amogus")
def amogus():
    return render_template("amogus.html")


if __name__ == '__main__':
    app.run(port = 8000)
    

