#Converts a tablePlot to an html table and adds export functionality. Works in webplayer and any browser that supports flash 
# to POC, Add a data table and two text areas. Then define the two script parameters:
# visTA : target text area (a blank text area different from where this script will running as it will replace its contents)
# visDT : Data Table visualization
from Spotfire.Dxp.Data import *
from Spotfire.Dxp.Application.Visuals import HtmlTextArea

# Create a temporary column that is a concatenation of the other columns in the table
expression = ["[%s]" % col for col in visDT.Columns]
expression = "Concatenate(" + ",\",\",".join(expression) + ")"
visDT.Columns.AddCalculatedColumn("Combined", expression)

# Build the Export button and HTML table
split_text = '<p style="display: none;">split_here</p>'
ta = visTA.As[HtmlTextArea]()
ta.HtmlContent = ta.HtmlContent.split(split_text)[0]
ta.HtmlContent += '%s<p id="exportTable" style="white-space: pre-wrap; display: none;">' % (split_text)

cursor = DataValueCursor.CreateFormatted(visDT.Columns["Combined"])
combined = [cursor.CurrentValue for row in visDT.GetRows(cursor)]
combined.append("</p>")

# Write the HTML table to text area
ta.HtmlContent += '\n'.join(combined)

# Remove the temporary column
visDT.Columns.Remove("Combined")