from pyquery import PyQuery as pq
from lxml import etree
import urllib

from client import drawer

d = pq(filename='../templates/index.html')

# print(d.html())

print(d('#clear'))