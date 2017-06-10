#!/usr/bin/env python2.7
# Code for query the 'puppyshelter.db' using sqlalchemy library.
# This is a project in the Full Stack Web Developer nanodegree program

##import sessionmaker to build a query session
from sqlalchemy.orm import sessionmaker

##import create_engine to build connection to database
from sqlalchemy import create_engine

##import table configurations from the table classes
from database_setup import Base, Shelter, Puppy

##import date for age calculation; import func to use sql functions
from datetime import date
from sqlalchemy import func

##set connection pointer to database
e = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = e

##set the query session
DBSession = sessionmaker(bind = e)

##make the query session and store it in 'session'
session = DBSession()

##time to use the session, test the first shelter
firstShelter = session.query(Shelter).first()
print ''
print 'Test: the first shelter is ' + firstShelter.name
print ''

##1. Query all of the puppies and return the results
##in ascending alphabetical order
def query_one():
    result = session.query(Puppy.name).order_by(Puppy.name.asc())
    print ("*****           All the puppies           *****")
    for a,b,c,d in zip(result[::4], result[1::4], result[2::4], result[3::4]):
        print '{:<12}{:<12}{:<12}{:<}'.format(a[0],b[0],c[0],d[0])

##2. Query all of the puppies that are less than 6 months old
##organized by the youngest first
def query_two():
    today = date.today()
    if (today.month>6):
        cut_off = date(today.year, today.month-6, today.day)
    else:
        cut_off = date(today.year-1, today.month+6, today.day)
    print today
    result = session.query(Puppy.name, Puppy.dateOfBirth)\
             .filter(Puppy.dateOfBirth>cut_off)\
             .order_by(Puppy.dateOfBirth.desc())
    print ("*****All the puppy toddlers younger than 6 months*****")
    for name, b_day in result:
        print '{0:<12}{1}'.format(name, b_day)

##3. Query all puppies by ascending weight
def query_three():
    result = session.query(Puppy.name, Puppy.weight)\
             .order_by(Puppy.weight.asc())
    print ("*****From skiny to chubby*****")
    for name, weight in result:
        print '{0:<12}{1:.1f} lbs'.format(name, weight)
    
##4. Query all puppies grouped by the shelter in which they are staying
def query_four():
    result = session.query(Shelter, func.count(Puppy.id))\
             .join(Puppy).group_by(Shelter.id).all()
    for shelter, count in result:
        print shelter.id, shelter.name, count

##5. Query all puppies in a shelter
def query_five():
    result = session.query(Shelter.name, Puppy.name)\
             .join(Puppy).order_by(Shelter.id)
    for shelter, pup in result:
        print '{0:<25} {1}'.format(shelter, pup)

if __name__ == '__main__':
    query_one()
    query_two()
    query_three()
    query_four()
    #query_five()
    
