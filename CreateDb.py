import sqlite3

# Water Supply Scada System Data Base

class Database:
	def __init__(self):
		conn=sqlite3.connect("WSSSDB.db")
		cur = conn.cursor()

		#Table structure for table of equipments
		cur.execute('''

		CREATE TABLE IF NOT EXISTS "equipments" 
		("equip_id"	INTEGER NOT NULL UNIQUE,
		"equip_type" TEXT NOT NULL,
		"equip_name" TEXT NOT NULL,
		PRIMARY KEY("equip_id"));

		''')

		############################################
		#Dumping data for table `equipments`
		cur.execute('''

		INSERT INTO `equipments` ( `equip_type`, `equip_name`) VALUES
		( 'BH_Pump', '1#'),
		( 'BH_Pump', '2#'),
		( 'BH_Pump', '3#'),
		( 'BH_Pump', '4#'),
		( 'BH_Pump', '5#'),
		( 'BH_Pump', '6#'),
		( 'BH_Pump', '7#'),
		( 'BH_Pump', '8#'),
		( 'cl_tank', '9#'),
		( 'booster_pump', '11#'),
		( 'booster_pump', '12#'),
		( 'booster_pump', '13#'),
		( 'booster_pump', '14#'),
		( 'booster_pump', '15#'),
		( 'booster_pump', '16#'),
		( 'Reservoir', 'CT5'),
		( 'Reservoir', 'Koye'),
		( 'Reservoir', 'AASTU')
		''')

		#######################################

		#Table structure for table Bore hole pumps
		cur.execute('''

		CREATE TABLE IF NOT EXISTS "SPumps" (
		"id"	INTEGER NOT NULL UNIQUE,
		"voltage_A_B"	INTEGER NOT NULL DEFAULT 0,
		"voltage_B_C"	INTEGER NOT NULL DEFAULT 0,
		"voltage_C_A"	INTEGER NOT NULL DEFAULT 0,
		"current"	float NOT NULL DEFAULT 0,
		"conductivity"	float NOT NULL,
		"level"	float NOT NULL,
		"pressure"	float NOT NULL,
		"flow"	INTEGER NOT NULL DEFAULT 0,
		"equip_id"	INTEGER NOT NULL,
		"log_time"	TEXT NOT NULL ,
		FOREIGN KEY("equip_id") REFERENCES "equipments"("equip_id"),
		PRIMARY KEY("id" AUTOINCREMENT)
		)
		''')

		#############################################

		#Table structure for table of chlorine tanks
		cur.execute('''
		CREATE TABLE IF NOT EXISTS "cl_tanks" (
		"id"	INTEGER NOT NULL,
		"cl_level"	REAL,
		"log_time"	TEXT,
		PRIMARY KEY("id" AUTOINCREMENT)
		);
		''')

		###########################################

		#Table structure for table of reservior status
		cur.execute('''
		CREATE TABLE IF NOT EXISTS "reservoir_status" (
		"id"	INTEGER NOT NULL UNIQUE,
		"r_level"	INTEGER NOT NULL,
		"flow_in"	INTEGER NOT NULL,
		"flow_out"	INTEGER NOT NULL,
		"equip_id"	INTEGER NOT NULL,
		"log_time"	TEXT NOT NULL UNIQUE,
		PRIMARY KEY("id" AUTOINCREMENT)
		)
		''')


		#####################################################
		#Table structure for table booster pumps amps and total outputs
		cur.execute('''
		CREATE TABLE IF NOT EXISTS "HBPumps" (
		"id"	INTEGER NOT NULL UNIQUE,
		"voltage_A_B"	INTEGER NOT NULL DEFAULT 0,
		"voltage_B_C"	INTEGER NOT NULL DEFAULT 0,
		"voltage_C_A"	INTEGER NOT NULL DEFAULT 0,
		"current"	float NOT NULL DEFAULT 0,
		"flow"	INTEGER NOT NULL DEFAULT 0,
		"pressure"	float NOT NULL,
		"equip_id"	INTEGER NOT NULL,
		"log_time"	TEXT NOT NULL ,
		FOREIGN KEY("equip_id") REFERENCES "equipments"("equip_id"),
		PRIMARY KEY("id" AUTOINCREMENT)
		)''')

		# ##################################################
		# #Table structure for table booster pumps outputs detail
		# cur.execute('''
		# CREATE TABLE IF NOT EXISTS "bp_outs" (
		# 	"id"	INTEGER NOT NULL UNIQUE,
		# 	"residual_chlorine"	REAL,
		# 	"turbidity"	REAL,
		# 	"PH"	REAL,
		# 	"waterTemperature"	REAL,
		# 	"log_time"	TEXT NOT NULL UNIQUE,
		# 	PRIMARY KEY("id" AUTOINCREMENT)
		# )''')

		# commit and i am out
		conn.commit()
		conn.close()
