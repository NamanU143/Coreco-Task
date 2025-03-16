﻿# Coreco-Task

Here’s some dummy data for better understanding:

1. User Table (users)
id	name	email	role	password
1	Admin	admin@example.com	Admin	admin123
2	Alice	alice@example.com	User	alicepass
3	Bob	bob@example.com	User	bobpass
2. Asset Types Table (asset_types)
asset_type_id	type_name	is_active
1	Laptop	True
2	Mobile Phone	True
3	Printer	False
3. Asset Table (assets)
asset_id	asset_type_id	asset_name	location	brand	purchase_year	is_active_asset	current_owner	purchase_date
1	1	MacBook Pro	Office A	Apple	2022	True	2	2023-02-15 10:00:00
2	2	iPhone 13	Office B	Apple	2021	True	3	2022-06-20 09:30:00
3	3	HP LaserJet	Office C	HP	2019	False	1	2020-11-10 14:45:00
4. Transactions Table (transactions)
transaction_id	asset_id	from_user_id	to_user_id	transaction_date
1	1	1	2	2023-03-01 12:00:00
2	2	1	3	2023-07-05 15:30:00
