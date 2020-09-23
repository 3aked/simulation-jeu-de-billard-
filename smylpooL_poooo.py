# -*- coding: latin-1 -*-

import pygame 
import math
import time

#définition des couleurs
green_bord=(12,53,30)
green_table=(0,96,41)
light_blue=(16,190,238)
brown1=(62,35,23)
beige=(215,215,115)
white=(255,255,255)
black=(0,0,0)
brown=(60,30,5)
blue=(0,30,100)
green=(0,50,20)
yellow=(230,220,20)
red = (240,0,0)
pink=(240,140,210)
#light_brown_light()

# Frames per second - Nomb_rede d'images par secondes
FPS = 130

#Définitions des constantes réelles
cos45 = math.sqrt(2)/2.0
epsilon = 0.01 

(x0,y0)=(75,75)

#variables globales pour stocker le son
sound_cue_ball = None
sound_ball_ball = None
sound_ball_fall = None
sound_ball_border = None

#définition de classes:
class Shape:
	def __init__(self,x,y,(r,g,b)):
		self.px=x
		self.py=y
		self.color=(r,g,b)
		
class Rectangle(Shape):
	# Constructeur
	def __init__(self, x, y, w, h,color):
		Shape.__init__(self,x,y,color)
		self.width = w
		self.height = h
		
	def draw(self, screen):
		pygame.draw.rect(screen, self.color, [ (self.px, self.py), (self.width, self.height) ], 0)
		
	def contains(self, x, y):
		return (x >= self.px) and (y >= self.py) and (x <= self.px + self.width)  and (y <= self.py + self.height)

class Trapeze(Shape):
	# Constructeur
	def __init__(self,list_points,color):
		self.list_points=list_points
		Shape.__init__(self,self.list_points[0][0],self.list_points[0][1],color)
		
		self.rect=self.get_rect0()
		self.rect1=self.get_rect1()
		self.rect2=self.get_rect2()
		
	def draw(self,screen):
		pygame.draw.polygon(screen,self.color,self.list_points,0)
		
	def get_rect0(self):
		(x1,y1)=(7000,7000)
		for p in self.list_points:
			if p[0]< x1:
				x1=p[0]
			if p[1]<y1:
				y1=p[1]
		(x,y)=(0,0)
		for p in self.list_points:
			if p[0]>x:
				x=p[0]
			if p[1]>y:
				y=p[1]
		return Rectangle(x1,y1,x-x1,y-y1,white)
		
	def get_rect1(self):
		(x1,y1)=(7000,7000)
		for p in self.list_points[:2]:
			if p[0]< x1:
				x1=p[0]
			if p[1]<y1:
				y1=p[1]
		(x,y)=(0,0)
		for p in self.list_points[:2]:
			if p[0]>x:
				x=p[0]
			if p[1]>y:
				y=p[1]	
		return Rectangle(x1,y1,x-x1,y-y1,red)
		
	def get_rect2(self):
		(x1,y1)=(7000,7000)
		for p in self.list_points[2:]:
			if p[0]< x1:
				x1=p[0]
			if p[1]<y1:
				y1=p[1]
		(x,y)=(0,0)
		
		for p in self.list_points[2:]:
			if p[0]>x:
				x=p[0]
			if p[1]>y:
				y=p[1]	
				
		return Rectangle(x1,y1,x-x1,y-y1,blue)
		
	def num_rect_container(self,(x,y)):
		if self.rect1.contains(x,y):
			return 1
		elif self.rect2.contains(x,y):
			return 2
		else :
			return 0
			
	def contains(self,(x,y)):
		value=self.rect.contains(x,y)
		return value
		
class Circle(Shape):
	# Constructeur
	def __init__(self, x, y, r,color):
		Shape.__init__(self, x, y,color)
		self.radius = r

	def draw(self, screen):
		pygame.draw.circle(screen, self.color, (int(self.px), int(self.py)), self.radius, 0)	
		
	def contains(self,x,y):
		return (x - self.px) **2 + (y - self.py) ** 2 <= self.radius ** 2
		
	def mingled(self,ball):
		return ( self.px - ball.px )**2 + ( self.py - ball.py )**2 <= (self.radius+ball.radius+1)**2
		

