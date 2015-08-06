#!/usr/bin/env python
#!-*- coding: utf-8 -*-
#
# afisha.ru bulk parser

from pdb import set_trace
import requests
from lxml import etree

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Text, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref, sessionmaker

engine = create_engine('sqlite:///afisharu.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)


def create_db():
    """Create database sqlite."""
    try:
        Base.metadata.create_all(engine)
        print "[+] Ok, database is created succesfully."
        return
    except Exception as __e:
        print "[-] Some error with database createing:"
        print __e

def get_db():
    """ Return db pointer. """
    try:
        dbsession = sessionmaker(bind=engine)
        session = dbsession()
        return session
    except Exception as _e:
        print _e


class Restoraunt(Base):
    __tablename__ = 'Restoraunts'
    id         = Column(Integer,    primary_key = True)
    kitchen    = Column(String,     default = '')
    metro      = Column(String,     default ='')
    def __init__(self, name, metro):
        self.name = name
        self.kitchen = kitchen
        self.metro = metro

base_url = 'http://www.afisha.ru/msk/restaurants/restaurant_list/'
page_prefix = '?&q=&page='

pages = 7
db = get_db();

for page in xrange(2, pages):
    print '-----'
    print u"страница %s" % page
    print '-----'
    page_url = "%s%s%i" % (base_url, page_prefix, page)
    req = requests.get(page_url)
    places = etree.HTML(req.content).xpath('//a[@class="places_link"]')
    places = [x.text.strip() for x in places if x.text and x.text.strip()]
    for place in places:
        print place

