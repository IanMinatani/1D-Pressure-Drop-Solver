# Functions & Imports
import math
#

# Welcome
# This script is based on the Crane 410 Fluids Manual
# Crane 410 (if properly implemented) is deemed to be the collection of equations most accurately modeling fluid due to
# experimental data. However, as of 2/8/23 SARP has not yet verified the accuracy for our purposes.
#

# N2O mdot: 6.8159271410284115
# Density: 1177.0578251674194
# 6.44*10^-5

# Fuel mdot: 1.9338963655337988
# Density: 843.4232622292875
#.00115 pa s
# DEFINITION OF VARIABLES ##
# 1177.06, 6.8159, 1.5

# FLUID PROPERTIES (F <=> Fluid)
fDensity = 1000      # kg/m^3
fMassFlow = 1.0     # kg/s
fViscosity = 1  # centipoise

# PLUMBING LINE PROPERTIES
tubeOD = 1          # Outer Diameter, inches
tubeThick = 0.00       # Wall Thickness, inches
tubeLength = 10          # Plumbing Length, feet
tubeRough = 0.00005     # Absolute Roughness, in feet. (Not Significant) 0.00005
tubeBendRadius = 3      # Bend Radius, inches

# PLUMBING COMPONENT QUANTITIES
numEnter = 1     # Open Vessel entering enclosed tubing. Should be 1
numExit = 0      # Enclosed tubing exiting to open vessel/environment. Should be 1
numElbow90 = 0
numElbow45 = 0
numBend = 0
numBallValve = 0
numGateValve = 0
numGlobeValve = 0 # For Beta=1
numAngleValve = 0 # For Beta=1

numPoppetCheck = 0
numSwingCheck = 0           # For Constant Diameter Flow
numSwingCheckFat = 0        # For Large Bellied Flow
numLiftCheck = 0            # For Vertical Lift & Beta=1
numLiftCheckAngled = 0      # For Forward Sweep & Beta=1
numStopCheckStraight = 0    # For constant-direction flow
numStopCheck90 = 0          # For 90-degree turn

# CALCULATIONS
g = 32.174

tubeID = tubeOD - 2 * tubeThick
tubeArea = (math.pi/4) * (tubeOD - 2 * tubeThick)**2 # ID Area of Tube, inches
tubeAreaFeet = tubeArea/144 # ID Area of Tube, feet

fDensityImp = fDensity/16.018           # lb/ft^3
fMassFlowImp = fMassFlow * 2.20462      # kg/s to lb/s

fFlowVelocity = fMassFlowImp / (fDensityImp * tubeAreaFeet) # ft/s

# ID in inch, flow in ft/s, density in lb/ft^3, viscosity in centipoise: This is the Crane 410 Way
fReynold = 124*tubeID*fFlowVelocity*fDensityImp/fViscosity

fricFactor = 0.25/(math.log(tubeRough/(3.7*tubeID/12) + 5.74/(fReynold**0.9)))**2   # friction factor, laminar
fricFactorTurb = 0.25/(math.log(tubeRough/(3.7*tubeID/12)))**2                      # friction factor, turbulent

kEnter = 0.78
kExit = 1.0
kElbow90 = 30*fricFactorTurb
kElbow45 = 16*fricFactorTurb
kBend = 12*fricFactorTurb       #Change to tabular method using if/else
kBallValve = 3*fricFactorTurb
kGateValve = 8*fricFactorTurb
kPoppetCheck = 420*fricFactorTurb

K = numEnter*kEnter +\
    numExit*kExit +\
    numElbow90*kElbow90 +\
    numElbow45*kElbow45 +\
    numBend*kBend +\
    numBallValve*kBallValve +\
    numGateValve*kGateValve +\
    numPoppetCheck*kPoppetCheck

# PRESSURE DROP
pDropFriction = 0.001295*fricFactor*tubeLength*fDensityImp*(fFlowVelocity**2)/tubeID
pDropFittings = (fDensityImp/144)*K*(fFlowVelocity**2)/(2*g)

pDrop = pDropFriction + pDropFittings

print("Fluid Pressure Drop: " + str(pDrop))





