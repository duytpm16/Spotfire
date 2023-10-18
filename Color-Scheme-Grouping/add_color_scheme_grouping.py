# Parameters:
#	visDT: The Table Plot Visualization
#	dt: The Data Table used in the Table Plot

from Spotfire.Dxp.Application.Visuals import TablePlot, CategoryKey
import System

# Define colors
color_1 = System.Drawing.Color.FromArgb(255, 78, 51)   # Redish
color_2 = System.Drawing.Color.FromArgb(158, 182, 255) # Blueish
color_3 = System.Drawing.Color.FromArgb(255, 255, 255) # White

# Get Data Table column names
dt_colnames = [col.Name for col in dt.Columns]

# Manually add columns C12 - C35, C36+ since they don't contain 'air_free' in column name
C_columns = ["C%d (mol_frac)" % (i) for i in range(12, 36)] + ["C31 (Avg_mol_frac)", "C36+ (mol_frac)"]

visDT = visDT.As[TablePlot]()
for col in visDT.Columns:
	colName = col.DataColumnName
	colName_split = colName.split('(')
	
	# Format names
	if len(colName_split) > 1:
		comp = colName_split[0].strip(' ')
		comp = comp if comp != 'Carbon Dioxide' else 'CarbonDioxide'

		if 'mol_frac_air_free' in colName_split[1] or colName in C_columns:
			suffix = "MolFracAirFree"
			avgName = comp + ".Avg" + suffix
			stdName = comp + ".StdDev" + suffix

			# Add Color Scheme Grouping
			if avgName in dt_colnames and stdName in dt_colnames:

				# Define Expressions
				expression_1 = "[{val}]>[{avg}]+(2*[{std}]) And [{val}]<[{avg}]-(2*[{std}])".format(val=colName, avg=avgName, std=stdName)
				expression_2 = "[{val}]>=[{avg}]+(1*[{std}]) And [{val}]<[{avg}]+(2*[{std}])".format(val=colName, avg=avgName, std=stdName)
				expression_3 = "[{val}]<[{avg}]-(1*[{std}]) And [{val}]>[{avg}]-(2*[{std}])".format(val=colName, avg=avgName, std=stdName)
				expression_4 = "[{val}]<[{avg}]+(1*[{std}]) or [{val}]>[{avg}]-(1*[{std}])".format(val=colName, avg=avgName, std=stdName)

				# Add coloring rules and colors
				coloring = visDT.Colorings.AddNew(colName)
				categoryKey = CategoryKey(colName)
				visDT.Colorings.AddMapping(categoryKey, coloring)

				coloring.DefaultColor = color_3
				coloring.EmptyColor = color_3
				coloring.AddExpressionRule(expression_1, color_1)
				coloring.AddExpressionRule(expression_2, color_2)
				coloring.AddExpressionRule(expression_3, color_2)
				coloring.AddExpressionRule(expression_4, color_3)
				coloring.SetColorOnText = True

				# Set the coloring rule display names
				coloring.Item[0].ManualDisplayName = comp + " 2 StdDev +/- from Mean"
				coloring.Item[1].ManualDisplayName = comp + " upper limit>1 and <2 StdDev"
				coloring.Item[2].ManualDisplayName = comp + " lower limit>1 and <2 StdDev"
				coloring.Item[3].ManualDisplayName = comp + " 1 StdDev +/- from Mean"