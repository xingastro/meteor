from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, HttpResponse


import sqlite3
from collections import namedtuple
import random
import re


# Create your views here.

car = []

def index(request):
    Entry = namedtuple('Entry', 'id, book_name, pic_url, pub, brief_des, des')
    with sqlite3.connect('meteor/data/db.sqlite') as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""SELECT * FROM books WHERE 
              id in (?, ?, ?, ?, ?);""", random.sample(range(0, 100), 5))
        entries = [Entry(*tuple(entry)) for entry in cur.fetchall()]
    return render(request, 'meteor/index.html', {'entries': entries})


def more(request, book_name):
    with sqlite3.connect('meteor/data/db.sqlite') as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""SELECT * FROM books WHERE book_name=(?)""", (book_name,))
        entry = cur.fetchone()
    return render(request, 'meteor/more.html', {'entry': entry})

def search(request):
    book_name = request.POST['book_name']
    return HttpResponseRedirect(reverse('meteor:more', args=(book_name,)))


def cars(request):
    global car
    Book = namedtuple('Book', 'book_name, price')
    with sqlite3.connect('meteor/data/db.sqlite') as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        books = []
        for index, book in enumerate(car):
            cur.execute("""SELECT book_name, pub FROM books WHERE book_name=(?)""", (book, ))
            book_name, pub =cur.fetchone() # book_name, pub
            books.append(Book(book_name, pub.split('/')[-1].replace('元', '')
                              .replace('NT$', '').replace('CNY', '')
                              .replace('NTD', '')))
    return render(request, 'meteor/cars.html', {'books': books})


def add_book(request):
    global car
    if request.method == 'POST':
        book_name = request.body.decode('utf-8').split('=')[-1]
        car.append(book_name) if book_name not in car else None
    return HttpResponse('Hi, client')

def del_book(request):
    global car
    if request.method == 'POST':
        book_name = request.body.decode('utf-8').split('=')[-1]
        if book_name == '*cleanbook*':
            car.clear()
            return HttpResponseRedirect(reverse('meteor:cars'))
        else:
            car.remove(book_name)
    return HttpResponse('Hi, client')


def buy(request):
    global car
    Book = namedtuple('Book', 'book_name, price')
    with sqlite3.connect('meteor/data/db.sqlite') as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        books = []
        for index, book in enumerate(car):
            cur.execute("""SELECT book_name, pub FROM books WHERE book_name=(?)""", (book,))
            book_name, pub = cur.fetchone()  # book_name, pub
            books.append(Book(book_name, pub.split('/')[-1].replace('元', '')
                              .replace('NT$', '').replace('CNY', '')
                              .replace('NTD', '')))
    total_money = round(sum(float(i.price) for i in books), 2)
    return render(request, 'meteor/buy.html', {'total_money': total_money})
