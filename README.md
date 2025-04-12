# Monitoring-app-for-sandboxing-ubuntu-server
🔍 Secure System Monitoring Service
A lightweight and secure Python-based system monitoring service for tracking CPU, RAM, and network usage in real-time. The service logs abnormal system behaviors and automatically cleans up logs after a period of inactivity.

📦 Features
✅ Monitors CPU and RAM usage

📡 Tracks network input/output activity

📝 Logs alerts with timestamps

🧹 Automatically deletes logs after an idle period

🔁 Runs as a persistent background service using systemd

📁 Project Structure
##########################################################
##########################################################
/opt/monitor/
│
├── monitor.py               # Main monitoring script
└── sandbox-monitor.service  # systemd service file
##########################################################
##########################################################
⚙️ Installation
1. Clone or copy the project to /opt/monitor
##########################################################
##########################################################
sudo mkdir -p /opt/monitor
sudo cp monitor.py /opt/monitor/
##########################################################
##########################################################
3. Install required Python package
##########################################################
##########################################################
sudo apt install python3
sudo /usr/bin/python3 -m pip install psutil
##########################################################
##########################################################
5. Create the systemd service
##########################################################
##########################################################
sudo nano /etc/systemd/system/sandbox-monitor.service
##########################################################
##########################################################
6. Paste the following content:

##########################################################
##########################################################
[Unit]
Description=Secure System Monitoring
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/monitor/monitor.py
Restart=always
RestartSec=5
User=nifo
WorkingDirectory=/opt/monitor
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
Make sure the User has access to the log directory (/home/nifo/ in this case).
##########################################################
##########################################################
🚀 Usage
Start and enable the monitoring service:
##########################################################
##########################################################
sudo systemctl daemon-reload
sudo systemctl enable sandbox-monitor
sudo systemctl start sandbox-monitor
##########################################################
##########################################################
Check the service status:
##########################################################
##########################################################
sudo systemctl status sandbox-monitor
##########################################################
##########################################################
View live logs:
##########################################################
##########################################################
journalctl -u sandbox-monitor -f
📂 Log File
Alerts are saved in:
##########################################################
##########################################################
/path/to/logs.txt
Logs are cleared automatically if no anomalies occur for over 1 hour.

🛡️ Requirements
Python 3.6+

psutil Python package

