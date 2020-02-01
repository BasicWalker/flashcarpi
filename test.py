def dist_meter_path(distance):
        nearest_dist = 2.5 * round(distance/2.5)
        bar_measure = str(nearest_dist).replace(".0", "")
        bar_measure = bar_measure.replace(".", "_")
        png_path = (bar_measure + 'dist.png')
        return str(png_path)

distance = 42.6

print(dist_meter_path(distance))