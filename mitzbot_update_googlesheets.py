import gspread
from oauth2client.service_account import ServiceAccountCredentials

#function takes the following values in the format social channel, column to write it in
def updategooglesheets(spreadsheet,worksheet,gdate,gfblikes,fbcolumn,gigfollowers,igcolumn,gtwitterfollwers,twittercolumn):
	# use creds to create a client to interact with the Google Drive API
	# creds set here https://console.developers.google.com/apis/credentials?project=healthy-kayak-161520
	scope = ['https://spreadsheets.google.com/feeds']
	creds = ServiceAccountCredentials.from_json_keyfile_name('/home/PythonScripts/client_secret.json', scope)
	client = gspread.authorize(creds)

	# Find a workbook by name and open the first sheet
	# Make sure you use the right name here.
	sheet = client.open(spreadsheet).worksheet(worksheet)
	
#little jig to find the next empty row, seems gspread doesnt have a native function for it
	#get the total number of rows in the sheet
	total_rows = len(sheet.col_values(1))
	#need to read the last written row from the storage file, 
	#if we dont do this we need to iterate over all the rows which takes a long time when there are heaps of data
	try:
		#open file
		current_row_from_file = open("lastwrittenrow.txt","r")
		#read file and convert result to integer
		current_row = int(current_row_from_file.read())
		#close file
		current_row_from_file.close()		
	except:
		#start at this row and go through them all
		current_row = 1
	#iterate through all the rows, 
	while 1: 
		
		#check if the value is blank, if so then this is our empty row, store and write to file
		if sheet.cell(current_row,1).value == "":
			next_empty_row = current_row
			#open file to store
			current_row_from_file = open("lastwrittenrow.txt","w")
			#write the new row number as string
			current_row_from_file.write(str(current_row))
			#close file
			current_row_from_file.close()
			#exit loop
			break
		#if not move on to the next row
		else:
			current_row = current_row + 1
		
	print "Adding values to row %i" %next_empty_row
	#write to sheet using the next empty row and the column values passed from function start (except for date which is always column 1
	sheet.update_cell(next_empty_row,1, gdate)
	sheet.update_cell(next_empty_row,fbcolumn, gfblikes)
	sheet.update_cell(next_empty_row,igcolumn, gigfollowers)
	sheet.update_cell(next_empty_row,twittercolumn, gtwitterfollwers)
	return
