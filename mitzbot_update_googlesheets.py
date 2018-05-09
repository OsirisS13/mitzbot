import gspread
from oauth2client.service_account import ServiceAccountCredentials

secretfile = ''

#function takes the following values in the format social channel, column to write it in
def updategooglesheets(storagefile, spreadsheet,worksheet,gdate,gfblikes,fbcolumn,gigfollowers,igcolumn,gtwitterfollwers,twittercolumn):
	# use creds to create a client to interact with the Google Drive API
	# creds set here https://console.developers.google.com/apis/credentials?project=healthy-kayak-161520
	scope = ['https://spreadsheets.google.com/feeds']
	creds = ServiceAccountCredentials.from_json_keyfile_name(secretfile, scope)
	client = gspread.authorize(creds)

	# Find a workbook by name and open the first sheet
	# Make sure you use the right name here.
	sheet = client.open(spreadsheet).worksheet(worksheet)
	
	#inserts a new row in row 3, then adds the values in the list in each column starting from 1.  the formulas are used to caluclate differences.
	#nb, this may cause problems with large sheets over 1000 rows including slowness and possibly even timeouts
	sheet.insert_row([gdate,gfblikes,'=B3-B4',gigfollowers,'=D3-D4',gtwitterfollwers,'=F3-F4'], index = 3)
	return