class Ball(Circle):
	#constructeur
	def __init__(self,x,y,r,color,value):
		Circle.__init__(self,x,y,r,color)
		self.x0=self.px
		self.y0=self.py
		self.vx=0
		self.vy=0
		self.kicked=False
		self.friction=0.008
		self.deceleration=0.8
		self.timer=0
		self.ready=True
		self.value=value
		self.points=[ [self.px+self.radius,self.py],[self.px,self.py-self.radius],[self.px-self.radius,self.py],[self.px,self.py+self.radius],\
					[self.px+self.radius*cos45,self.py-self.radius*cos45], [self.px+self.radius*cos45,self.py+self.radius*cos45],\
					[self.px-self.radius*cos45,self.py+self.radius*cos45], [self.px-self.radius*cos45,self.py-self.radius*cos45] ]
	
	def set_speed(self,nvx,nvy):
		self.vx=(self.deceleration*nvx)
		self.vy=(self.deceleration*nvy)
		self.kicked=True
		self.ready=False
		self.timer=time.time()
		
	def collision(self,ball,liste_collisions_cueBall):
		if ball is not self:
			npx1=self.px+self.vx
			npy1=self.py+self.vy
			npx2=ball.px+ball.vx
			npy2=ball.py+ball.vy
				
			if math.sqrt((npx1-npx2)**2+(npy1-npy2)**2)<=self.radius+ball.radius:
				
				v1=math.sqrt(self.vx**2+self.vy**2)
				v2=math.sqrt(ball.vx**2+ball.vy**2)
					
				if v1!=0:
					pasx1=self.vx*1.0/v1
					pasy1=self.vy*1.0/v1
				else :
					pasx1=0
					pasy1=0
				if v2!=0:					
					pasx2=ball.vx*1.0/v2
					pasy2=ball.vy*1.0/v2
				else:
					pasx2=0
					pasy2=0
					
				npx1=self.px
				npy1=self.py
				npx2=ball.px
				npy2=ball.py
					
				cpt=0
				while  math.sqrt((npx1-npx2)**2+(npy1-npy2)**2)>self.radius+ball.radius+1.5:
					npx1=npx1+pasx1
					npy1=npy1+pasy1
					npx2=npx2+pasx2
					npy2=npy2+pasy2
					cpt=cpt+1
					if cpt>20:
						break
				self.px=npx1
				self.py=npy1
				ball.px=npx2
				ball.py=npy2
					
				deltaX=(ball.px)-self.px
				deltaY=(ball.py)-self.py
				deltaVx=-self.vx+ball.vx
				deltaVy=-self.vy+ball.vy
					
				if self.color==white or ball.color==white :
					if self.color==white:
						value=ball.value
					else:
						value=self.value
					liste_collisions_cueBall.append(value)
					
				self.set_speed( self.vx+(deltaVx*deltaX+deltaVy*deltaY)*deltaX*1.0/(4*self.radius**2),self.vy+(deltaVx*deltaX+deltaVy*deltaY)*deltaY*1.0/(4*self.radius**2))
				ball.set_speed(ball.vx-(deltaVx*deltaX+deltaVy*deltaY)*deltaX*1.0/(4*self.radius**2),ball.vy-(deltaVx*deltaX+deltaVy*deltaY)*deltaY*1.0/(4*self.radius**2))
					
				if ball.vx!=0 and ball.vy!=0:
					sound_ball_ball.play()
	
	def reflexion(self,extremities_t1,extremities_t2,extremities_t3,extremities_t4,(num_zone,edge_reflect)):
		if num_zone==0:
			if edge_reflect in range(0,2):
				self.vy=abs(self.vy)
				if self.vx!=0 and self.vy!=0:
					sound_ball_border.play()
							
			if edge_reflect ==2:
				self.vx=-abs(self.vx)
				if self.vx!=0 and self.vy!=0:
					sound_ball_border.play()
				
			if edge_reflect ==5:
				self.vx=abs(self.vx)
				if self.vx!=0 and self.vy!=0:
					sound_ball_border.play()
				
			if edge_reflect in range(3,5):
				self.vy=-abs(self.vy)
				if self.vx!=0 and self.vy!=0:
					sound_ball_border.play()
							
		else :
			v=math.sqrt(self.vx**2+self.vy**2)/2
			if (edge_reflect,num_zone) in extremities_t1:
				self.vx=-v
				self.vy=v
				if self.vx!=0 and self.vy!=0:
					sound_ball_border.play()
				
					
			elif (edge_reflect,num_zone) in extremities_t2:
				self.vx=v
				self.vy=-v
				if self.vx!=0 and self.vy!=0:
					sound_ball_border.play()
				
			elif (edge_reflect,num_zone) in extremities_t3:
				self.vx=v
				self.vy=v
				if self.vx!=0 and self.vy!=0:
					sound_ball_border.play()
			
			elif (edge_reflect,num_zone) in extremities_t4:
				self.vx=-v
				self.vy=-v
				if self.vx!=0 and self.vy!=0:
					sound_ball_border.play()
					
	def update (self,world,liste_collisions_cueBall,zones,extremities_t1,extremities_t2,extremities_t3,extremities_t4):
		if abs(self.vx)<epsilon and abs(self.vy)<epsilon:
			self.vx=0
			self.vy=0
			
		edge_reflect=None		

		#changement de direction suite à la réflexion	
		for edge in zones:
			for p in self.points:
				if edge.contains(p):
					num_zone=edge.num_rect_container(p)
					edge_reflect=zones.index(edge)
					break
		
		if edge_reflect != None:
			self.reflexion(extremities_t1,extremities_t2,extremities_t3,extremities_t4,(num_zone,edge_reflect))
				
				
		#friction
		t=time.time()-self.timer
		self.vx=self.vx*math.exp(-self.friction*t)
		self.vy=self.vy*math.exp(-self.friction*t)
	
		#collision
		for ball in world:
			self.collision(ball,liste_collisions_cueBall)
			
		#mise à jour de la position			
		self.px = self.px + self.vx
		self.py = self.py + self.vy
		self.points=points=[ [self.px+self.radius,self.py],[self.px,self.py-self.radius],[self.px-self.radius,self.py],[self.px,self.py+self.radius],\
					[self.px+self.radius*cos45,self.py-self.radius*cos45], [self.px+self.radius*cos45,self.py+self.radius*cos45],\
					[self.px-self.radius*cos45,self.py+self.radius*cos45], [self.px-self.radius*cos45,self.py-self.radius*cos45] ]		
					
		if self.vx==0 and self.vy==0:						
			if self.kicked: 
				self.ready= True
				self.kicked=False
			
			
