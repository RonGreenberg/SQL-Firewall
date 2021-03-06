# SQL Firewall
A tool for detection of SQL Injection attempts, created together with [Itamar Azmoni](https://github.com/Itamar-Azmoni) as part of Colman Hackathon 2022, sponsored by [Spot](https://github.com/spotinst).
Won 3rd place along with [the project of the rest of our team](https://github.com/avivk9/AWS_anomaly_detection).

![injection_detection](https://user-images.githubusercontent.com/89278943/161638964-69aa04e4-f03f-4deb-8764-d93845af112b.jpeg)

## Setup
First run [CreateDB.py](source/CreateDB.py), a script that automatically creates and generates records for the local MySQL database required for the test queries.
You don't have to run the script again from now on, unless you manually delete the database at some point.

## Usage
Run [httpServer.py](source/httpServer.py), a local HTTP server hosted on port 5555. Connect to localhost:5555 using a browser. The HTML page will be presented. You can choose one of the example queries and either use the auto-generated user input that is an injection attempt, or enter an input of your own (if it's not an injection attempt, the result of the query will be shown as a table).\
You can edit the [configurations.ini](source/configurations.ini) file to configure which known injection cases to check for, and define lists of blocked keywords or literals. Changes to the file can take effect even while the server is running.
