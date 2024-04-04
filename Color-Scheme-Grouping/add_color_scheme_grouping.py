from Spotfire.Dxp.Application.Visuals import TablePlot, CategoryKey
import System

# Define colors
color_1 = System.Drawing.Color.FromArgb(255, 78, 51)   # Redish
color_2 = System.Drawing.Color.FromArgb(158, 182, 255) # Blueish
color_3 = System.Drawing.Color.FromArgb(255, 255, 255) # White


visDT = visDT.As[TablePlot]()
visDT.Colorings.Clear()

for col in visDT.Columns:
	colName = col.DataColumnName
	if not colName.startswith(('Date Sampled', 'Unique Sample ID', 'Avg_', 'StdDev_')):
		component = colName

		avgColumn = "Avg_" + component
		stdColumn = "StdDev_" + component

		# Add Color Scheme Grouping
		# Define Expressions
		expression_1 = "[{val}]> Max([{avg}])+(2*Max([{std}])) or  [{val}]<Max([{avg}])-(2*Max([{std}]))".format(val=colName, avg=avgColumn, std=stdColumn)
		expression_2 = "[{val}]>=Max([{avg}])+(1*Max([{std}])) And [{val}]<Max([{avg}])+(2*Max([{std}]))".format(val=colName, avg=avgColumn, std=stdColumn)
		expression_3 = "[{val}]< Max([{avg}])-(1*Max([{std}])) And [{val}]>Max([{avg}])-(2*Max([{std}]))".format(val=colName, avg=avgColumn, std=stdColumn)
		expression_4 = "[{val}]< Max([{avg}])+(1*Max([{std}])) or  [{val}]>Max([{avg}])-(1*Max([{std}]))".format(val=colName, avg=avgColumn, std=stdColumn)

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
		coloring.Item[0].ManualDisplayName = component + " 2 StdDev +/- from Mean"
		coloring.Item[1].ManualDisplayName = component + " upper limit>1 and <2 StdDev"
		coloring.Item[2].ManualDisplayName = component + " lower limit>1 and <2 StdDev"
		coloring.Item[3].ManualDisplayName = component + " 1 StdDev +/- from Mean"
