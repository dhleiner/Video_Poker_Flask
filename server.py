from flask import Flask, request
import random
from flask_cors import CORS
 
app = Flask(__name__)
CORS(app)


class Card:
  def __init__(self, rank, suit):
    self.rank = rank
    self.suit = suit
  def toJSON(self):
    return {"rank":self.rank,"suit":self.suit}
@app.route("/draw",methods=["POST"])
def draw():
  oldCards=request.get_json()
  add_jokers=request.args.get("add_jokers",False)
  print(oldCards)
  Deck = range(1, 53)
  newDeck=[]
  remainingCards=[]
  r=0
  s=" "
  bet=4
 
  for n in Deck:
    if n >=1 and n <= 13:
      s="Spades"
    if n >=14 and n <= 26:
      s="Hearts"
    if n >=27 and n <= 39:
      s="Diamonds"
    if n >=40 and n <= 52:
      s="Clubs"

    if n%13==1:
      r="Ace"
    elif n%13==0:
      r="King"
    elif n%13==12:
      r="Queen"
        
    elif n%13==11:
      r="Jack"
    else:
      r=str(n%13)
        

    card1=Card(r,s)
    
    newDeck.append(card1.toJSON())
  if add_jokers:
    card1=Card("Joker1","Joker")
    card2=Card("Joker2","Joker")
    newDeck.append(card1.toJSON())
    newDeck.append(card2.toJSON())


  for card in newDeck:
    if not any(currentCard["rank"]==card["rank"] and currentCard["suit"]==card["suit"] for currentCard in oldCards):
      remainingCards.append(card)
    
  random.shuffle(remainingCards)    
  newCards=[]
  index=0
  for currentCard in oldCards:
    # print(index)
    # print(type(index))
    # print(currentCard)
    # print(type(currentCard))

    if currentCard["keep"]:
      newCards.append(currentCard)
    else:
      newCards.append(remainingCards[index])
      index=index+1

    
  print(newCards)
  hand=newCards
  return hand
  #hand=[Card("Ace","Clubs"),Card("10","Clubs"),Card("Jack","Clubs"),Card("Queen","Clubs"),Card("King","Clubs")]
@app.route("/calculate",methods=["POST"])
def calculate():
  handRank="NOTHING"
  data=request.get_json()
  hand=data["hand"]
  bet=data["bet"]
  #print(data)
  
  handCounter= {
  "Ace":0,
  "2":0,
  "3":0,
  "4":0,
  "5":0,
  "6":0,
  "7":0,
  "8":0,
  "9":0,
  "10":0,
  "Jack":0,
  "Queen":0,
  "King":0
  }

  for c in hand:
    handCounter[c["rank"]]=handCounter[c["rank"]]+1

 


  highStraight=False
  payout=-1
  v=list(handCounter.values())
  if v.count(1)>0:
    w=v.index(1)
  else:
    w=0
    highStraight=(handCounter["Ace"]==handCounter["10"]==handCounter["Jack"]==handCounter["Queen"]==handCounter["King"]==1) 
  isStraight=False

  if w<=8:

    isStraight=(v[w]==v[w+1]==v[w+2]==v[w+3]==v[w+4]) or highStraight
  

  isFlush=(hand[0]["suit"]==hand[1]["suit"]==hand[2]["suit"]==hand[3]["suit"]==hand[4]["suit"])

  if highStraight and isFlush:
    handRank="ROYAL FLUSH"
    payout=250
    if bet==5:
      payout=800
  
  
  
  elif isStraight and isFlush:
    handRank="STRAIGHT FLUSH"
    payout=50
  
  elif isStraight:
    handRank="STRAIGHT"
    payout=4
  
  elif isFlush:
    handRank="FLUSH"
    payout=6
  
  elif v.count(4)==1:
    handRank="FOUR OF A KIND"
    payout=25
  
  elif v.count(2)==1 and v.count(3)==1:
    handRank="FULL HOUSE"
    payout=9

  elif v.count(3)==1:
    handRank="THREE OF A KIND"
    payout=3

  elif v.count(2)==2:
    handRank="TWO PAIR"
    payout=2
  
  elif v[10]==2 or v[11]==2 or v[12]==2 or v[0]==2:
    handRank="JACKS OR BETTER"
    payout=1
  
 
 

  winnings=bet*payout*0.25
  print(handRank)
  print("Bet:",bet)
  print("You win:",winnings)
  return{"winnings":winnings,"handRank":handRank}  
