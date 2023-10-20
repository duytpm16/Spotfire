from Spotfire.Dxp.Application.Visuals import TablePlot, CategoryKey
import System

# Define colors
colors = {
	"red": System.Drawing.Color.FromArgb(255, 78, 51),
	"blue": System.Drawing.Color.FromArgb(158, 182, 255),
	"white": System.Drawing.Color.FromArgb(255, 255, 255)
}

# Get Data Table column names
dt_colnames = [col.Name for col in dt.Columns]

# Manually add columns C12 - C35, C36+ since they don't contain 'air_free' in column name
C_columns = ["C%d (mol_frac)" % (i) for i in range(12, 36)] + ["C31 (Avg_mol_frac)", "C36+ (mol_frac)"]

visDT = visDT.As[TablePlot]()
for col in visDT.Columns:
	colName = col.DataColumnName
	colNameSplit = colName.split('(')
	
	# Format names
	if len(colNameSplit) > 1 and ('mol_frac_air_free' in colNameSplit[1] or colName in C_columns):
		comp = colNameSplit[0].strip(' ')
		comp = comp if comp != 'Carbon Dioxide' else 'CarbonDioxide'

		avgName = comp + ".AvgMolFracAirFree"
		stdName = comp + ".StdDevMolFracAirFree"

		if avgName in dt_colnames and stdName in dt_colnames:

			# Define Expressions
			expression_1 = "[{val}]>[{avg}]+(2*[{std}]) And [{val}]<[{avg}]-(2*[{std}])".format(val=colName, avg=avgName, std=stdName)
			expression_2 = "[{val}]>=[{avg}]+(1*[{std}]) And [{val}]<[{avg}]+(2*[{std}])".format(val=colName, avg=avgName, std=stdName)
			expression_3 = "[{val}]<[{avg}]-(1*[{std}]) And [{val}]>[{avg}]-(2*[{std}])".format(val=colName, avg=avgName, std=stdName)
			expression_4 = "[{val}]<[{avg}]+(1*[{std}]) or [{val}]>[{avg}]-(1*[{std}])".format(val=colName, avg=avgName, std=stdName)

			# Add Color Scheme Grouping
			coloring = visDT.Colorings.AddNew(colName)
			
			coloring.SetColorOnText = True
			coloring.DefaultColor = colors["white"]
			coloring.EmptyColor = colors["white"]
			coloring.AddExpressionRule(expression_1, colors["red"])
			coloring.AddExpressionRule(expression_2, colors["blue"])
			coloring.AddExpressionRule(expression_3, colors["blue"])
			coloring.AddExpressionRule(expression_4, colors["white"])

			# Add column to Color Scheme Grouping
			categoryKey = CategoryKey(colName)
			visDT.Colorings.AddMapping(categoryKey, coloring)

			# Set the coloring rule display names
			coloring.Item[0].ManualDisplayName = comp + " 2 StdDev +/- from Mean"
			coloring.Item[1].ManualDisplayName = comp + " upper limit>1 and <2 StdDev"
			coloring.Item[2].ManualDisplayName = comp + " lower limit>1 and <2 StdDev"
			coloring.Item[3].ManualDisplayName = comp + " 1 StdDev +/- from Mean"