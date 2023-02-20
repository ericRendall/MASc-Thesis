#this I will try to numerically solve the 3bp 
#probably reference notes from the rocket science class 

import numpy as np 
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.integrate import solve_ivp   
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import PillowWriter

#now with the 3bp, results will vary depending on the initial conditions
#certain initial coniditions lead to stable orbits, but most are unstable

#these are the stable initial conditions described in the papers
    #m1 = m2 = 1, and m3 can vary slighly 
    #at t = 0, x1 = -x2 = -1 and x3 = 0 meaning m3 is in the middle and m1 and m2 are on either side same distance apart
    #at t = 0, y1 = y2 = y3 = 0 meaning m1,m2,m3 all are in the same plane and 0 in the y axis from a 2d perspective
    #at t = 0, vx1 = vx2 = v1 where v1 is some defined speed, so m1 and m2 are moving in the x plane at the same speed initially 
    #at t = 0, vy1 = vy2 = v2 where v2 is some defined speed, so m1 and m2 are moving in the y plane at the same speed initially 
    #at t = 0, vx3 = -2v1/m3 and vy3 = -2v2/m3, so x speed and y speed of third body have these proportions
    
    #the only parameters that change are v1, v2, and m3
    #this config makes this system have net zero angular momentym and net zero linear momentum
    
# PARARMS TO CHANGE
#stable conditions from paper:
    #m3 = 1
    #v1 =  0.39295
    #v2 = 0.09758
    
#m3 = 100 #maybe can simulate the IC's with a monte carlo in the future
#v1 = 2 #initial x vel of m1, m2
#v2 = 30 #initial y vel of m1, m2
#v3 = 4 #initial z vel of m1, m2

# Everything else follows from paper
#masses
m1 = 5
m2 = 5
m3 = 5
m4 = 5

#body 1 initial positions
x1_0 = 0
y1_0 = 0
z1_0 = 0

#body 2 initial positions
x2_0 = 1
y2_0 = 0
z2_0 = 0

#body 3 initial positions
x3_0 = 0
y3_0 = 1
z3_0 = 0

#body 4 initial positions
x4_0 = -1
y4_0 = 0
z4_0 = 0

#body 1 initial velocities
vx1_0 =  0
vy1_0 =  0
vz1_0 = 0

#body 2 initial velocities
vx2_0 = 0
vy2_0 = 1
vz2_0 = 0

#body 3 initial velocities
vx3_0 = -1
vy3_0 = 0
vz3_0 = 0

#body 4 initial velocities
vx4_0 = 0
vy4_0 = -1
vz4_0 = 40

#now define the ODE system
def dSdt(t, S):
    x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4, vx1, vy1, vz1, vx2, vy2, vz2, vx3, vy3, vz3, vx4, vy4, vz4 = S #solve these as they vary with time
    r12 = np.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2) #pythag in 3D
    r13 = np.sqrt((x3-x1)**2 + (y3-y1)**2 + (z3-z1)**2)
    r14 = np.sqrt((x4-x1)**2 + (y4-y1)**2 + (z4-z1)**2)
    r23 = np.sqrt((x3-x2)**2 + (y3-y2)**2 + (z3-z2)**2)
    r24 = np.sqrt((x4-x2)**2 + (y4-y2)**2 + (z4-z2)**2)
    r34 = np.sqrt((x4-x3)**2 + (y4-y3)**2 + (z4-z3)**2)
    return [ 
            vx1,
            vy1,
            vz1, 
            vx2,
            vy2,
            vz2, #these get integrated to solve for position as time changes
            vx3,
            vy3,
            vz3, 
            vx4,
            vy4,
            vz4,
            m2/r12**3 * (x2-x1) + m3/r13**3 * (x3-x1) + m4/r14**3 * (x4-x1), #mass 1, this is acceleration which came from force and each mass has two terms since it is being pulled by two other bodies
            m2/r12**3 * (y2-y1) + m3/r13**3 * (y3-y1) + m4/r14**3 * (y4-y1),
            m2/r12**3 * (z2-z1) + m3/r13**3 * (z3-z1) + m4/r14**3 * (z4-y1),
            m1/r12**3 * (x1-x2) + m3/r23**3 * (x3-x2) + m4/r24**3 * (x4-x2), #mass 2
            m1/r12**3 * (y1-y2) + m3/r23**3 * (y3-y2) + m4/r24**3 * (y4-y2),
            m1/r12**3 * (z1-z2) + m3/r23**3 * (z3-z2) + m4/r24**3 * (z4-z2),
            m1/r13**3 * (x1-x3) + m2/r23**3 * (x2-x3) + m4/r34**3 * (x4-x3), #mass 3
            m1/r13**3 * (y1-y3) + m2/r23**3 * (y2-y3) + m4/r34**3 * (y4-y3), 
            m1/r13**3 * (z1-y3) + m2/r23**3 * (z2-y3) + m4/r34**3 * (z4-z3), #these get integrated to solve for velocity as time changes
            m1/r14**3 * (x1-x4) + m2/r24**3 * (x2-x4) + m3/r34**3 * (x3-x4), #mass 4 terms
            m1/r14**3 * (y1-y4) + m2/r24**3 * (y2-y4) + m3/r34**3 * (y3-y4),
            m1/r14**3 * (z1-z4) + m2/r24**3 * (z2-z4) + m3/r34**3 * (z3-z4)
           ]