class Line:
	#constructeur:
	def __init__(self,start_pos,end_pos,color,w):
		self.start_pos=start_pos
		self.end_pos=end_pos
		self.color=color
		self.width=w
		
	def draw(self,screen):
		pygame.draw.line(screen,self.color,self.start_pos,self.end_pos,self.width)
		
		
class Cue:
	#Constructeur
	def __init__(self,game,(x2,y2),(x1,y1)):
		self.raideur=0.12
		self.handled=False
		self.slope=(y2-y1)*1.0/(x2-x1)
		self.b=y1-self.slope*x1
		self.l0=game.radius+5
		self.l=game.radius+5
		self.length=440
		
		D=math.sqrt((x2-x1)**2+(y2-y1)**2)
		
		self.x_mouse=x1
		self.y_mouse=y1
		
		x_fin=x1+(x2-x1)*(self.length/D)
		y_fin=self.slope*x_fin+self.b
		
		x_centre=x1+(x2-x1)*(300/D)
		y_centre=self.slope*x_centre+self.b
		
		self.x_debut=x0+(x1-x0)*self.l/D
		self.y_debut=x1+(self.x_debut-x1)*(self.length/D)
		
		self.line1=Line((x_fin,y_fin),(x_centre,y_centre),brown1,6)
		self.line2=Line((x_centre,y_centre),(self.x_debut,self.y_debut),beige,5)
		self.line3=None
		
		self.vx=0
		self.vy=0
		self.x_handled=x_fin
		self.y_handled=y_fin
		self.released=False
		self.limit=100
		
	def draw(self,screen):
		self.line1.draw(screen)
		self.line2.draw(screen)
		if self.line3!=None:
			self.line3.draw(screen)
		
	def handle(self,pos):
		self.x_handled=pos[0]
		self.y_handled=pos[1]
		self.handled=True
		
	def hitball(self,xb,yb):
		self.handled=False
		self.released=True
		vy=yb-self.y_debut
		vx=xb-self.x_debut
		self.vx=vx*1.0/(math.sqrt(vx**2+vy**2))*(self.l-self.l0)*self.raideur
		self.vy=vy*1.0/(math.sqrt(vx**2+vy**2))*(self.l-self.l0)*self.raideur
		
	def update(self,x1,y1,ball):
		(x0,y0)=(ball.px,ball.py)
		(self.x_mouse,self.y_mouse)=(x1,y1)
		if self.handled==False:
			self.l=self.l0
			if x1!= x0:
				
				self.slope=(y1-y0)*1.0/(x1-x0)
				self.b=y0-self.slope*x0
			
				
		else :
			if math.sqrt((x1-x0)**2+(y1-y0)**2)>=math.sqrt((self.x_handled-x0)**2+(self.y_handled-y0)**2):
				self.l=self.l0+math.sqrt((self.x_handled-x1)**2+(self.y_handled-y1)**2)
				if self.l>self.limit:
					self.l=self.limit
		if x1!= x0 and y1!=y0:	
			D=math.sqrt((x1-x0)**2+(y1-y0)**2)
			self.x_debut=x0+(x1-x0)*self.l/D
			self.y_debut=self.slope*self.x_debut+self.b
			x_fin=x0+(x1-x0)*((self.length+self.l-self.l0)/D)
			y_fin=self.slope*x_fin+self.b
			x_centre=x0+(x1-x0)*((300+self.l-self.l0)/D)
			y_centre=self.slope*x_centre+self.b		
			self.line1=Line([x_fin,y_fin],[x_centre,y_centre],brown1,6)
			self.line2=Line([x_centre,y_centre],[self.x_debut,self.y_debut],beige,5)
			self.line3=self.path(x0,y0)
		elif x1==x0:
			
			self.line1=Line([x1,y0+self.length],[x1,y0+300],brown1,6)
			self.line2=Line([x1,y0+300],[x1,self.y_debut],beige,5)
			
	def update_on_release(self,ball,game):
		if (self.x_debut-ball.px)**2+(self.y_debut-ball.py)**2 >game.radius**2:
			(x_fin,y_fin)=self.line1.start_pos
			(x_centre,y_centre)=self.line1.end_pos
			(x_debut,y_debut)=self.line2.end_pos
			x_debut=x_debut+self.vx
			y_debut=y_debut+self.vy
			x_centre=x_centre+self.vx
			y_centre=y_centre+self.vy
			x_fin=x_fin+self.vx
			y_fin=y_fin+self.vy
			self.x_debut=x_debut
			self.y_debut=y_debut
			self.line1=Line([x_fin,y_fin],[x_centre,y_centre],brown1,6)
			self.line2=Line([x_centre,y_centre],[x_debut,y_debut],beige,5)
		else:
			ball.set_speed(self.vx,self.vy)
			self.vx=0
			self.vy=0
			self.released=False
			sound_cue_ball.play()
			
	def path(self,xb,yb):
		x2=self.line2.start_pos[0]
		y2=self.line2.start_pos[1]
		x1=xb
		while True:	
			x1=x1+(xb-x2-1)*1.0/abs(xb-x2-1)
			y1=self.slope*x1+self.b
			if (x1< 34+x0) or (x1>806+x0 )or (y1 < 34+y0) or (y1 > 406+y0):
				break
		return Line([x1,y1],[xb,yb],white,1)
	
		
class Text:
	#constructeur:
	def __init__(self, text, color,(x,y),menu_font):
		self.text = text
		self.pos = (x,y)
		self.color = color
		self.hovered=False
		self.menu=menu_font
		self.set_rect()
		
	def draw(self,screen):
		self.set_rend()
		screen.blit(self.rend, self.rect)
		
	def set_rend(self):
		self.rend = self.menu.render(self.text, True, self.color)
		
	
	def set_rect(self):
		self.set_rend()
		self.rect = self.rend.get_rect()
		self.rect.topleft = self.pos
		
