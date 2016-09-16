"""
This is untested code. This should be close to being right though.
Need to use nested cursor. Take a point and then compare that points
distances to all the other features in the other table. This is done
using distanceTo method. The distanceTo method is in the polygon and line
geometry class. The distanceTo method will work on point, line and polygon.
The distanceTo method is found within the geometry class. 

Codes does not test if the projections are the same. It is assumed 
the two files are already in the same projections. This code could be added later. 
See:
http://gis.stackexchange.com/questions/182851/arcpy-geometry-object-distanceto-method-in-a-for-loop
distanceTo
http://pro.arcgis.com/en/pro-app/arcpy/classes/polygon.htm
http://pro.arcgis.com/en/pro-app/tool-reference/analysis/near.htm
"""

# Import arcpy.
import arcpy
# Define the input files.
point_feature = r"C:\Users\name\Documents\ArcGIS\Default.gdb\Gas_points"
line_feature = r"C:\Users\name\Documents\ArcGIS\Default.gdb\Gas_lines"

# Need to add two fields to store the near distance and the near feature id. 
# Need to add field to store the near distance. 
arcpy.AddField_management(point_feature, "Near_dist", "DOUBLE")
# Need to add field to store the near id.
arcpy.AddField_management(point_feature, "Near_id", "LONG")

# Create an updatecursor on the point file. This will allow one to 
# update the feature with the nearest distance and the id of that feature.
point_fields = ['SHAPE@', "Near_dist", "Near_id"]
with arcpy.da.UpdateCursor(point_feature, point_fields) as pointcursor:       
    # Iterate over each point
    for point_row in pointcursor:
        # For each point create an empty list. The list will store the near 
        # distance and the id.
        distance_val = []
        # Get the point geometry. This will be used in the 
        # next cursor to calculate the distance.
        geometry = point_row[0]
        print geometry.type
        # Create a search cursor for the other feature. This could be a point,
        # line or polygon feature. 
        with  arcpy.da.SearchCursor(line_feature, ['SHAPE@', "OID@"]) as linecursor:
            # Iterate over every feature in the second table. 
            for line_row in linecursor:
                # Get the geometry object. 
                newgeometry = line_row[0]
                # Use the distanceTo method to determine the distance to object. 
                dist = newgeometry.distanceTo(geometry)
                # Search radius boolean test would go here. 
                # Create a nested list to store distance and id. 
                distance_val.append([dist, line_row[1]])
        # After iterating over every feature in the second table need to 
        # sort the list. Set the key to be the first element in the list.
        # This will then sort on the near distance. 
        sort_distance_val = sort(distance_val, key=lambda items: items[0]))
        # Get the minimum near distance from the list.
        # This is done using python slicing. 
        row[1] = sort_distance_val[0][0]
        # Get the near feature id from the list.
        # This is done using python slicing. 
        row[2] = sort_distance_val[0][1]
        # Print the minimum near distance and the near id. 
        print(row[1], row[2])
        # Update the point feature class so that the near distance and near id are 
        # stored. 
        pointcursor.updateRow(row)