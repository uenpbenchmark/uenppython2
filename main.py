# coding: utf-8
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
		#1. Carrega variáveis necessárias para o workload por post
			workload = self.request.get("workload")
			operationcount = self.request.get("operationcount")
			schema = self.request.get("schema")
			writes = self.request.get("writes")
			reads = self.request.get("reads")
			
			#2. Armazena o tempo inicial
			initialTime = time.clock() 
			
			#3. Realiza as operações de acordo com o esquema recebido por post
			# No Python, cria-se grupos de entidade da seguinte forma: 
			# Crie um objeto pai; persista o objeto pai com a funcao put(), que retorna uma chave;
			# Crie um objeto filho e passe a chave do objeto pai como parâmetro (parent = chaveDoPai)
			if(schema == "1"):
				
				user = User()
				userKey = user.put()
				article = Article(parent = userKey)
				articleKey = article.put()
			
				for writeOperations  in range(0, int(writes)):
					comment = Comment(parent = articleKey)
					comment.put()
				for readOperations  in range(0, int(reads)):
					query = Comment.query().get()
			
			elif(schema == "2"):
				#No esquema 2, o número de escritas é dividido por 2 porque a cada iteração, são inseridas 3 entidades
				for writeOperations  in range(0, int(writes)/3):
					user = User()
					userKey = user.put()
					article = Article(parent = userKey)
					article.put()
					comment = Comment(parent = userKey)
					comment.put()
				for readOperations  in range(0, int(reads)):
					query = Comment.query().get()
			
			totalTime = time.clock() - initialTime
			
			dictionary = {'expectedReads:': reads, 'reads': "a implementar", 'expectedWrites': writes, 'writes': "a implementar" ,'totalTime': totalTime }
			self.response.write(template.render('results.html', dictionary))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
