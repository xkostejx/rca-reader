#!/usr/bin/python

from time import sleep
import sys
import re
from mygpio import mygpio
from mydb import mydb
from myldap import myldap
from config import config as c

# Raspberry board pinout
BUZZER     = c.BUZZER 
LED_RED    = c.LED_RED
LED_GREEN  = c.LED_GREEN
LED_BLUE   = c.LED_BLUE

DB_HOST    = c.DB_HOST
DB_USER    = c.DB_USER
DB_PASS    = c.DB_PASS
DB_NAME    = c.DB_NAME

LDAP_SRV   = c.LDAP_SRV

def main():
	gpio = mygpio(LED_RED, LED_GREEN, LED_BLUE, BUZZER)
	db = None
	ldap = None

	while True:
		try:
			# Init 	
			ldap = myldap(LDAP_SRV)
			db   = mydb(DB_HOST, DB_USER, DB_PASS, DB_NAME)

			# Ready to start
			gpio.startSeq()	
			gpio.ledForTime(LED_GREEN, mygpio.INFINITY)

			while True:
				line = sys.stdin.readline()
				chipidsearch = re.search( r'SN=\[([a-f0-9]*)\]', line, re.M)
				chipid = None
				if chipidsearch:
					chipid = chipidsearch.group(1)
					#print "CardID = %s" % (chipid)

					user = db.getUserByChipId(chipid)
					if not user:
						ldapuser = ldap.getLdapUserByChipId(chipid)
						if ldapuser is None:
							# chipid not in LDAP, invalid user
							gpio.failSeq()
							continue
									
						username = ldapuser.get('uid')
						user = db.getUserByUsername(username)
						if user:
							# username in db, but with different chipcard
							db.updateChipCard(user, chipid)
						else:			
							# new username, adding to db
							db.insertUserFromLdap(ldapuser, chipid)
							user = db.getUserByUsername(username)
					else:
						# it's ok
						# user with chipcard already in db
						pass
                   			
					gpio.successSeq()
					db.insertCoffee(user)
								
				else:
					gpio.failSeq()

				sleep(0.1)
		
		except Exception as error:
			# Bad state (mysql, ldap, ...), reboot of raspberry is needed
			print error	
			if db:
				db.close()
			
			if ldap:
				ldap.close()
			
			#15s blinking RED
			gpio.ledFail(LED_RED, 1)

		print "Error occurred, restarting rca-reader"

if __name__ == "__main__":
    main()