class Option(Text):
	#constructeur:
	def __init__(self, text, color,color_rect,(x,y),menu_font):
		Text.__init__(self, text, color,(x,y),menu_font)
		self.color_rect = color_rect
		
	def set_rend(self):
		Text.set_rend(self)
		self.rend = self.menu.render(self.text, True, self.color)

	def draw_rect(self,screen,dim):
		pygame.draw.rect(screen, self.color_rect, [ (self.pos[0]-5,self.pos[1]-10), dim ], 0)
		
class Scene:
	#constructeur:
	def __init__(self):
		pygame.init()
		(W,H)=(960,680)
		self.screen=pygame.display.set_mode((W,H))
		self.destroy_all=False
		
	def run (self):
		return
			
	def quit(self):
		pygame.quit ()
		
class Scene_debut(Scene):
	#constructeur:
	def __init__(self):
		Scene.__init__(self)
		title_font = pygame.font.Font(None, 80)
		menu_font = pygame.font.Font(None, 40)
	
		self.choix_debut = [Option("Nouvelle partie",yellow,brown,(80,290),menu_font), \
					Option("Règles du jeu",yellow,brown,(680,290),menu_font),\
					Option("Continuer la partie",yellow,brown,(380,600),menu_font)]
		self.partie_en_cours=False			
		self.game_title=Text("Bienvenue sur SMYL Pool",red,(130,30),title_font)	
		
		self.regle=Regles()
		self.fond= pygame.image.load("menu.png").convert()
	def run (self):
		self.done=False
		self.boolean1=True
		self.boolean2=True
		pygame.init()
		while self.done == False:
			for event in pygame.event.get():
				#fermeture du programme
				if event.type == pygame.QUIT:
					self.done=True
				
				#manipulation de la queue avec la souris		
				elif event.type==pygame.MOUSEBUTTONDOWN:
					if self.choix_debut[0].rect.collidepoint(pygame.mouse.get_pos()):
						self.jeu=Snooker()
						self.partie_en_cours=True
						self.jeu.run()
						if self.jeu.destroy_all:
							self.done=True
						
						print pygame.display.get_init()
						self.boolean1=False
					if self.choix_debut[1].rect.collidepoint(pygame.mouse.get_pos()):
						self.regle.run()
						if self.regle.destroy_all :
							self.done=True
						self.boolean2=False
					if self.partie_en_cours:
						if self.choix_debut[2].rect.collidepoint(pygame.mouse.get_pos()):
							self.jeu.run()
							if self.jeu.destroy_all:
								self.done=True
						
				
			# collage du fond
			if not self.done:
			
				self.screen.blit(self.fond, (0,0))
				
					
				self.choix_debut[0].draw_rect(self.screen,(225,45))
				self.choix_debut[0].draw(self.screen)
				self.choix_debut[1].draw_rect(self.screen,(195,45))
				self.choix_debut[1].draw(self.screen)
				if self.partie_en_cours:
					self.choix_debut[2].draw_rect(self.screen,(275,45))
					self.choix_debut[2].draw(self.screen)
				
				self.game_title.draw(self.screen)
				pygame.display.flip()
			
			
