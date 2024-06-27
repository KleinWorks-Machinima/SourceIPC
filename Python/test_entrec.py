import numpy
import time
import random
import math



def ParseSourceVectors(test_angle, prev_angles: list):


    # this should technically trigger if either X Y or Z prev_angles are < 0...
    # but theres no case in which Y or Z would have more angles than X
    if len(prev_angles) <= 0:
        return test_angle


    print("Converting angle into Radians...")
    test_angle = math.radians(test_angle)




    print("De-modulating angle...")

    prev_angles.append(test_angle)

    test_angle = numpy.unwrap(prev_angles)[-1]

    
    test_angle = numpy.rad2deg(test_angle)

    return test_angle





angle = 0

angles = []

overallRotation = 0

for i in range(50):
    time.sleep(0.1)

    angle = angle % 360 - 180

    print(f">> Angle is [{angle}].\n")

    rotation = random.randint(-75, 75)
    print(f"++ Rotating angle by [{rotation}].\n")

    angle += rotation


    angle = angle % 360 - 180

    overallRotation += rotation

    print(f"?? Expected unwrapped value: [{overallRotation}]\n")


    print(f"** Unwrapping angles: {angles}...\n")
    
    unwrapped_angles = ParseSourceVectors(angle, angles)
    
    
    print(f"== Unwrapped angles: {unwrapped_angles}...\n")

    angles.append(angle)























print(f"?? Expected unwrapped value: [{overallRotation}]\n")


print(f"** Unwrapping angles: {angles}...\n")

angles = numpy.deg2rad(angles)

angles = numpy.unwrap(angles)

angles = numpy.rad2deg(angles)


print(f"== Unwrapped angles: {angles}...\n")

