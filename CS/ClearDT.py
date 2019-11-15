import MySQLdb
from python_mysql_dbconfig import read_db_config




def clear_TFT():
	db_config = read_db_config()
	print(db_config)
	db = MySQLdb.connect(**db_config)

	cursor = db.cursor()
	cursor2 = db.cursor()
	projects=cursor.execute("SELECT id, name FROM Scrum_scrumproject WHERE to_clear_TFT =1 ")
	numrows = cursor.rowcount
	counter = 1
	total_goals_cleared = 0
	for x in range(0,numrows):
		
		row = cursor.fetchone()
		thisRow = row[0]
		print("=========================================  " + str(counter) + "  ====================================================")
		print(row)	
		print("Project ID: " + str(thisRow))
		print(row[1])

		sql ="""UPDATE Scrum_scrumgoal SET status=0, days_failed = days_failed + 1 WHERE status=1 AND moveable = 1 AND visible = 1 AND project_id= %s"""
		counter += 1
		
		

		try:
			cursor2.execute(sql, (thisRow, ))
			print("Goals Affected: " + str(cursor2.rowcount))
			print("")
			total_goals_cleared += cursor2.rowcount
			db.commit()
			
		except Exception as e:
			db.rollback()
			print("Failed to execute") 
			raise e

	print("Total number of project affected is: " + str(numrows))
	print("Total number of Goals affected is: " + str(total_goals_cleared))
	print("Successful!!!")
	db.close()
	return

clear_TFT()
