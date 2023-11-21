import numpy as np
import math

# MPDgetMassFlow is a function that inputs two fluid states (Typically, a tank and an outlet), an associated pressure drop, and nominal pipe and outputs a
# mass flow rate in Kg/s.
#
# IAN TO DO: mass flow will depend on pressure drop coefficients, so the equation should be re-worked


#fluidStateVector: [Pressure(psi), density (kg/m3), average fluid velocity (m/s), fluid depth (m), kinetic energy correction factor (dimensionless)]
fluidStateVector1 = np.array([45,1000,0,0,1])
fluidStateVector2 = np.array([15,1000,np.nan,0,1])

def MPDgetMassFlow(fluidStateVector1, fluidStateVector2, darcyFrictionFactor, tubeOuterDiameterIn2, tubeThicknessIn2):
    #fluidStateVector: [Pressure(psi), density (kg/m3), average fluid velocity (m/s), fluid depth (m), kinetic energy correction factor (dimensionless)]
    
    tubeAreaMeters = (np.pi * (tubeOuterDiameterIn2 - 2*tubeThicknessIn2)**2)/(4 * 1550) # 1550 sq in / sq m
    g = 9.81
    
    if math.isnan(fluidStateVector2[2]) == True:
        print("nan")
        
        pressurePa1 = fluidStateVector1[0] * 6895
        dynamicPressurePa1 = 0.5 * fluidStateVector1[4] * fluidStateVector1[1] * fluidStateVector1[2]**2
        potentialEnergy1 = fluidStateVector1[1] * g * fluidStateVector1[3]
        
        pressurePa2 = fluidStateVector2[0] * 6895
        potentialEnergy2 = fluidStateVector2[1] * g * fluidStateVector2[3]
        
        fluidStateVector2[2] = math.sqrt((pressurePa1 + dynamicPressurePa1 * potentialEnergy1 - pressurePa2 - potentialEnergy2 - pressureDrop) / (0.5 * fluidStateVector2[4] * fluidStateVector2[1]))
        massFlowKgS = fluidStateVector2[1] * tubeAreaMeters * fluidStateVector2[2]
    else:
        print("ERROR: You fed me velocity of state 2, next time use a hand calculator!")
        massFlowKgS = fluidStateVector2[1] * tubeAreaMeters * fluidStateVector2[2]
    
    
    
    print("MPDgetMassFlow Ran Successfully!")
    print(massFlowKgS, "Kg/s")
     
MPDgetMassFlow(fluidStateVector1, fluidStateVector2,0,1,0.065)