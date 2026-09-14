"""Cesta světla – plošinovka v pygame. Spusť: python main.py"""
import math, os, sys, pygame

WIDTH, HEIGHT, FPS = 1280, 720, 60
ASSETS = os.path.join(os.path.dirname(__file__), "assets")
GRAVITY, SPEED, JUMP = 2100, 390, 790
SKY_A, SKY_B, INK, GOLD = (49,113,213), (196,231,255), (26,43,73), (255,205,67)
LEVELS = [
 ("Nazaret", [(0,620,1280,100),(260,510,180,25),(560,430,150,25),(810,520,190,25),(1080,390,150,25)], [(170,555),(305,445),(370,445),(605,365),(670,365),(855,455),(935,455),(1130,325)]),
 ("Galilea", [(0,620,1280,100),(145,500,145,25),(390,415,135,25),(635,500,160,25),(885,390,145,25),(1100,480,130,25)], [(185,435),(245,435),(430,350),(485,350),(675,435),(745,435),(925,325),(985,325),(1140,415),(1195,415)]),
 ("Hora radosti", [(0,620,1280,100),(115,520,130,25),(330,440,120,25),(540,350,155,25),(780,450,130,25),(1000,340,180,25)], [(150,455),(205,455),(365,375),(415,375),(575,285),(625,285),(670,285),(815,385),(875,385),(1040,275),(1100,275),(1150,275)])]

def load_sprite():
 try: return pygame.transform.smoothscale(pygame.image.load(os.path.join(ASSETS,"jesus.png")).convert_alpha(),(86,124))
 except pygame.error: return None

class Player:
 def __init__(self,sprite): self.sprite=sprite; self.rect=pygame.Rect(80,500,55,92); self.pos=pygame.Vector2(self.rect.topleft); self.vel=pygame.Vector2(); self.ground=False; self.face=1
 def reset(self): self.rect.topleft=(80,500); self.pos.xy=self.rect.topleft; self.vel.xy=(0,0)
 def update(self,dt,platforms):
  k=pygame.key.get_pressed(); d=int(k[pygame.K_RIGHT] or k[pygame.K_d])-int(k[pygame.K_LEFT] or k[pygame.K_a]); self.vel.x=d*SPEED
  if d:self.face=d
  if self.ground and (k[pygame.K_SPACE] or k[pygame.K_w] or k[pygame.K_UP]):self.vel.y=-JUMP;self.ground=False
  self.vel.y=min(1050,self.vel.y+GRAVITY*dt); self.pos.x+=self.vel.x*dt; self.rect.x=round(self.pos.x)
  for p in platforms:
   if self.rect.colliderect(p): self.rect.right=p.left if self.vel.x>0 else self.rect.right; self.rect.left=p.right if self.vel.x<0 else self.rect.left; self.pos.x=self.rect.x
  self.pos.y+=self.vel.y*dt; self.rect.y=round(self.pos.y);self.ground=False
  for p in platforms:
   if self.rect.colliderect(p):
    if self.vel.y>0:self.rect.bottom=p.top;self.ground=True
    else:self.rect.top=p.bottom
    self.vel.y=0;self.pos.y=self.rect.y
  self.rect.left=max(0,min(WIDTH-self.rect.width,self.rect.left));self.pos.x=self.rect.x
 def draw(self,s):
  pygame.draw.ellipse(s,(35,70,60),(self.rect.centerx-25,self.rect.bottom-7,50,11))
  if self.sprite:
   pic=self.sprite if self.face>0 else pygame.transform.flip(self.sprite,True,False);s.blit(pic,pic.get_rect(midbottom=self.rect.midbottom))
  else:
   pygame.draw.circle(s,(115,70,43),(self.rect.centerx,self.rect.y+18),18);pygame.draw.circle(s,(238,193,150),(self.rect.centerx,self.rect.y+20),14);pygame.draw.rect(s,(247,239,205),(self.rect.x+9,self.rect.y+34,37,48),border_radius=12);pygame.draw.rect(s,(76,135,185),(self.rect.x+31,self.rect.y+36,9,46))

