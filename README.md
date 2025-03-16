# Coreco-Task
# Asset Management Database Schema

## Overview
This database schema is designed for an **Asset Management Tool**. It consists of four tables:
1. `users` - Stores user details.
2. `asset_types` - Defines different categories of assets.
3. `assets` - Stores individual asset records.
4. `transactions` - Tracks asset transfers between users.

## Tables & Schema

### 1. Users Table (`users`)
Stores information about system users (Admins and general Users).

| Column  | Type        | Constraints               |
|---------|------------|---------------------------|
| id      | Integer    | Primary Key, Auto-increment |
| name    | String(255) | Not Null                  |
| email   | String(255) | Unique, Not Null          |
| role    | Enum('Admin', 'User') | Not Null, Default: 'User' |
| password | String(255) | Not Null                  |

#### **Sample Data**
| id | name   | email              | role  | password   |
|----|--------|--------------------|-------|------------|
| 1  | Admin  | admin@example.com  | Admin | admin123   |
| 2  | Alice  | alice@example.com  | User  | alicepass  |
| 3  | Bob    | bob@example.com    | User  | bobpass    |

---

### 2. Asset Types Table (`asset_types`)
Defines different categories of assets.

| Column       | Type         | Constraints                 |
|-------------|------------|---------------------------|
| asset_type_id | Integer  | Primary Key, Auto-increment |
| type_name   | String(100) | Unique, Not Null            |
| is_active   | Boolean     | Default: True              |

#### **Sample Data**
| asset_type_id | type_name      | is_active |
|--------------|--------------|-----------|
| 1            | Laptop       | True      |
| 2            | Mobile Phone | True      |
| 3            | Printer      | False     |

---

### 3. Assets Table (`assets`)
Stores information about individual assets.

| Column          | Type        | Constraints                     |
|----------------|------------|---------------------------------|
| asset_id       | Integer    | Primary Key, Auto-increment    |
| asset_type_id  | Integer    | Foreign Key -> asset_types.asset_type_id |
| asset_name     | String(255) | Not Null                        |
| location      | String(255) | Not Null                        |
| brand         | String(255) | Not Null                        |
| purchase_year | Integer     | Not Null                        |
| is_active_asset | Boolean    | Default: True                  |
| current_owner | Integer     | Foreign Key -> users.id (Default: Admin) |
| purchase_date | DateTime    | Not Null                        |

#### **Sample Data**
| asset_id | asset_type_id | asset_name       | location   | brand  | purchase_year | is_active_asset | current_owner | purchase_date        |
|----------|--------------|-----------------|------------|--------|---------------|----------------|---------------|----------------------|
| 1        | 1            | MacBook Pro     | Office A   | Apple  | 2022          | True           | 2             | 2023-02-15 10:00:00  |
| 2        | 2            | iPhone 13       | Office B   | Apple  | 2021          | True           | 3             | 2022-06-20 09:30:00  |
| 3        | 3            | HP LaserJet     | Office C   | HP     | 2019          | False          | 1             | 2020-11-10 14:45:00  |

---

### 4. Transactions Table (`transactions`)
Tracks asset transfers between users.

| Column            | Type      | Constraints                     |
|------------------|----------|---------------------------------|
| transaction_id   | Integer  | Primary Key, Auto-increment    |
| asset_id        | Integer  | Foreign Key -> assets.asset_id |
| from_user_id    | Integer  | Foreign Key -> users.id        |
| to_user_id      | Integer  | Foreign Key -> users.id        |
| transaction_date | DateTime | Default: CURRENT_TIMESTAMP     |

#### **Sample Data**
| transaction_id | asset_id | from_user_id | to_user_id | transaction_date       |
|---------------|---------|-------------|-----------|----------------------|
| 1             | 1       | 1           | 2         | 2023-03-01 12:00:00  |
| 2             | 2       | 1           | 3         | 2023-07-05 15:30:00  |

---