class Regles(Scene):
	def __init__ (self):
		Scene.__init__(self)
		
		title_font = pygame.font.Font(None, 80)
		self.regle_title=Text("Règles du jeu",red,(300,30),title_font)
		
		texte_font = pygame.font.Font(None, 20)
		txt1="        Le snooker se joue à deux sur une table avec « une boule de choc » (la boule blanche) et des boules objets"
		txt2="objets appelées aussi couleurs(15 boules rouges valant 1 point et 6 boules de couleur jaune, vert, rose, marron,"
		txt3="bleu  et  noir  valant  2  points , 3  points , 4  points ,5  points , 6  points  et  7  points  respectivement  ) . Seule " 
		txt4="la boule blanche peut être directement jouée par le joueur à l'aide d'une queue."
		
		txt5="        Le  jeu  consiste  en  deux  phases ; Dans  la  première  phase,"
		
		txt6="les joueurs  doivent  jouer  une  boule rouge. Lorsqu'ils réussissent"
		txt7="à empocher  une boule rouge , ils obtiennent  un  autre  coup  leur"
		txt8="permettant de jouer une couleur .  Dés  que la dernière boule rouge"
		txt9="et la couleur ont été empochées, la deuxième phase commence. "
		txt09="Dans cette phase, les couleurs doivent être empochées dans l'ordre correct"
		txt009="à savoir jaune puis verte, marron, bleue,rose et enfin noire."
		txt10="Il est à noter que si le coup est valide, le joueur marque les points suivants :"
		txt11="   * 1 point pour chaque boule rouge "
		txt12="   * La valeur de la boule pour les couleurs"
		
		txt13="Sinon il sera pénalisé comme suit :"
		txt14="   * -2 s'il a empoché une boule non-valide "
		txt15="   * -1 si la boule blanche touche une boule non-valide "
		
		self.x_pos=70
		self.y_pos=110
		self.color=white
		self.fond=None
		self.texte1 = Option(txt1,self.color,self.fond,(self.x_pos,self.y_pos),texte_font)
		self.texte2 = Option(txt2,self.color,self.fond,(self.x_pos,self.y_pos+30),texte_font)
		self.texte3 = Option(txt3,self.color,self.fond,(self.x_pos,self.y_pos+60),texte_font)
		self.texte4 = Option(txt4,self.color,self.fond,(self.x_pos,self.y_pos+90),texte_font)
		
		self.texte5 = Option(txt5,self.color,self.fond,(self.x_pos,self.y_pos+140),texte_font)
		self.texte6 = Option(txt6,self.color,self.fond,(self.x_pos,self.y_pos+170),texte_font)
		self.texte7 = Option(txt7,self.color,self.fond,(self.x_pos,self.y_pos+200),texte_font)
		self.texte8 = Option(txt8,self.color,self.fond,(self.x_pos,self.y_pos+230),texte_font)
		self.texte9 = Option(txt9,self.color,self.fond,(self.x_pos,self.y_pos+260),texte_font)
		self.texte09 = Option(txt09,self.color,self.fond,(self.x_pos,self.y_pos+290),texte_font)
		self.texte009 = Option(txt009,self.color,self.fond,(self.x_pos,self.y_pos+320),texte_font)
		
		self.texte10 = Option(txt10,self.color,self.fond,(self.x_pos-50,self.y_pos+390),texte_font)
		self.texte11 = Option(txt11,self.color,self.fond,(self.x_pos-50,self.y_pos+420),texte_font)
		self.texte12 = Option(txt12,self.color,self.fond,(self.x_pos-50,self.y_pos+450),texte_font)
		self.texte13= Option(txt13,self.color,self.fond,(self.x_pos+520,self.y_pos+390),texte_font)
		self.texte14 = Option(txt14,self.color,self.fond,(self.x_pos+520,self.y_pos+420),texte_font)
		self.texte15 = Option(txt15,self.color,self.fond,(self.x_pos+520,self.y_pos+450),texte_font)
		
		button_font = pygame.font.Font(None, 30)
	
		self.button = Option("Retour au Menu principal",yellow,brown,(350,630),button_font)
		
	def run (self):
		self.done=False
		while self.done == False:
			for event in pygame.event.get():
				#fermeture du programme
				if event.type == pygame.QUIT:
					self.done=True
					self.destroy_all=True
				elif event.type==pygame.MOUSEBUTTONDOWN:
					if self.button.rect.collidepoint(event.pos):
						self.done=True
			
				
			#Chargement et collage du fond
			self.fond= pygame.image.load("fond2.jpg").convert()
			self.screen.blit(self.fond, (0,0))
			
			self.largeur1=530
			self.largeur2=370
			self.hauteur=30
			
			self.texte1.draw(self.screen)
			self.texte2.draw(self.screen)
			self.texte3.draw(self.screen)
			self.texte4.draw(self.screen)
			self.texte5.draw(self.screen)
			self.texte6.draw(self.screen)
			self.texte7.draw(self.screen)
			self.texte8.draw(self.screen)
			self.texte9.draw(self.screen)
			self.texte09.draw(self.screen)
			self.texte009.draw(self.screen)
			self.texte10.draw(self.screen)
			self.texte11.draw(self.screen)
			self.texte12.draw(self.screen)
			self.texte13.draw(self.screen)
			self.texte14.draw(self.screen)
			self.texte15.draw(self.screen)
			
			self.button.draw_rect(self.screen,(260,40))
			self.button.draw(self.screen)
			
			self.regle_title.draw(self.screen)
			pygame.display.flip()
			
class End_Game(Scene):
	def __init__(self,joueurs):
		Scene.__init__(self)
		
		msg_font = pygame.font.Font(None, 80)
		txt_font= pygame.font.Font(None,40)
		
		max=joueurs[0].score
		winner=joueurs[0]
		if joueurs[1].score>max:
			max=joueurs[1].score
			winner=joueurs[1]
			
		sound_end.play()
		
		self.fond= pygame.image.load("fin.jpg").convert()
	
		message="Bravo "+winner.name+"..!"
		self.msg = Option(message,white,red,(255,50),msg_font)
		
		texte_retour="Retour au menu principal"
		self.retour=Option(texte_retour,yellow,brown,(300,570),txt_font)
					
	def run(self):
		self.done=False
		while self.done == False:
			for event in pygame.event.get():
				#fermeture du programme
				if event.type == pygame.QUIT:
					self.done=True
					self.destroy_all=True
					
				elif event.type==pygame.MOUSEBUTTONDOWN:
					if self.retour.rect.collidepoint(event.pos):
						self.done=True
			
			self.screen.blit(self.fond, (0,0))
			
			self.msg.draw_rect(self.screen,(450,75))
			self.msg.draw(self.screen)
			
			self.retour.draw_rect(self.screen,(355,50))
			self.retour.draw(self.screen)
			
			pygame.display.flip()
		
class Player:
	def __init__(self,name):
		self.name=name
		self.score=0
		self.color=beige
		
	def affiche_score(self,x,y,game):
		# Crée une surface et écrit dessus avec la police standard_font en vert 
		text_surface = game.standard_font.render("Score " + self.name+ ": " + str(self.score),1,self.color)

		# Colle la surface text_surface sur la surface d'affichage screen à l'emplacement (20, 30)
		game.screen.blit(text_surface, (x,y) )

		
	
