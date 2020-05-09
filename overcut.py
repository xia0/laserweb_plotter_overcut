import re
import sys
import math

output = "; GCODE passed through overcut script\n; xia0\n"
path = -1
on_path = False
triggered_g1 = False
overcut_target_distance = float(sys.argv[2])

overcut_output = ""

with open(sys.argv[1], 'r') as f:
    for line in f.readlines():
        #print(line)

        # Look for beginning of path
        m_path = re.search("; Pass \d* Path (\d*)", line)
        # locate start co-ordinates of path
        start_path = re.search("G0\sX([-\d\.]*) Y([-\d\.]*)", line)
        mid_path = re.search("G1\sX([-\d\.]*) Y([-\d\.]*)", line)

        if m_path:
            path = int(m_path.group(1))

        elif start_path:
            overcut_distance = 0
            overcut_output = ""
            on_path = True
            triggered_g1 = False
            interpolation_done = False
            last_x = float(start_path.group(1))
            last_y = float(start_path.group(2))

        elif mid_path and path >= 0:

            triggered_g1 = True

            x = float(mid_path.group(1))
            y = float(mid_path.group(2))

            delta_x = x - last_x    # calculate the distance between this point and last
            delta_y = y - last_y

            overcut_distance_delta = math.sqrt(pow(delta_x, 2) + pow(delta_y, 2))

            # add this point to overcut since we have not met our target
            if (overcut_distance < overcut_target_distance and interpolation_done == False):

                # will adding this point exceed our target?
                if (overcut_distance + overcut_distance_delta > overcut_target_distance):
                    # if so, we need to calculate an interpolated point
                    overshot_distance = overcut_distance + overcut_distance_delta - overcut_target_distance # how much are we over target?
                    overshot_ratio = (overcut_distance_delta-overshot_distance) / overcut_distance_delta

                    # calculate co-ordinates of new point
                    new_x = last_x + delta_x * overshot_ratio
                    new_y = last_y + delta_y * overshot_ratio

                    # sanity check - calculate this new distance
                    interpolated_distance = math.sqrt(pow(last_x - new_x, 2) + pow(last_y - new_y, 2))

                    # add our interpolated point into the output stream
                    overcut_output += "G1 X" + str(round(new_x, 2)) + " Y" + str(round(new_y, 2)) + " ; interpolated distance " + str(interpolated_distance) + "\n"
                    overcut_distance += interpolated_distance # add up the new interpolated distance to double check

                    # we're done with this shit
                    interpolation_done = True

                else: #otherwise, add this co-ordinate as normal
                    overcut_distance += overcut_distance_delta
                    overcut_output += line

            last_x = x  # update last_x and y values for next iteration
            last_y = y

        elif (on_path == True and triggered_g1 == True): # the path has ended

            on_path = False
            overcut_output = "; overcut start\n" + overcut_output + "; overcut end - distance " + str(overcut_distance) + "\n"
            output += overcut_output

        output += line

print(output)

f = open(sys.argv[3], "w")
f.write(output)
f.close()