@app.route("/create")
def create():
  add_jokers=request.args.get("add_jokers",False)
  # print(add_jokers)
  Deck = range(1, 53)
  newDeck=[]
  r=0
  s=" "
  
 
  for n in Deck:
    if n >=1 and n <= 13:
      s="Spades"
    if n >=14 and n <= 26:
      s="Hearts"
    if n >=27 and n <= 39:
      s="Diamonds"
    if n >=40 and n <= 52:
      s="Clubs"

    if n%13==1:
      r="Ace"
    elif n%13==0:
      r="King"
    elif n%13==12:
      r="Queen"
        
    elif n%13==11:
      r="Jack"
    else:
      r=str(n%13)
        

    card1=Card(r,s)
    
    newDeck.append(card1.toJSON())
    
  if add_jokers:
    card1=Card("Joker1","Joker")
    card2=Card("Joker2","Joker")
    newDeck.append(card1.toJSON())
    newDeck.append(card2.toJSON())

    

  print("The new deck is",newDeck)  
  random.shuffle(newDeck)

  return [newDeck.pop(),newDeck.pop(),newDeck.pop(),newDeck.pop(),newDeck.pop()] 

@app.route("/createJokers")
# def createJokers():
  
#   Deck = range(1, 55)
#   newDeck=[]
#   r=0
#   s=" "
  
 
#   for n in Deck:
#     if n >=1 and n <= 13:
#       s="Spades"
#     if n >=14 and n <= 26:
#       s="Hearts"
#     if n >=27 and n <= 39:
#       s="Diamonds"
#     if n >=40 and n <= 52:
#       s="Clubs"
#     if n==53 or n==54:
#       s="Joker"
#       r="Joker"


#     if n%13==1:
#       r="Ace"
#     elif n%13==0:
#       r="King"
#     elif n%13==12:
#       r="Queen"
        
#     elif n%13==11:
#       r="Jack"
#     else:
#       r=str(n%13)
        

#     card1=Card(r,s)
    
#     newDeck.append(card1.toJSON())
    


    

    
#   random.shuffle(newDeck)

#   return [newDeck.pop(),newDeck.pop(),newDeck.pop(),newDeck.pop(),newDeck.pop()] 
 


@app.route("/calculateLooseDeuces",methods=["POST"])
def calculateDeuces():
  data=request.get_json()
  hand=data["hand"]
  bet=data["bet"]
  payout=-1

  handCounter= {
    "Ace":0,
    "2":0,
    "3":0,
    "4":0,
    "5":0,
    "6":0,
    "7":0,
    "8":0,
    "9":0,
    "10":0,
    "Jack":0,
    "Queen":0,
    "King":0
  }

  suitCounter={
    "Clubs":0,
    "Diamonds":0,
    "Hearts":0,
    "Spades":0,
    "Wild":0
  }
 

 

  handRank="NOTHING"

  for c in hand:
    handCounter[c["rank"]]=handCounter[c["rank"]]+1
    if c["rank"]=="2":
  
      suitCounter["Wild"]=suitCounter["Wild"]+1
    else:
      suitCounter[c["suit"]]=suitCounter[c["suit"]]+1
 



  suits=list(suitCounter.values())
  suits.pop(4)
 
  v=list(handCounter.values())
  v.pop(1)

  if 1 in v:
    w=v.index(1)
 
  else:
    w=0



  highStraight=((handCounter["Ace"]+handCounter["10"]+handCounter["Jack"]+handCounter["Queen"]+handCounter["King"]+handCounter["2"]==5) and (handCounter["Ace"]<=1 and handCounter["10"]<=1 and handCounter["Jack"]<=1 and handCounter["Queen"]<=1 and handCounter["King"]<=1))
  isStraight=False

  if w<=7 and w>0:

     isStraight=((v[w]+v[w+1]+v[w+2]+v[w+3]+v[w+4]+handCounter["2"]==5) and (v[w]<=1 and v[w+1]<=1 and v[w+2]<=1 and v[w+3]<=1 and v[w+4]<=1)) or highStraight

  isFlush=(5-suitCounter["Wild"]) in suits

  if highStraight and isFlush and (handCounter["2"]==0):
    handRank="ROYAL FLUSH"
    payout=250
    if bet==5:
     payout=800
  
  elif handCounter["2"]==4:
    handRank="FOUR DEUCES"
    payout=500
  
  
  elif highStraight and isFlush and handCounter["2"]!=0:
    handRank="WILD ROYAL FLUSH"
    payout=25


  elif (5-handCounter["2"] in v):
    handRank="FIVE OF A KIND"
    payout=15

 
  elif isStraight and isFlush:
    handRank="STRAIGHT FLUSH"
    payout=8
 
  elif (4-handCounter["2"] in v):
    handRank="FOUR OF A KIND"
    payout=4
 
  elif isStraight or highStraight:
    handRank="STRAIGHT"
    payout=2
 
  elif isFlush:
    handRank="FLUSH"
    payout=2



  elif (v.count(2)==1 and v.count(3)==1 and handCounter["2"]==0) or (v.count(2)==2 and handCounter["2"]==1):
    handRank="FULL HOUSE"
    payout=3

  elif (3-handCounter["2"] in v):
    handRank="THREE OF A KIND"
    payout=1





  winnings=bet*payout*0.25
  
  print("Bet:",bet)
  print("You win:",winnings)
  return{"winnings":winnings,"handRank":handRank}  