class Game(Scene):
	
	def __init__ (self,title):

		Scene.__init__(self)
		
		button_font = pygame.font.Font(None, 30)
	
		self.button_retour = Option("Retour au menu principal",yellow,brown,(340,580),button_font)
		
		#Chargement et collage du fond
		self.fond = pygame.image.load("fond.jpg").convert()
		
		#définition des dimensions de la table
		(self.width,self.height)=(840,440)

		self.liste_collisions_cueBall=[]
				
		# Change le nom de la fenêtre
		pygame.display.set_caption( title )
		
		# Crée un objet horloge
		self.clock = pygame.time.Clock()
		
		# Initialisation de la police de caractères standard
		self.standard_font = pygame.font.Font(None, 36)
		
		#instanciation de la table
		self.radius=11
		self.table=Rectangle(x0,y0,self.width,self.height,green_bord)
		self.zone=Rectangle(x0+27,y0+27,self.width-54,self.height-54,green_table)
		self.zone0=Rectangle(self.zone.px+13,self.zone.py+13,self.zone.width/4-13,self.zone.height-26,white)
		self.quarter_line=Line([x0+self.zone.width/4+self.radius,y0+34],[x0+self.zone.width/4+self.radius,y0+410],white,1)

		#joueur en cours:
		self.current_player=None

		#instanciation des trous réels
		Circle1=Circle(x0+33,y0+33,18,black)
		Circle2=Circle(x0+self.width/2,y0+20,18,black)
		Circle3=Circle(x0+self.width-33,y0+33,18,black)
		Circle4=Circle(x0+33,y0+self.height-33,18,black)
		Circle5=Circle(x0+self.width/2,y0+self.height-20,18,black)
		Circle6=Circle(x0+self.width-33,y0+self.height-33,18,black)
		
		self.Pockets=[Circle1,Circle2,Circle3,Circle4,Circle5,Circle6]
		
		#instanciation des petits trous virtuels:
		virtual_radius=7
		small_pock_vir1=Circle(x0+33,y0+33,virtual_radius,black)
		small_pock_vir2=Circle(x0+self.width/2,y0+20,virtual_radius,black)
		small_pock_vir3=Circle(x0+self.width-33,y0+33,virtual_radius,black)
		small_pock_vir4=Circle(x0+33,y0+self.height-33,virtual_radius,black)
		small_pock_vir5=Circle(x0+self.width/2,y0+self.height-20,virtual_radius,black)
		small_pock_vir6=Circle(x0+self.width-33,y0+self.height-33,virtual_radius,black)

		self.small_virtual_Pockets=[small_pock_vir1,small_pock_vir2,small_pock_vir3,small_pock_vir4,small_pock_vir5,small_pock_vir6]

#construction des bords de la table:
		#haut à gauche
		point1=(x0+51,y0+27)
		point2=(x0+58,y0+34)
		point3=(x0+397,y0+34)
		point4=(x0+402,y0+27)
		trapeze1=Trapeze([point1,point2,point3,point4],light_blue)
		
		#haut à droite
		point5=(x0+437,y0+27)
		point6=(x0+444,y0+34)
		point7=(x0+783,y0+34)
		point8=(x0+790,y0+27)
		trapeze2=Trapeze([point5,point6,point7,point8],light_blue)
		
		#droite
		point9=(x0+813,y0+51)
		point10=(x0+806,y0+60)
		point11=(x0+806,y0+383)
		point12=(x0+813,y0+390)
		trapeze3=Trapeze([point9,point10,point11,point12],light_blue)
		
		#bas à droite
		point13=(x0+790,y0+414)
		point14=(x0+783,y0+407)
		point15=(x0+444,y0+407)
		point16=(x0+437,y0+414)
		trapeze4=Trapeze([point13,point14,point15,point16],light_blue)
		
		#bas à gauche
		point17=(x0+402,y0+414)
		point18=(x0+397,y0+407)
		point19=(x0+58,y0+407)
		point20=(x0+51,y0+414)
		trapeze5=Trapeze([point17,point18,point19,point20],light_blue)
		
		#gauche
		point21=(x0+27,y0+390)
		point22=(x0+34,y0+383)
		point23=(x0+34,y0+60)
		point24=(x0+27,y0+51)
		trapeze6=Trapeze([point21,point22,point23,point24],light_blue)
		
		self.extremities_t1=[(0,1),(1,1),(2,2)]
		self.extremities_t2=[(3,1),(4,1),(5,2)]
		self.extremities_t3=[(0,2),(1,2),(5,1)]
		self.extremities_t4=[(2,1),(3,2),(4,2)]
		
		self.edges=[trapeze1,trapeze2,trapeze3,trapeze4,trapeze5,trapeze6]
		
		for trapeze in self.edges:
			pass
		self.cue_display=True
		self.hold_ball=False
		self.cue_display0=True
		self.new_turn=False
		self.ball_fallen=False
		p1=Player("joueur 1")
		p2=Player("joueur 2")
		self.players=[ p1 , p2 ]
		self.current_player = self.players.index(p1)
		
		self.clock = pygame.time.Clock()
		
	def quit(self):
		# Libération des ressources alloués par pygame
		pygame.quit ()
		
	def clic(self,position):
		return
					
	def release(self):
		return
				
	def mouse_movement(self,position):
		return
	
	def change_player(self):
		self.current_player=(self.current_player+1) % 2
	
	def periodic(self):
		return
		
	def run(self):
		self.hold_ball= False
		self.done=False
		while self.done == False:
			for event in pygame.event.get():
				#fermeture du programme
				if event.type == pygame.QUIT:
					self.done=True
					self.destroy_all=True
					
					
				#manipulation de la queue avec la souris		
				elif event.type==pygame.MOUSEBUTTONDOWN:
					self.clic(event.pos)
										
				elif  event.type == pygame.MOUSEBUTTONUP: 
					self.release()
					
				elif event.type == pygame.MOUSEMOTION:
					self.mouse_movement(event.pos)
					
			self.periodic()
			if len(self.world)==1:
				fin_jeu=End_Game(self.players)
				fin_jeu.run()
				self.done= True
				
			self.button_retour.draw_rect(self.screen,(260,40))
			self.button_retour.draw(self.screen)
			
			pygame.display.flip()
			self.clock.tick(FPS)
			
