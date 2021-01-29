#!/usr/bin/env python
# coding: utf-8

# # Fagdag 27.01.2021

# In[2]:


# 7.3
def trapes(f, a, b, n):
    h = (b-a)/n                 # grunnflaten til trapesene
    integral = (f(a)+f(b))/2    # høydene
    for i in range (1,n):       
        integral += f(a + i*h)
    return h*integral

def f(x):
    return 2+x

print(trapes(f,1,5,3))


# In[43]:


from pylab import *
from math import *

# 7.9 a)
def T(t):
    return 70*math.exp((-0.065*t))

def newtons_k(f,x,h):
    f_derivert = (f(x+h)-f(x))/h
    return f_derivert 

stigning = []
tid = []
h = 60/1000

for i in range (1,1000):
    deltaT = newtons_k(T,(i - 1)*h,h)
    stigning.append(deltaT)
    tid.append(i*h)

plot(tid, stigning)
show()

# b)
plot(tid, stigning, label = "Derivert", color = "cyan")
temperatur = [T(v) for v in tid]
plot(tid, temperatur, label = "Temperatur")
legend()
show()

# c)
print("Ved element nr 42 synker temperaturen med ", round(abs(temperatur[42] - temperatur[41]),2),"°C.")


# In[60]:


data = loadtxt(r'C:\Users\straw\OneDrive\Dokumenter\Programmering\Oppgaver\posisjon.txt',skiprows=1)
tid = data[:,0]
posisjon = data[:,1]

def der(x, x_0, delta):
    return (x - x_0)/delta

lengde = len(tid)
hastighet = []
akselerasjon = []
for i in range(1, lengde):
    derivert = der(posisjon[i], posisjon[i-1], (tid[i]-tid[i-1]))
    hastighet.append(derivert)

for i in range(1, lengde-1):
    dobbelt_derivert = der(hastighet[i-1], hastighet[i], (tid[i]-tid[i-1]))
    akselerasjon.append(dobbelt_derivert)

has = array(hastighet)
aks = array(akselerasjon)

plot(tid[:-1], has, label = "Hastighet", color = "limegreen")
plot(tid[:-2], aks, label = "Akselerasjon", color = "cyan")
legend()
show()


# Deriver følgende funksjoner med Newtons kvotient. Plottfunksjoneneforx∈[2,5). Kontroller ved å derivere for hånd.
# 1.f(x) =2x+1
# 2.f(x) =x^2−4x+5
# 3.f(x) =e^x
# 4.f(x) =e^x−5x
# 5.f(x) =6√x−x
# 6.f(x) =5e^(−2x)
# 7.f(x) =√ln(x)
# 8.f(x) =4 ln(x^2)
# 9.f(x) =4·5^(x^3−2x)
# 
# Integrer funksjonene i oppgave 7.1 ved hjelp av rektangelmetoden og trapesmetoden. Sammenlikn svarene.
# 
# Legg 7.3, 7.9, 7.12 og 7.14 på GitHub som en Jupyter-fil. Skriv også en teoridel der du gjør rede for hva forskjellen på analytisk og numerisk derivasjon er, og hva numerisk integrasjon er. Gjør også rede for hvorfor tilnærmingene dine varierer med dx (derivasjon) og n (integrasjon). Leveres i løpet av fagdagen eller i løpet av uka, hvis du ikke rekker å bli ferdig.

# In[78]:


from math import *

def rekt(f, a, b, n):
    A = 0           
    h = (b-a)/n      
    for i in range (1, n):
        A += f(a + h*i)
    return A*h
    

def trapes(f, a, b, n):
    h = (b-a)/n
    integral = (f(a) + f(b))/2.0
    for i in range(1, n):
        integral += f(a + h*i)
    return integral*h

