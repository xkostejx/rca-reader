import ldap

class myldap():
	
	BASEDN = "ou=rfc2307,o=zcu,c=cz"

	def __init__(self, server):
		self.server = server
		self.session = ldap.initialize(server)
                self.session.protocol_version = ldap.VERSION3
	
	def getLdapUserByChipId(self, chipid):
        	retrieveAttributes = ['uid', 'cn', 'mail', 'givenname', 'sn']
        	searchFilter = "jisChipNo=%s" % (chipid)

	        res = self.session.search_s(myldap.BASEDN, ldap.SCOPE_SUBTREE, searchFilter, retrieveAttributes)
		if res:
			res2 = {}
			for key, elem in res[0][1].items():
				res2[key] = elem[0].decode('utf8')
				#res2[key] = elem[0]

			print res2
			return res2
		else:
			return None


        	return res[0][1] if res else None

	def close(self):
		if self.session:
			self.session.unbind()
