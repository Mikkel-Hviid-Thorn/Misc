# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 19:48:07 2020

@author: Mikkel Hviid Thorn og Rebekka Engelund Balle


Information
Lufthavnen:
- Har en landingsbane.
- Vil måske have to landingsbaner.

Følgende observationer er givet:
- Der ankommer gennemsnitlig 200 fly i det nulte år.
- Flyene ankommer i et interval af 13 timer.
- Fly ankommer tilfældigt i intervallet, altså uniformt fordelt.
- Der er givet en observation af landingstider over en enkelt dag.

Lufthavnen forventer:
- At flytrafikken stiger med 5% hvert år.


Ordbog
- f og fly står for flyene
- l, m, n er diskrete antal
- LB står for landingsbane
- ventetider er tiden et fly skal vente før det kan lande, hvor tiden kun tælles, hvis den er forskelligt for nul.
- fly_der_venter er brøkdelen af fly som venter.
- over_lukketid er den tid, hvor sidste fly er landet, relativt til de 13 timer.


Data som simuleringen danner
- ventetider for fly
- antallet af fly der venter
"""


import numpy as np
import numpy.random as npr

npr.seed(1)


"""
Første sektion indeholder en funktion, som danner fly.
"""


def fly(n):
    """
    Danner x fly, hvor x er en stokatisk variabel for en poisson fordeling med lambda = n.
    Hvert fly er en liste med en ankomsttid i første index og landingstid i andet index.
    Flyene er arangeret i forhold til ankomsttiden, så det første fly ankommer først.

    Input
    n -> er lambda værdien i vores poisson fordeling. Det skal symbolisere den gennemsnitlige mængde fly.

    Output
    f -> en liste af x fly.
    
    Eksempel
    >>> fly(3)
    array([[11090,   177],
           [24876,    81]])
    
    >>> fly(3)
    array([[ 1003,   101],
           [29724,   138]])
    """
    
    x = npr.poisson(n) #antal fly
    
    ankomsttider = np.sort(npr.randint(0, 13*60*60, size = x)) #liste med ankomsttider
    
    #liste med landingstider
    landingstider = npr.choice(np.arange(8), size = x, p = [16/200, 33/200, 61/200, 41/200, 25/200, 10/200, 8/200, 6/200])
    landingstider = [npr.randint(i*30+31, (i+2)*30) for i in landingstider]
    
    f = np.transpose([ankomsttider,landingstider]) #liste med fly
    return f


"""
Anden sektion indeholder funktioner, som simulerer lufthavnen med en landingsbane.
"""


def en_dag(n):
    """
    Simulerer en dag i lufthavnen. Funktionen arbejder med en liste fly.

    Input
    n -> skal symbolisere den gennemsnitlige mængde fly.

    Output
    ventetider -> en liste med ventetiderne for alle fly, som skal vente med at lande.
    len(ventetider)/len(fly_liste) -> brøkdelen af fly, som skal vente med at lande.
    LB - 13*60*60 -> hvornår det sidste fly er landet i forhold til lukketid.
    
    Eksempel
    >>> en_dag(50)
    ([188, 49, 11, 22, 22, 93, 110], 0.14583333333333334, -242)
    
    >>> en_dag(50)
    ([1, 43, 57], 0.07142857142857142, -70)
    """
    
    fly_liste = fly(n) #setup
    LB, ventetider = 0, []
    
    for f in fly_liste: #simulerer en dag ved at tjekke status på lufthavnen hver gang et fly ankommer
        if f[0] < LB: #landingsbanen er optaget
            ventetider.append(LB-f[0])
            LB += f[1]
        else: #landingsbanen er fri
            LB = np.sum(f)
            
    return ventetider, len(ventetider)/len(fly_liste), LB - 13*60*60


def m_dage(m,n):
    """
    Simulerer m dage i lufthavnen. 
    Funktionen gentager en_dag funktionen m gange.

    Input
    m -> antallet af dage simuleret.
    n -> skal symbolisere den gennemsnitlige mængde fly.

    Output
    liste_mean_ventetider -> en liste med gennemsnitlig ventetid for alle fly, som skal vente med at lande, hver dag.
    liste_fly_der_venter -> en liste over brøkdelen af fly, som skal vente med at lande, hver dag.
    liste_over_lukketid -> en liste over hvornår det sidste fly er landet i forhold til lukketid hver dag.
    
    Eksempel
    >>> m_dage(3,50)
    ([65.28571428571429, 77.44444444444444, 67.75], [0.1320754716981132, 0.1836734693877551, 0.1509433962264151], [112, -12, -2579])
    
    >>> m_dage(3,50)
    ([92.66666666666667, 72.0, 94.5], [0.13043478260869565, 0.10638297872340426, 0.0392156862745098], [-771, 26, -568])
    """
    
    liste_ventetider, liste_fly_der_venter, liste_over_lukketid = [], [], [] #setup
    
    for i in range(0,m): #gentager simuleringen i en_dag funktionen m gange
        ventetider, fly_der_venter, over_lukketid = en_dag(n)
        liste_ventetider.append(ventetider)
        liste_fly_der_venter.append(fly_der_venter)
        liste_over_lukketid.append(over_lukketid)
    
    liste_mean_ventetider = [np.mean(vt) for vt in liste_ventetider] #tager den gennemsnitlige ventetid for hver dag
    
    return liste_mean_ventetider, liste_fly_der_venter, liste_over_lukketid


def l_år(l,m,n):
    """
    Simulerer l år i lufthavnen.
    Funktionen gentager m_dage funktionen l gange, hvor det gennemsnitlige antal fly stiger for hver iteration.
    Stigningen er på 5% hvert år og udregnes med renteformlen.
    Outputtet er to todimensionelle lister.

    Input
    l -> antallet af år simuleret.
    m -> antallet af dage simuleret.
    n -> skal symbolisere den gennemsnitlige mængde fly.

    Output
    liste_ventetider -> en liste med gennemsnitlig ventetid for alle fly, som skal vente med at lande, hver dag for l år.
    liste_fly_der_venter -> en liste over brøkdelen af fly, som skal vente med at lande, hver dag for l år.
    liste_over_lukketid -> en liste over hvornår det sidste fly er landet i forhold til lukketid hver dag for l år.
    
    Eksempel
    >>> l_år(3,3,50)
    ([[117.2, 56.25, 87.33333333333333], [134.75, 83.33333333333333, 79.85714285714286], [96.25, 63.0, 133.88888888888889], [46.25, 86.36363636363636, 71.875]], [[0.10204081632653061, 0.08695652173913043, 0.16363636363636364], [0.07142857142857142, 0.16071428571428573, 0.16666666666666666], [0.0975609756097561, 0.14285714285714285, 0.16363636363636364], [0.10256410256410256, 0.15714285714285714, 0.1702127659574468]], [[-1716, -82, -1359], [-2334, -2567, -1754], [-52, 85, -890], [-1677, -2028, -4875]])
    
    >>> l_år(3,3,50)
    ([[127.9090909090909, 78.0, 76.75], [117.77777777777777, 47.0, 55.625], [105.5, 93.0, 33.666666666666664], [62.57142857142857, 75.28571428571429, 104.08333333333333]], [[0.21568627450980393, 0.15517241379310345, 0.1568627450980392], [0.15789473684210525, 0.16279069767441862, 0.17777777777777778], [0.12, 0.0392156862745098, 0.058823529411764705], [0.12280701754385964, 0.12727272727272726, 0.18461538461538463]], [[-138, 131, -1806], [-21, -25, -309], [-283, -765, -250], [-509, -839, 160]])
    """
    
    liste_ventetider, liste_fly_der_venter, liste_over_lukketid = [], [], [] #setup
    
    for i in range(0,l+1): #gentager simuleringen i m_dage funktionen l gange
         ventetider, fly_der_venter, over_lukketid = m_dage(m,int(n*(1.05)**i))
         liste_ventetider.append(ventetider)
         liste_fly_der_venter.append(fly_der_venter)
         liste_over_lukketid.append(over_lukketid)
         
    return liste_ventetider, liste_fly_der_venter, liste_over_lukketid


"""
Tredje sektion indeholder funktioner, som simulerer lufthavnen med to landingsbaner.
"""


def en_dag_2LB(n):
    """
    Simulerer en dag i lufthavnen med to landingsbaner. Funktionen arbejder med en liste fly.

    Input
    n -> skal symbolisere den gennemsnitlige mængde fly.

    Output
    ventetider -> en liste med ventetiderne for alle fly, som skal vente med at lande.
    len(ventetider)/len(fly_liste) -> brøkdelen af fly, som skal vente med at lande.
    LB - 13*60*60 -> hvornår det sidste fly er landet i forhold til lukketid.
    
    Eksempel
    >>> en_dag_2LB(80)
    ([12], 0.012345679012345678, 62)
    
    >>> en_dag_2LB(120)
    ([21, 88, 9, 16, 6, 19], 0.05454545454545454, -116)
    """
    
    fly_liste = fly(n) #setup
    LB1, LB2, ventetider = 0, 0, []
    
    for f in fly_liste: #simulerer en dag ved at tjekke status på lufthavnen hver gang et fly ankommer
        if f[0] < LB1: #tjekker om landingsbanerne er optaget
            if f[0] < LB2:    
                if LB1 <= LB2:
                    ventetider.append(LB1-f[0])
                    LB1 += f[1]
                elif LB2 < LB1:
                    ventetider.append(LB2-f[0])
                    LB2 += f[1]
                    
            else: #landingsbaneren er ikke optaget
                LB2 = np.sum(f)
        else:
            LB1 = np.sum(f)
    
    if LB2 < LB1: #finder den landingsbaner som lukker sidst
        LB = LB1
    else:
        LB = LB2
    
    return ventetider, len(ventetider)/len(fly_liste), LB - 13*60*60


def m_dage_2LB(m,n):
    """
    Simulerer m dage i lufthavnen med to landingsbaner. 
    Funktionen gentager en_dag funktionen m gange.

    Input
    m -> antallet af dage simuleret.
    n -> skal symbolisere den gennemsnitlige mængde fly.

    Output
    liste_mean_ventetider -> en liste med gennemsnitlig ventetid for alle fly, som skal vente med at lande, hver dag.
    liste_fly_der_venter -> en liste over brøkdelen af fly, som skal vente med at lande, hver dag.
    liste_over_lukketid -> en liste over hvornår det sidste fly er landet i forhold til lukketid hver dag.
    
    Eksempel
    >>> m_dage_2LB(3,80)
    ([38.0, 10.0, 45.25], [0.024390243902439025, 0.014285714285714285, 0.05128205128205128], [-650, -137, -1274])
    
    >>> m_dage_2LB(3,120)
    ([27.666666666666668, 46.833333333333336, 44.0], [0.05, 0.047244094488188976, 0.0410958904109589], [-311, -377, 200])
    """
    
    liste_ventetider, liste_fly_der_venter, liste_over_lukketid, = [], [], [] #setup
    
    for i in range(0,m): #gentager simuleringen i en_dag funktionen m gange
        ventetider, fly_der_venter, over_lukketid = en_dag_2LB(n)
        liste_ventetider.append(ventetider)
        liste_fly_der_venter.append(fly_der_venter)
        liste_over_lukketid.append(over_lukketid)
    
    liste_mean_ventetider = [np.mean(vt) for vt in liste_ventetider] #tager den gennemsnitlige ventetid for hver dag
    
    return liste_mean_ventetider, liste_fly_der_venter, liste_over_lukketid


def l_år_2LB(l,m,n):
    """
    Simulerer l år i lufthavnen med to landingsbaner.
    Funktionen gentager m_dage funktionen l gange, hvor det gennemsnitlige antal fly stiger for hver iteration.
    Stigningen er på 5% hvert år og udregnes med renteformlen.
    Outputtet er to todimensionelle lister.

    Input
    l -> antallet af år simuleret.
    m -> antallet af dage simuleret.
    n -> skal symbolisere den gennemsnitlige mængde fly.

    Output
    liste_ventetider -> en liste med gennemsnitlig ventetid for alle fly, som skal vente med at lande, hver dag for l år.
    liste_fly_der_venter -> en liste over brøkdelen af fly, som skal vente med at lande, hver dag for l år.
    liste_over_lukketid -> en liste over hvornår det sidste fly er landet i forhold til lukketid hver dag for l år.
    
    Eksempel
    >>> l_år_2LB(3,3,80)
    ([[47.0, nan, 23.333333333333332], [58.5, 40.0, nan], [91.6, 18.0, 24.0], [59.0, 82.5, 53.0]], [[0.023529411764705882, 0.0, 0.04054054054054054], [0.02197802197802198, 0.037037037037037035, 0.0], [0.04950495049504951, 0.04, 0.011494252873563218], [0.010309278350515464, 0.018691588785046728, 0.03614457831325301]], [[-1115, -40, -63], [-327, -4, -37], [-272, -794, -350], [-378, 51, -245]])
    
    >>> l_år_2LB(3,3,120)
    ([[66.0, 24.666666666666668, 56.285714285714285], [18.25, 76.85714285714286, 77.0], [57.75, 58.125, 40.857142857142854], [53.4, 49.09090909090909, 20.6]], [[0.018018018018018018, 0.024390243902439025, 0.051470588235294115], [0.031746031746031744, 0.050724637681159424, 0.04516129032258064], [0.057971014492753624, 0.06201550387596899, 0.04827586206896552], [0.04716981132075472, 0.07006369426751592, 0.037037037037037035]], [[-147, -12, 65], [-496, -99, -5], [-603, -725, -260], [175, -252, 48]])
    """
    liste_ventetider, liste_fly_der_venter, liste_over_lukketid = [], [], [] #setup
    
    for i in range(0,l+1): #gentager simuleringen i m_dage funktionen l gange
         ventetider, fly_der_venter, over_lukketid = m_dage_2LB(m,int(n*(1.05)**i))
         liste_ventetider.append(ventetider)
         liste_fly_der_venter.append(fly_der_venter)
         liste_over_lukketid.append(over_lukketid)
         
    return liste_ventetider, liste_fly_der_venter, liste_over_lukketid



if  __name__ == '__main__':
   import doctest #doctest tester om alle funktionerne giver samme resultat som eksemplerne
   print(doctest.testmod())