""" Oppgave 7.14 (uten å ha sett kommentar)
def f(x):
    return 2*x-1

def g(x):
    return x**2-4*x+5

def h(x):
    return exp(x)

def i(x):
    return exp(x)-5*x

def j(x):
    return 6*sqrt(x)-x

def k(x):
    return 5*exp(-2*x)

def l(x):
    return sqrt(log(x))

def m(x):
    return 4*log(x**2)

def n(x):
    return 4*5**(x**3-2*x)

print("integraler fra 2-5 ved bruk av rektangelmetoden: ","\n integral 2*x-1 =",round(rekt(f,2,5,10),2),"\n integral x**2-4*x+5 =",round(rekt(g,2,5,10),2),"\n integral e^x =",round(rekt(h,2,5,10),2),"\n integral e^x-5*x =",round(rekt(i,2,5,10),2),"\n integral 6√x−x =",round(rekt(j,2,5,10),2),"\n integral 5e^(−2x) =",round(rekt(k,2,5,10),2),"\n integral √ln(x) =",round(rekt(l,2,5,10),2),"\n inregral 4·ln(x^2) =",round(rekt(m,2,5,10),2),"\n inregral 4·5^(x^3−2x) =",round(rekt(n,2,5,10),2))
print("")
print("integraler fra 2-5 ved bruk av trapesmetoden: ","\n integral 2*x-1 =",round(trapes(f,2,5,10),2),"\n integral x**2-4*x+5 =",round(trapes(g,2,5,10),2),"\n integral e^x =",round(trapes(h,2,5,10),2),"\n integral e^x-5*x =",round(trapes(i,2,5,10),2),"\n integral 6√x−x =",round(trapes(j,2,5,10),2),"\n integral 5e^(−2x) =",round(trapes(k,2,5,10),2),"\n integral √ln(x) =",round(trapes(l,2,5,10),2),"\n inregral 4·ln(x^2) =",round(trapes(m,2,5,10),2),"\n inregral 4·5^(x^3−2x) =",round(trapes(n,2,5,10),2))
"""

def o(x):
    return 0.0005*x**3 + 0.04*x**2 + 2

analytisk = 7.63613  # brukte geogebra
integral=[]
print("integral fra 2-5 av funksjonen 0.0005x**3 + 0.04*x**2 + 2 for ulike n-verdier:\n ")
for i in range (2,11):
    print("n=", i, ", rektangulær integral = ",round(rekt(o,2,5,i),5), " trapes integral = ",round(trapes(o,2,5,i),5))


# Ut ifra resultatene kan man se at integralet vi fikk ved større n-verdi nermere det analytiske integralet: 7.63613
# Samtidig kan man også se at inegralet vi fikk ut ifra trapesmetoden var en mye bedre tilnærming enn rektangelmetoden.
# Dermed kan vi konkludere at man får et mer nøyaktig svar når man øker antall rektangler/trapeser man beregner arealet med.

# ## Teori del 
# 
# analytisk derivasjon er derivasjon der man tar i bruk grenseverdier for å finne en generell og eksakt verdi av stigningen til grafen, mens numerisk derivasjon tilnærmer grenseverdiene for å få ikke en eksakt verdi, men en verdi som er nerme nok. 
# 
# Tilnærmingene av den deriverte vil variere med delta x siden den deriverte er definert ved å bringe tangentene til 2 punkter på en graf så nærme at de nesten er lik hverandre og har nesten samme stigning. Derfor vil den momentane vekstfarten være mer nøyaktig jo mindre delta x (forskjellen i x-koordinatene) er.
# 
# Tilnærmingene av intergrasjonen til en graf vil variere med n siden n bestemmer hvor mange figurer arealet under grafen deles opp i. Jo færre figurer, jo bredere vil de være, og dermed vil også unøyaktigheten stige, siden mye av arealet figurene dekker kan enten være utenfor grafen eller ikke dekke hele grafen. Men med færre figurer, blir figurene også bli smalere, og dermed romme mer av arealet under grafen og mindre av arealet over grafen. Detfor vil integralet bli mer nøyaktig jo større n man har.

# In[ ]:




