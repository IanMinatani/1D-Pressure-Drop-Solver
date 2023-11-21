import numpy as np
import math

# MPDgetPressureDrop is a function that inputs fluid state, pipe dimensions, reynolds number
# and a darcy resistance coefficient and outputs two coefficients. The first coefficient when
# multiplied by length and fluid velocity squared provides major pressure drop losses. The second
# when multiplied by fluid velocity squared provides minor pressure drop losses.
#
# Major: Pipe wall friction losses
# Minor: Fittings, Bends, Contractions, etc.
#
# Can be improved by using colebrook equation instead of swamee-jain approximation
#
# IAN TO DO: Validate answer makes sense. Add code that calculates reynolds number (probably)

#fluidStateVector: [Pressure(psi), density (kg/m3), average fluid velocity (m/s), fluid depth (m), kinetic energy correction factor (dimensionless)]
#tubeVector: [diameterIn, thicknessIn, lengthFt, roughnessFt, typ. R/D]
fluidStateVector1 = np.array([45,1000,0,0,1])
fluidStateVector2 = np.array([15,1000,np.nan,0,1])
tubeVector2 = np.array([1,0.065,5,6.6*10**(-3),6])


def MPDgetPressureDropCoefficient(fluidStateVector, tubeVector, reynoldsNumber, darcyResistanceCoefficient):
    #Swamee-Jain for Darcy Friction Factor
    darcyFrictionFactor = 0.25 / (math.log10(tubeVector[3]/(0.3083*tubeVector[0]) + 5.74/(reynoldsNumber**0.9)))**2
    tubeInnerDiameterIn = tubeVector[0] - 2*tubeVector[1]
    
    # Minor Losses
    pressureDropCoefficientMinor = 0.5 * fluidStateVector[1] * darcyResistanceCoefficient
    
    # Major Losses
    pressureDropCoefficientMajor = (fluidStateVector[1] * darcyFrictionFactor)/((1/6)*tubeInnerDiameterIn)
    
    print("MPDgetPressureDrop Ran Successfully!")
    return([pressureDropCoefficientMajor, pressureDropCoefficientMinor])
    
test = MPDgetPressureDropCoefficient(fluidStateVector1, tubeVector2, 300000, 500)
print(test)