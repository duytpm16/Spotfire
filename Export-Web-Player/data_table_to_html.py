#Converts a data table to an html table and adds export functionality. Works in webplayer and any browser that supports flash 
# to POC, Add a data table and two text areas. Then define the two script parameters:
# visTA : target text area (a blank text area different from where this script will running as it will replace its contents)
# visDT : Data Table
from Spotfire.Dxp.Data import *
from Spotfire.Dxp.Application.Visuals import HtmlTextArea

# Create a temporary column that is a concatenation of the other columns in the table
expression = ["[%s]" % col for col in visDT.Columns]
expression = "Concatenate(" + ",\",\",".join(expression) + ")"
visDT.Columns.AddCalculatedColumn("Combined", expression)

# Build the Export button and HTML table
ta = visTA.As[HtmlTextArea]()
ta.HtmlContent = '<input id="btnExport" type="button" style="color:#26A2ED;" value="Export" class="sf-element sf-element-control sfc-action sfc-action-button"><br>'
if visDT.RowCount > 1000:
    ta.HtmlContent += "<h3 align='center'&gt;Table is too large to display.</h3><p id='exportTable' class='Test' style='white-space: pre-wrap; display: none;'>"
else:
    ta.HtmlContent += "<p id='exportTable' class='Test' style='white-space: pre-wrap;'>;"

cursor = DataValueCursor.CreateFormatted(visDT.Columns["Combined"])
combined = [cursor.CurrentValue for row in visDT.GetRows(cursor)]
combined.append("</p>")

# Write the HTML table to text area
ta.HtmlContent += '\n'.join(combined)