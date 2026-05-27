import time
from collections import defaultdict
from scapy.all import *

THRESHOLD = 10 #Number of different ports connected to by a single source before being flagged
TIME_WINDOW = 10 #Time window in second to count the ports visited

blocked_ips = set() #create a set with just unique values
flagget_ips = set()


connection = defaultdict(list) #All ports the source i
