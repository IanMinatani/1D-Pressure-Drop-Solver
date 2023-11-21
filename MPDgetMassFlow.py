import numpy as np
import math
import matplotlib.pyplot as plt
from MPDgetPressureDropCoefficient import MPDgetPressureDropCoefficient

# MPDgetMassFlow is a function that inputs two fluid states (Typically, a tank and an outlet), 
# an associated pressure drop, and nominal pipe and outputs a mass flow rate in Kg/s.
#
# IAN TO DO: 

# fluidStateVector: [Pressure(psi),   density (kg/m3), average fluid velocity (m/s), ...
#                   fluid depth (m), kinetic energy correction factor (dimensionless), dynamic viscosity]
# tubeVector: [diameterIn, thicknessIn, lengthFt, roughnessFt, typ. R/D]

def MPDgetMassFlow(fluidStateVector1, fluidStateVector2, darcyResistanceCoefficient, tubeVector):
    
    tubeAreaMeters = (np.pi * (tubeVector[0] - 2*tubeVector[1])**2)/(4 * 1550) # 1550 sq in / sq m
    tubeDiameterMeter = tubeVector[0] / 39.37
    g = 9.81
    
#    if math.isnan(fluidStateVector2[2]) == True:
#        print("nan")
        
    # Conversion to Metric Fluid Parameters
    pressurePa1 = fluidStateVector1[0] * 6895
    dynamicPressurePa1 = 0.5 * fluidStateVector1[4] * fluidStateVector1[1] * fluidStateVector1[2]**2
    potentialEnergy1 = fluidStateVector1[1] * g * fluidStateVector1[3]
        
    pressurePa2 = fluidStateVector2[0] * 6895
    potentialEnergy2 = fluidStateVector2[1] * g * fluidStateVector2[3]
        
    i = 100
    reynoldsIteration = np.zeros(i)
    reynoldsIteration[0] = 300000
    for x in range(i):
        # Obtain Pressure Drop Coefficients (Pressure Drop / Flow Rate Squared)
        [majorPDropCoefficient, minorPDropCoefficient] = MPDgetPressureDropCoefficient(fluidStateVector2, tubeVector, reynoldsIteration[x], darcyResistanceCoefficient)
        
        # Solve for Fluid Velocity => Incompressible Mass Flow Rate
        fluidStateVector2[2] = math.sqrt( (pressurePa1 + dynamicPressurePa1 + potentialEnergy1 - pressurePa2 - potentialEnergy2) / (0.5 * fluidStateVector2[4] * fluidStateVector2[1] + majorPDropCoefficient * tubeVector[2] + minorPDropCoefficient) )
        reynoldsIteration[x+1] = fluidStateVector2[1] * fluidStateVector2[2] * tubeDiameterMeter / fluidStateVector2[5]
            
        # Iterate Reynolds Until Convergence
        reynoldsBackwardsDifference = abs(reynoldsIteration[x+1] - reynoldsIteration[x])
        if reynoldsBackwardsDifference < 10**(-8):
            print("Reynolds Iterations:", x, "  Number:", reynoldsIteration[x])
            break
    massFlowKgS = fluidStateVector2[1] * tubeAreaMeters * fluidStateVector2[2]
    return massFlowKgS
#    else:
#        print("ERROR: You fed me velocity of state 2, next time use a hand calculator!")
#        massFlowKgS = fluidStateVector2[1] * tubeAreaMeters * fluidStateVector2[2]
    
#    print(massFlowKgS, "Kg/s")
    
fluidStateVector1 = np.array([370,843.42,0,0,1.04,0.00115])
fluidStateVector2 = np.array([15,843.42,np.nan,0,1.04,0.00115])

i=25
massFlowTubeDistanceArray = np.zeros(i)
for x in range(i):
    tubeDistanceArray = np.linspace(1,100,i)
    tubeVector = np.array([0.75,0.065,tubeDistanceArray[x],6.6*10**(-3),6])
    massFlowTubeDistanceArray[x] = MPDgetMassFlow(fluidStateVector1, fluidStateVector2, 0, tubeVector)

fluidStateVector1 = np.array([370,843.42,0,0,1.04,0.00115])
fluidStateVector2 = np.array([15,843.42,np.nan,0,1.04,0.00115])
massFlowResistanceCoefficientArray = np.zeros(i)
for x in range(i):
    darcyResistanceCoefficientArray = np.linspace(0,500,i)
    tubeVector = np.array([0.75,0.065,5,6.6*10**(-3),6])
    massFlowResistanceCoefficientArray[x] = MPDgetMassFlow(fluidStateVector1, fluidStateVector2, darcyResistanceCoefficientArray[x], tubeVector)

plt.figure(1)
plt.plot(tubeDistanceArray, massFlowTubeDistanceArray)
plt.title("Effect of Tube Distance on Mass Flow")
plt.xlabel("Tube Distance, feet")
plt.ylabel("Mass Flow, Kg/s")
plt.show()

plt.figure(2)
plt.plot(darcyResistanceCoefficientArray, massFlowResistanceCoefficientArray)
plt.title("Effect of Resistance Coefficient on Mass Flow")
plt.xlabel("Resistance Coefficient")
plt.ylabel("Mass Flow, Kg/s")
plt.show()