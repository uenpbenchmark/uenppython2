# coding: utf-8
# modelo de dados: 2 - Orientado a usuários
import webapp2
import os
import time
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

class User(ndb.Model):
	name = ndb.StringProperty()

class Article(ndb.Model):
	name =  ndb.StringProperty()
	text = ndb.StringProperty()

class Comment(ndb.Model):
	name =  ndb.StringProperty()
	text = ndb.StringProperty()
	article = ndb.KeyProperty()

class MainHandler(webapp2.RequestHandler):
		
		def post(self):
			workload = self.request.get("workload")
			operationcount = self.request.get("operationcount")
			schema = self.request.get("schema")
			writes = 0
			reads = 0
			
			if (workload == "a"):
				writes = 0.5 * int(operationcount)
				reads = 0.5 * int(operationcount)
			elif(workload == "b"):
				writes = 0.9 *  int(operationcount)
				reads = 0.05 * int(operationcount)
			elif(workload == "c"):
				writes = 0
				reads = int(operationcount)
			elif(workload == "w"):
				writes =   int(operationcount)
				reads = 0
			
			self.persist(writes, reads, schema)
			
		def persist(self, writes, reads, schema):
			
			user = User()
			userKey = user.put()
			article = Article(parent = userKey)
			articleKey = article.put()
			
			initialTime = time.clock() 
			for writeOperations  in range(0, int(writes)):
				if (schema == "1"):
					comment = Comment(parent = articleKey)
					comment.put()
				else:
					comment = Comment(parent = userKey)
					comment.put()
			for readOperations  in range(0, int(reads)):
				query = Comment.query().get()
			totalTime = time.clock() - initialTime
			
			dictionary = {'expectedReads:': reads, 'reads': 2, 'expectedWrites': writes, 'expectedWrites': 4 ,'totalTime': totalTime }
			self.response.write(template.render('results.html', dictionary))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
