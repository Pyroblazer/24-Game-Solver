import kivy
import random

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

# Setting untuk GUI
Builder.load_string('''
#:kivy 1.10.1

<RootWidget>:
    FloatLayout:
        size: (800,600)
        FloatLayout:
            Image:
                id: card_1
                source: ""
                size_hint: .2,.2
                pos_hint: {'x':.4,'y':.65}
            Image:
                id: card_2
                source: ""
                size_hint: .2,.2
                pos_hint: {'x':.15,'y':.45}
            Image:
                id: card_3
                source: ""
                size_hint: .2,.2
                pos_hint: {'x':.4,'y':.25}
            Image:
                id: card_4
                source: ""
                size_hint: .2,.2
                pos_hint: {'x':.65,'y':.45}
            Image:
                source:"Image/24.png"
                size_hint: .1,.1
                pos_hint: {'x':.45,'y':.5}
        FloatLayout:
            Button:
                id: deal
                size_hint: .125,.1
                text: "Deal"
                bold: True
                font_size: 18
                pos_hint: {'x':.315,'y':.5}
                on_press: root.deal()
                background_normal: ''
                background_color: .0, 75, 75, .75
                disabled: False
            Button:
                id: reset
                size_hint: .125,.1
                text: "Reset Deck"
                font_size: 18
                bold: True
                pos_hint: {'x':.555,'y':.5}
                on_press: root.reset()
                background_normal: ''
                background_color: .0, 75, 75, .75
                disabled: True
            Label:
                id: card_num
                size_hint: .3,.3
                font_size: 30
                text: "Remaining Cards: 52"
                pos_hint: {'x':.35,'y':.775}
    Label:
        id: answer
        size_hint: .5,.5
        font_size: 36
        text: ""
        pos_hint: {'x':.25,'y':-.1}
''')

