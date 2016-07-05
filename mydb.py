import MySQLdb


class mydb():

	COFFEE_PRICE = 5

	def __init__(self, host, user, passwd, db):
		self.host = host
		self.user = user
		self.passwd = passwd
		self.db = db

		self.conn = MySQLdb.connect(self.host, self.user, self.passwd, self.db, use_unicode=True, charset="utf8")
		self.conn.ping(True)
		self.cur = self.conn.cursor(MySQLdb.cursors.DictCursor)

	
	def getUserByChipId(self, chipid):
		#print "SELECT * FROM users WHERE chipid = '%s'" % (chipid)
		self.cur.execute("SELECT * FROM users WHERE chipid = '%s'" % (chipid))
		return self.cur.fetchone()
	
	def getUserByUsername(self, username):
		#print "SELECT * FROM users WHERE username = '%s'" % (username)
		self.cur.execute("SELECT * FROM users WHERE username = '%s'" % (username))
		return self.cur.fetchone()

	def insertUserFromLdap(self, ldapuser, chipid, role = 0, status = 1):
		username = ldapuser.get('uid')
		givenname = ldapuser.get('givenName;lang-cs')
		surname = ldapuser.get('sn;lang-cs')
		fullname = ldapuser.get('cn;lang-cs')
		email = ldapuser.get('mail')
		
		#print "INSERT INTO users VALUES (NULL, NOW(), '%s', '%s', '%s', '%s', '%s', '%s', %d, %d)" % (username, givenname, surname, fullname, email, chipid, role, status)
		self.cur.execute("INSERT INTO users VALUES (NULL, NOW(), '%s', '%s', '%s', '%s', '%s', '%s', %d, %d)" % (username, givenname, surname, fullname, email, chipid, role, status))
		self.conn.commit()

	def updateChipCard(self, user, chipid):
		#print "UPDATE CHIP for %s (%s)" % (user['username'], chipid)
		#print "UPDATE users SET chipid = '%s' WHERE username = '%s'" % (chipid, user['username'])
		self.cur.execute("UPDATE users SET chipid = '%s' WHERE username = '%s'" % (chipid, user['username']))
		self.conn.commit()
	
	def insertCoffee(self, user):
		pricedb = self.getCoffeePrice()
		price = pricedb if pricedb else mydb.COFFEE_PRICE
	
		#print "INSERT INTO coffee VALUES(NULL, NOW(), %d, %d)" % (int(user['id']), price)
		self.cur.execute("INSERT INTO coffee VALUES(NULL, NOW(), %d, %d)" % (int(user['id']), price))
		self.conn.commit()

	def getCoffeePrice(self):
		#print "SELECT price FROM settings LIMIT 1"
		self.cur.execute("SELECT price FROM settings LIMIT 1")
		rs = self.cur.fetchone()

		try:
			if 'price' in rs:
				return int(rs.get('price'))
			else:	
				return None
		except:
			return None

	
	def close(self):
		if self.cur:
			self.cur.close()
	
		if self.conn.open:
			self.conn.close()

	def is_connected(self):
		return self.conn.is_connected()