@app.route("/calculateJokers",methods=["POST"])
def calculateJokers():
  data=request.get_json()
  handFromReact=data["hand"]
  bet=data["bet"]
  payout=-1
  hand=[]
  for originalCard in handFromReact:
    if originalCard["rank"]=="Joker1" or originalCard["rank"]=="Joker2":
      originalCard["rank"]="Joker"
    hand.append(originalCard)
  handCounter= {
    "Ace":0,
    "2":0,
    "3":0,
    "4":0,
    "5":0,
    "6":0,
    "7":0,
    "8":0,
    "9":0,
    "10":0,
    "Jack":0,
    "Queen":0,
    "King":0,
    "Joker":0
  }

  suitCounter={
    "Clubs":0,
    "Diamonds":0,
    "Hearts":0,
    "Spades":0,
    "Joker":0
  }
 

 

  handRank="NOTHING"

  for c in hand:
    handCounter[c["rank"]]=handCounter[c["rank"]]+1
    if c["rank"]=="Joker":
      handCounter["Joker"]=suitCounter["Joker"]+1
      suitCounter["Joker"]=suitCounter["Joker"]+1
    else:
      suitCounter[c["suit"]]=suitCounter[c["suit"]]+1
 



  suits=list(suitCounter.values())
  suits.pop(4)
 
  v=list(handCounter.values())
  v.pop(13)

  if 1 in v:
    w=v.index(1)
 
  else:
    w=0



  highStraight=((handCounter["Ace"]+handCounter["10"]+handCounter["Jack"]+handCounter["Queen"]+handCounter["King"]+handCounter["Joker"]==5) and (handCounter["Ace"]<=1 and handCounter["10"]<=1 and handCounter["Jack"]<=1 and handCounter["Queen"]<=1 and handCounter["King"]<=1))
  isStraight=False

  if w<=7 and w>0:

     isStraight=((v[w]+v[w+1]+v[w+2]+v[w+3]+v[w+4]+handCounter["Joker"]==5) and (v[w]<=1 and v[w+1]<=1 and v[w+2]<=1 and v[w+3]<=1 and v[w+4]<=1)) or highStraight

  isFlush=(5-suitCounter["Joker"]) in suits

  if highStraight and isFlush and (suitCounter["Joker"]==0):
    handRank="ROYAL FLUSH"
    payout=250
    if bet==5:
      payout=940
    
  
  elif highStraight and isFlush and suitCounter["Joker"]!=0:
    handRank="WILD ROYAL FLUSH"
    payout=100


  elif (5-handCounter["Joker"] in v):
    handRank="FIVE OF A KIND"
    payout=200

 
  elif isStraight and isFlush:
    handRank="STRAIGHT FLUSH"
    payout=50
 
  elif (4-suitCounter["Joker"] in v):
    handRank="FOUR OF A KIND"
    payout=20
 
  elif isStraight or highStraight:
    handRank="STRAIGHT"
    payout=3
 
  elif isFlush:
    handRank="FLUSH"
    payout=5



  elif (v.count(2)==1 and v.count(3)==1 and suitCounter["Joker"]==0) or (v.count(2)==2 and suitCounter["Joker"]==1):
    handRank="FULL HOUSE"
    payout=7

  elif (3-suitCounter["Joker"] in v):
    handRank="THREE OF A KIND"
    payout=2

  elif v.count(2)==2 or (v.count(2)==1 and suitCounter["Joker"]==1):
    handRank="TWO PAIR"
    payout=1

  elif ((handCounter["King"]==2 or handCounter["Ace"]==2) and suitCounter["Joker"]==0) or (handCounter["King"]==1 and suitCounter["Joker"]==1) or (handCounter["Ace"]==1 and suitCounter["Joker"]==1):
    handRank="KINGS OR BETTER"
    payout=1


 
  


  winnings=bet*payout*0.25
 
  
  
  
  print("Bet:",bet)
  print("You win:",winnings)
  return{"winnings":winnings,"handRank":handRank}  