class RootWidget(FloatLayout):
  # Kelas untuk tampilan utama
  def __init__(self, **kwargs):
    super(RootWidget, self).__init__(**kwargs)
    self.deck = Deck()
    self.deck.start()
    self.deck2 = Deck()
    self.table = Deck()
    self.num = []
    self.op = []
    self.ids.card_1.source = "Image/blue_back.png"
    self.ids.card_2.source = "Image/blue_back.png"
    self.ids.card_3.source = "Image/blue_back.png"
    self.ids.card_4.source = "Image/blue_back.png"

  def deal(self):
  # Mengeluarkan 4 kartu dari dek utama dan menampilkan hasil operasi dari 4 kartu tersebut
     if(self.deck.deck != []):
         if(self.table != []):
             self.table.clear()
             del self.num[:]
             del self.op[:]
         for i in range(4):
             card = self.deck.remove()
             self.num.append(self.translate(card.num[0]))
             self.deck2.add(card)
             self.table.add(card)
         self.ids.reset.disabled = False
         self.sort()
         self.op.append(self.pick_operator(self.num[0],self.num[1]))
         self.op.append(self.pick_operator(self.hitung(self.num[0],self.op[0],self.num[1]),self.num[2]))
         self.op.append(self.pick_operator(self.hitung(self.hitung(self.num[0],self.op[0],self.num[1]),self.op[1],self.num[2]),self.num[3]))
         self.ids.card_num.text = "Remaining Cards : " + str(len(self.deck.deck))
         self.ids.card_1.source = "Image/" + self.table.deck[0].num + self.table.deck[0].suit[0] + ".png"
         self.ids.card_2.source = "Image/" + self.table.deck[1].num + self.table.deck[1].suit[0] + ".png"
         self.ids.card_3.source = "Image/" + self.table.deck[2].num + self.table.deck[2].suit[0] + ".png"
         self.ids.card_4.source = "Image/" + self.table.deck[3].num + self.table.deck[3].suit[0] + ".png"
         self.ids.answer.text = self.solve(self.num[0],self.op[0],self.num[1],self.op[1],self.num[2],self.op[2],self.num[3])
         if(self.deck.deck == []):
             self.ids.deal.disabled = True

  def reset(self):
  # Mengembalikan seluruh kartu yang telah digunakan ke dek awal, urutan kartu diacak kembali
    for i in range(len(self.deck2.deck)):
        card = self.deck2.remove()
        self.deck.add(card)
    self.ids.card_1.source = "Image/blue_back.png"
    self.ids.card_2.source = "Image/blue_back.png"
    self.ids.card_3.source = "Image/blue_back.png"
    self.ids.card_4.source = "Image/blue_back.png"
    self.table.clear()
    self.ids.card_num.text = "Remaining Cards : " + str(len(self.deck.deck))
    random.shuffle(self.deck.deck)
    self.ids.answer.text = ""
    self.ids.deal.disabled = False
    self.ids.reset.disabled = True
    del self.num[:]
    del self.op[:]

  def sort(self):
  #prosedur untuk sort 4 bilangan dari besar ke kecil
  #menggunakan bubble sort
      for i in range(4):
          for j in range (0, 3-i):
    	        if(self.num[j] < self.num[j+1]):
                    self.num[j], self.num[j+1] = self.num[j+1], self.num[j]


  def translate(self,char):
  # Mengubah karakter dari nomor kartu menjadi integer
      if(char == "J"):
          return(11)
      elif(char == "Q"):
          return(12)
      elif(char == "K"):
          return(13)
      elif(char == "A"):
          return(1)
      elif(char == "1"):
          return(10)
      else:
          return int(char)

  def hitung(self,a,operator,b):
  #fungsi untuk mengembalikan hasil dari operasi a dan b yang sesuai dengan operatornya
  #operator terdiri dari +,-,*,/
      if (operator == '+'):
        return a+b
      elif (operator == '-'):
        return a-b
      elif (operator == '*'):
        return a*b
      elif (operator == '/'):
        return a/b

  def pick_operator(self,a,b):
  #fungsi untuk mengembalikan operator yang sesuai sehingga operasi a b mendekati 24
  #operator yang digunakan adalah +,-,*,/
    if (a < 24):
        op = '+'
        pembanding = abs(a+b-24)
        if(abs(a*b-24) < pembanding):
            op = '*'
    elif (a > 24):
        op = '-'
        pembanding = abs(a-b-24)
        if(abs(a/b-24) < pembanding):
            op = '/'
    else:
        op = '+'
        pembanding = abs(a+b-24)
        if(abs(a-b-24) < pembanding):
            pembanding = abs(a-b-24)
            op  = '-'
        if(abs(a*b-24) < pembanding):
            pembanding = abs(a*b-24)
            op = '*'
        if(abs(a/b-24) < pembanding):
            pembanding = abs(a/b-24)
            op = '/'
    return op

  def hitung_all(self,a,b,c,d):
  #mengembalikan hasil dari operasi a,b,c,d dengan operator yang sesuai agar mendekati 24
  #menggunakan algoritma greedy
  	op1 = self.pick_operator(a,b)
  	op2 = self.pick_operator(self.hitung(a,op1,b),c)
  	op3 = self.pick_operator(self.hitung(self.hitung(a,op1,b),op2,c),d)
  	return self.hitung(self.hitung(self.hitung(a,op1,b),op2,c),op3,d)

  def solve(self,a,op1,b,op2,c,op3,d):
    #mengembalikan output dari hasil operasi dengan tempat kurung yang sesuai
    if (((op2 == '+') or (op2 == '-')) and ((op3 == '*') or (op3 == '/'))):
    	return ("(" + str(a) + op1 + str(b) + op2 + str(c) + ")" + op3 + str(d) + "=" + str(self.hitung_all(a,b,c,d)))
    elif (((op1 == '+') or (op1 == '-')) and ((op2 == '*') or (op2 == '/'))):
    	return ("(" + str(a) + op1 + str(b) + ")" + op2 + str(c) + op3 + str(d) + "=" + str(self.hitung_all(a,b,c,d)))
    else:
    	return (str(a) + op1 + str(b) + op2 + str(c) + op3 + str(d) + "=" + str(self.hitung_all(a,b,c,d)))

class Card(object):
    # Kelas untuk kartu, terdiri dari angka dan jenis
    suits = ("Club","Heart","Spade","Diamond")
    nums = ("2","3","4","5","6","7","8","9","10","Jack","Queen","King","Ace")

    def __init__(self, num ,suit):
        self.num=num
        self.suit=suit

class Deck(object):
    # Kelas untuk dek kartu
    def __init__(self):
        self.deck = []

    def start(self):
    # Mengisi dek dengan 52 kartu berbeda
        for suit in Card.suits:
            for num in Card.nums:
                self.deck.append(Card(num,suit))
        random.shuffle(self.deck)

    def remove(self):
    # Mengeluarkan satu kartu dari dek
        card = self.deck.pop()
        return card

    def add(self,Card):
    # Menambah satu kartu ke dalam dek
        self.deck.append(Card)

    def clear(self):
    # Menghapus seluruh kartu dari dek
        del self.deck[:]

class TestApp(App):
    # Menjalankan GUI
     def build(self):
         return RootWidget()


if __name__ == '__main__':
    TestApp().run()