t = np.linspace(0, 20, 1000)

#Here we use the special DOP853 solver as recommended by the paper. We set very small values for rtol and atol to ensure a proper solution
sol = solve_ivp(dSdt, (0,20), y0=[x1_0, y1_0, z1_0, x2_0, y2_0, z2_0, x3_0, y3_0, z3_0, x4_0, y4_0, z4_0,
                       vx1_0, vy1_0, vz1_0, vx2_0, vy2_0, vz2_0, vx3_0, vy3_0, vz3_0, vx4_0, vy4_0, vz4_0],
                method = 'DOP853', t_eval=t, rtol=1e-10, atol=1e-13)

t = sol.t
x1 = sol.y[0]
y1 = sol.y[1]
z1 = sol.y[2]
x2 = sol.y[3]
y2 = sol.y[4]
z2 = sol.y[5]
x3 = sol.y[6]
y3 = sol.y[7]
z3 = sol.y[8]
x4 = sol.y[9]
y4 = sol.y[10]
z4 = sol.y[11]

#print(x1)

#Get the actual times (this assumes 3 suns orbiting at earth-sun distance)
tt = 1/np.sqrt(6.67e-11 * 1.99e30 / (1.5e11)**3 ) # seconds
tt = tt / (60*60 * 24* 365.25) * np.diff(t)[0] # per time step (in years)


#try to create my own animated plot
    #maybe can run an if statement that if any of the positional values of the stars get within a threshold value 
    #of the xlim and ylim of the plot, can expand the plot by a certain amount 
    #alternatively could read the farthest value of each and create the xlim and ylim that way
        #problem with this is that if it goes out super far, won't really be able to see the initial motion when they start close together 
        #because plot will be too zoomed out to see this

from matplotlib.animation import FuncAnimation
from mpl_toolkits import mplot3d

  
def animate(i):
    
    
    plt.cla() #clears axis
    make_it_3D.scatter3D(x1[i], y1[i], z1[i], s = m1*10) #body 1, s denotes markersize
    make_it_3D.scatter3D(x2[i], y2[i], z2[i], s = m2*10) #body 2
    make_it_3D.scatter3D(x3[i], y3[i], z3[i], s = m3*10) #body 3, maybe could scale the size of the body with its mass value, that would be cool 
    make_it_3D.scatter3D(x4[i], y4[i], z4[i], s = m4*10) #body 4
    
    array = np.array([x1[i], x2[i], x3[i], x4[i], y1[i], y2[i], y3[i], y4[i], z1[i], z2[i], z3[i], z4[i]])
    array = np.abs(array)
    max_val = np.max(array)
    
        
    plt.xlim([-max_val - 2, max_val + 2])
    plt.ylim([-max_val - 2, max_val + 2])
    make_it_3D.set_zlim([-max_val - 2, max_val + 2])
    
    make_it_3D.set_xlabel('x direction')
    make_it_3D.set_ylabel('y direction')
    make_it_3D.set_zlabel('z direction')
    
    
fig = plt.figure()
make_it_3D = plt.axes(projection = "3d")
    
ani = FuncAnimation(plt.gcf(), animate, interval = 1) #interval is ms delay so 1000 = 1 second
#ani.save('trajectory.gif', writer='pillow', fps=30)

plt.show()