class Game:
 def __init__(self):
  pygame.init();pygame.display.set_caption("Cesta světla");self.screen=pygame.display.set_mode((WIDTH,HEIGHT));self.clock=pygame.time.Clock();self.font={"title":pygame.font.SysFont("georgia",58,True),"big":pygame.font.SysFont("arial",29,True),"ui":pygame.font.SysFont("arial",20,True),"small":pygame.font.SysFont("arial",16,True)};self.player=Player(load_sprite());self.state="menu";self.index=self.score=0;self.platforms=[];self.coins=[]
 def start(self,i=0):
  self.index=i;self.score=0;self.state="play";self.player.reset();name,p,c=LEVELS[i];self.platforms=[pygame.Rect(x) for x in p];self.coins=[(pygame.Vector2(x,y),False,n*.55) for n,(x,y) in enumerate(c)]
 def event(self,e):
  if e.type==pygame.QUIT:pygame.quit();sys.exit()
  if e.type==pygame.KEYDOWN:
   if e.key==pygame.K_ESCAPE:self.state="menu"
   if e.key==pygame.K_r and self.state=="play":self.start(self.index)
   if self.state=="menu" and e.key in (pygame.K_RETURN,pygame.K_SPACE):self.start()
   if self.state=="complete" and e.key in (pygame.K_RETURN,pygame.K_SPACE):self.start((self.index+1)%len(LEVELS))
 def update(self,dt):
  if self.state!="play":return
  self.player.update(dt,self.platforms)
  for n,(pos,taken,phase) in enumerate(self.coins):
   if not taken and self.player.rect.inflate(12,12).collidepoint(pos):self.coins[n]=(pos,True,phase);self.score+=1
  if self.player.rect.top>HEIGHT:self.start(self.index)
  if self.score==len(self.coins):self.state="complete"
 def text(self,v,k,c,p,center=True):
  a=self.font[k].render(v,True,c);self.screen.blit(a,a.get_rect(center=p) if center else p)
 def sky(self):
  for y in range(HEIGHT):
   t=y/HEIGHT;c=tuple(int(SKY_A[i]*(1-t)+SKY_B[i]*t) for i in range(3));pygame.draw.line(self.screen,c,(0,y),(WIDTH,y))
  pygame.draw.circle(self.screen,(255,239,165),(1070,118),54)
  for x,y,z in [(110,150,1),(420,105,.7),(720,175,.9)]:pygame.draw.ellipse(self.screen,(255,255,255),(x,y,110*z,33*z));pygame.draw.circle(self.screen,(255,255,255),(int(x+42*z),int(y),int(24*z)))
  pygame.draw.polygon(self.screen,(112,177,122),[(0,540),(230,405),(480,535),(690,390),(900,535),(1120,415),(1280,505),(1280,720),(0,720)])
 def platform(self,p):
  pygame.draw.rect(self.screen,(92,112,67),p.move(0,7),border_radius=7);pygame.draw.rect(self.screen,(180,127,74),p,border_radius=7);pygame.draw.rect(self.screen,(105,167,77),(p.x,p.y,p.width,9),border_radius=6)
 def draw(self,t):
  self.sky()
  if self.state=="menu":
   self.text("CESTA SVĚTLA","title",(255,252,231),(640,215));self.text("Ježíš a ztracené mince","big",GOLD,(640,275));self.text("Pohyb: A/D nebo ←/→     Skok: mezerník / W / ↑","ui",(255,255,255),(640,355));pygame.draw.rect(self.screen,GOLD,(510,420,260,65),border_radius=22);self.text("ZAČÍT HRU","big",INK,(640,452));self.text("Stiskni ENTER nebo MEZERNÍK","small",(255,255,255),(640,525));return
  for p in self.platforms:self.platform(p)
  for pos,taken,phase in self.coins:
   if not taken:
    x,y=pos.x,pos.y+math.sin(t*4+phase)*5;pygame.draw.circle(self.screen,(171,116,24),(x,y+3),14);pygame.draw.circle(self.screen,GOLD,(x,y),13);pygame.draw.circle(self.screen,(255,238,128),(x-4,y-4),4)
  self.player.draw(self.screen);self.text(LEVELS[self.index][0],"big",(255,255,255),(640,35));self.text(f"MINCE  {self.score} / {len(self.coins)}","ui",(255,255,255),(30,29),False);self.text("R — od začátku     ESC — menu","small",(255,255,255),(1000,30),False)
  if self.state=="complete":
   b=pygame.Rect(360,235,560,200);pygame.draw.rect(self.screen,(29,55,88),b,border_radius=28);pygame.draw.rect(self.screen,GOLD,b,3,border_radius=28);self.text("ÚROVEŇ DOKONČENA!","big",(255,255,255),(640,295));self.text("Všechny mince jsou zachráněné.","ui",(255,255,255),(640,337));self.text("ENTER / MEZERNÍK — další úroveň","ui",GOLD,(640,390))
 def run(self):
  t=0
  while 1:
   dt=self.clock.tick(FPS)/1000;t+=dt
   for e in pygame.event.get():self.event(e)
   self.update(dt);self.draw(t);pygame.display.flip()
if __name__=="__main__":Game().run()