class Snooker(Game):
	def __init__ (self):
		global sound_cue_ball
		global sound_ball_ball
		global sound_ball_fall
		global sound_ball_border
		global sound_error
		global sound_clapping
		global sound_end
		
		Game.__init__(self,"SMYL Pool")
		
		#Chargement des effets sonores 
		sound_cue_ball=pygame.mixer.Sound("cue.wav")
		sound_ball_ball=pygame.mixer.Sound("ball.wav")
		sound_ball_fall=pygame.mixer.Sound("fall.wav")
		sound_ball_border=pygame.mixer.Sound("border.wav")
		sound_error=pygame.mixer.Sound("error.wav")
		sound_clapping=pygame.mixer.Sound("clapping.wav")
		sound_end=pygame.mixer.Sound("son_fin.wav")
		
	#instanciation des balles
		self.radius=11
		pos1=x0+0.75*self.width+8*(self.radius+1)
		#cue ball
		self.b_white=Ball(x0+600,y0+280,self.radius,white,None)
		#red balls
		self.b_red1=Ball(pos1,y0+self.height/2-2*(2*self.radius+2),self.radius,red,1)
		self.b_red2=Ball(pos1,y0+self.height/2-2*(self.radius+1),self.radius,red,1)
		self.b_red3=Ball(pos1,y0+self.height/2,self.radius,red,1)
		self.b_red4=Ball(pos1,y0+self.height/2+2*(self.radius+1),self.radius,red,1)
		self.b_red5=Ball(pos1,y0+self.height/2+2*(2*self.radius+2),self.radius,red,1)
		self.b_red6=Ball(pos1-2*(self.radius+1),y0+self.height/2-3*(self.radius+1),self.radius,red,1)
		self.b_red7=Ball(pos1-2*(self.radius+1),y0+self.height/2-self.radius-1,self.radius,red,1)
		self.b_red8=Ball(pos1-2*(self.radius+1),y0+self.height/2+self.radius+1,self.radius,red,1)
		self.b_red9=Ball(pos1-2*(self.radius+1),y0+self.height/2+3*(self.radius+1),self.radius,red,1)
		self.b_red10=Ball(pos1-2*(2*self.radius+2),y0+self.height/2-2*(self.radius+1),self.radius,red,1)
		self.b_red11=Ball(pos1-2*(2*self.radius+2),y0+self.height/2,self.radius,red,1)
		self.b_red12=Ball(pos1-2*(2*self.radius+2),y0+self.height/2+2*(self.radius+1),self.radius,red,1)
		self.b_red13=Ball(pos1-2*(3*self.radius+3),y0+self.height/2-self.radius-1,self.radius,red,1)
		self.b_red14=Ball(pos1-2*(3*self.radius+3),y0+self.height/2+self.radius+1,self.radius,red,1)
		self.b_red15=Ball(x0+0.75*self.width,y0+self.height/2,self.radius,red,1)
		#colored balls
		self.b_pink=Ball(x0+0.75*self.width-2*(self.radius+4),y0+self.height/2,self.radius,pink,6)
		self.b_black=Ball(pos1+2*(self.radius+2),y0+self.height/2,self.radius,black,7)
		self.b_blue=Ball(x0+self.width/2,y0+self.height/2,self.radius,blue,5)
		self.b_green=Ball(x0+self.width/4,y0+self.height/2-4*self.radius,self.radius,green,3)
		self.b_brown=Ball(x0+self.width/4,y0+self.height/2,self.radius,brown,4)
		self.b_yellow=Ball(x0+self.width/4,y0+self.height/2+4*self.radius,self.radius,yellow,2)

		
		"""self.world=[self.b_white,self.b_red1,self.b_red2,self.b_red3,self.b_red4,self.b_red5,self.b_red6,self.b_red7,self.b_red8,self.b_red9,\
			       self.b_red10,self.b_red11,self.b_red12,self.b_red13,self.b_red14,self.b_red15,self.b_pink,self.b_black,self.b_blue,\
			       self.b_green,self.b_brown,self.b_yellow]"""
			       
		self.world=[self.b_white,self.b_red7,self.b_pink,self.b_black,self.b_blue]
			       
		self.cue=Cue(self,(x0+100,y0-15),(x0+200,y0-15))
		
		self.no_more_reds=True
		self.fin_tir=False
		self.last_fallen_ball=self.b_white
		
	def red_balls (self,ball):
		
		try:
			if ball.vx!=0 and ball.vy!=0 :
				self.world.remove(ball)
				if ball!=self.b_white:
				
					if self.last_fallen_ball.color!=red:
						if ball.color==red:
							self.players[self.current_player].score+=ball.value
						else:
							self.players[self.current_player].score+=-2
					else:
						self.players[self.current_player].score+=ball.value
					
					if ball.color!=red:
						(ball.px,ball.py)=(ball.x0,ball.y0)
						(ball.vx,ball.vy)=(0,0)
						self.world.append(ball)
					
				else:
					self.players[self.current_player].score+=-2
				sound_ball_fall.play()
				
				if ball.color==white:
					sound_error.play()
				else:
					if self.last_fallen_ball.color==red:
						if ball.color!=red:
							sound_clapping.play()
						else:
							sound_error.play()
					else:
						if ball.color==red:
							sound_clapping.play()
						else:
							sound_error.play()
							
				self.last_fallen_ball=ball
		except:
			pass
	
	def no_red_balls(self,ball):			
		try:
			if ball.vx!=0 and ball.vy!=0 :
				self.world.remove(ball)
				if ball!=self.b_white:
					if ball.value==self.existing_balls[0]:
						self.players[self.current_player].score+=ball.value
					else:
						self.players[self.current_player].score+=-2
						(ball.px,ball.py)=(ball.x0,ball.y0)
						(ball.vx,ball.vy)=(0,0)
						self.world.append(ball)
				else:
					self.players[self.current_player].score+=-2
				sound_ball_fall.play()
				
				if ball.color==white:
					sound_error.play()
				else:
					if ball.value==self.existing_balls[0]:
						sound_clapping.play()
					else:
						sound_error.play()
				
		except:
			pass
		
	def clic(self,position):
		if self.button_retour.rect.collidepoint(position):
			self.done=True
			
		if self.cue_display:
			self.cue.handle(position)
			
		if self.hold_ball:
			self.superposed=False
			index=0
			while index<len(self.world) and self.superposed==False:
				if self.world[index]!=self.b_white:
					self.superposed= self.world[index].mingled(self.b_white)
				index+=1
				
			self.in_Circle=False
			index=0
			while index<len(self.Pockets) and self.in_Circle==False:
				if self.Pockets[index]!=self.b_white:
					self.in_Circle= self.Pockets[index].mingled(self.b_white)
				index+=1
					
			if self.zone0.contains(position[0],position[1]) and self.superposed==False and self.in_Circle==False:
				self.hold_ball=False
				self.cue_display=True
				
	def release(self):
		if self.cue_display:
			if self.cue.handled==True:
				if self.cue.l-self.cue.l0  !=0:
					self.cue.hitball(self.b_white.px,self.b_white.py)
				else:
					self.cue.handled=False
				
	def mouse_movement(self,position):
		if self.hold_ball:
			self.b_white.px = position[0]
			self.b_white.py = position[1]
					
		if self.cue_display and not self.cue.released:
			(mx, my) = position
			self.cue.update(mx,my,self.b_white)
		
	def periodic(self):
		
		self.screen.blit(self.fond, (0,0))
		self.all_balls_not_moving=True
		self.existing_balls=[]
		
		for b in self.world:
			if b.color!=white:
				self.existing_balls.append(b.value)
		
		self.existing_balls.sort()
		self.no_more_reds=True
		
		for ball in self.world:
			if ball.value==1:
				self.no_more_reds=False
				break
		
		for ball in self.world:
			if ball.vx!=0 and ball.vy!=0:
				self.all_balls_not_moving=False
				break
			
		self.cue_display=self.all_balls_not_moving and self.b_white.ready and self.hold_ball==False
		self.new_turn=not self.cue_display0 and self.cue_display
		if self.new_turn:
			self.cue.update(0,0,self.b_white)
			
		#traçage de la table
		self.table.draw(self.screen)
		self.zone.draw(self.screen)
		self.quarter_line.draw(self.screen)
		
		for hole in self.small_virtual_Pockets:
			for ball in self.world:
				for point in  ball.points:
					if hole.contains(point[0],point[1]) and self.hold_ball == False:
						if self.no_more_reds:
							self.no_red_balls(ball)
						else:
							self.red_balls(ball)
						self.ball_fallen=True
				
		#traçage trous
		for element in self.Pockets+self.edges :
			element.draw(self.screen)
				
				
		#mise à jour du traçage des objets en mvt
		for object in self.world:
			object.update(self.world,self.liste_collisions_cueBall,self.edges,self.extremities_t1,self.extremities_t2,self.extremities_t3,self.extremities_t4)
			object.draw(self.screen)
		
		if self.cue_display:	
			
			#traçage de la queue		
			if self.cue.released:
				self.cue.update_on_release(self.b_white,self)
			self.cue.draw(self.screen)
			
			
			if self.new_turn:
				if  self.liste_collisions_cueBall!=[]:
					if self.liste_collisions_cueBall[0]!=self.existing_balls[0]:
						self.players[self.current_player].score+=-1
						self.change_player()
					elif  self.ball_fallen==False:
						self.change_player()
					elif self.last_fallen_ball.value!=self.existing_balls[0]:
						self.change_player()
				else:
					self.change_player()
				self.ball_fallen=False	
				self.last_fallen_ball=self.b_white
			if self.hold_ball==False:
					self.liste_collisions_cueBall=[]
				
		else:
			
			if self.b_white not in self.world:
					(self.b_white.px,self.b_white.py)=(x0+self.width/4 ,y0+self.height/2)
					(self.b_white.vx,self.b_white.vy)=(0,0)
					self.world.append(self.b_white)
					self.hold_ball= True
	
			
		self.players[self.current_player].color=red
		self.players[(self.current_player+1) % 2].color=beige
			
		self.players[0].affiche_score(120,20,self)
		self.players[1].affiche_score(650,20,self)	
		self.cue_display0=self.cue_display	
# programme principal
S = Scene_debut()
S.run()
S.quit()