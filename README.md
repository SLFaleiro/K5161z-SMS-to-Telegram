# SMS-to-Telegram Bridge

![Python Version](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Tested Device](https://img.shields.io/badge/Tested%20Device-Vodafone%20K5161z-brightgreen.svg)

A Python service that forwards SMS messages from 4G modems to Telegram, with automatic message deletion after forwarding. Tested specifically with Vodafone K5161z hardware.

## Features

- Automatically checks for new SMS messages
- Forwards messages to Telegram
- Deletes processed messages from modem
- Runs continuously with configurable polling interval
- Error logging and handling
- No external dependencies beyond Python standard libraries
- Tested with Vodafone K5161z hardware

## Compatible Hardware
Tested with:
- **Device Name**: Vodafone Mobile Broadband
- **Model**: K5161z
- **Software Version**: BD0_K5161zV2.7
- **Hardware Version**: Ver.B(T2)

Should work with any modem that uses similar:
1. Web interface at `http://192.168.6.1`
2. SMS API endpoints:
   - `/goform/goform_get_cmd_process` (GET)
   - `/goform/goform_set_cmd_process` (POST)

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/sms-to-telegram-bridge.git
   cd sms-to-telegram-bridge
   ```

2. **Configure the script:**
   Edit `sms_bridge.py` with your details:
   ```python
   # Modem configuration (Vodafone K5161z default)
   SMS_SERVER_URL = 'http://192.168.6.1'
   REFERER_HEADER = {'Referer': 'http://192.168.6.1/index.html'}
   
   # Telegram configuration
   TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN'  # From @BotFather
   TELEGRAM_CHAT_ID = 'YOUR_CHAT_ID'     # Group/channel ID
   
   # Polling interval (seconds)
   POLL_INTERVAL = 10
   ```

3. **Create Telegram bot:**
   - Message @BotFather on Telegram
   - Use `/newbot` command
   - Copy the API token

4. **Get Chat ID:**
   - Add bot to your group/channel
   - Visit: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
   - Look for `chat.id` in JSON response

## Running the Service

### Manual Run:
```bash
python3 sms_bridge.py
```

### As Background Service (Linux):
1. Create systemd service:
   ```bash
   sudo nano /etc/systemd/system/sms-bridge.service
   ```
2. Add configuration:
   ```ini
   [Unit]
   Description=SMS to Telegram Bridge
   After=network.target

   [Service]
   User=root
   WorkingDirectory=/path/to/sms-to-telegram-bridge
   ExecStart=/usr/bin/python3 /path/to/sms-to-telegram-bridge/sms_bridge.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```
3. Enable and start:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable sms-bridge
   sudo systemctl start sms-bridge
   ```

## Viewing Logs
```bash
tail -f sms_bridge.log
```

## Vodafone K5161z Notes
1. Ensure SMS storage is set to "Device" (not SIM) in modem settings
2. Web interface must be accessible without authentication
3. The modem typically assigns itself `192.168.6.1` by default
4. SMS decoding handles UTF-16BE format used by this device

## Security Notes
- Ensure your modem's web interface is not exposed to the internet
- Keep Telegram bot token private
- Use private Telegram groups/channels
- Regularly rotate credentials
- The Referer header is required for API access

## Troubleshooting
| Error | Solution |
|-------|----------|
| Connection errors | Verify modem IP is reachable |
| 403 Forbidden | Check Referer header matches modem URL |
| Empty messages | Confirm SMS storage is set to Device |
| Telegram failures | Verify bot token/chat ID permissions |
| Decoding errors | Confirm message encoding is UTF-16BE |

## License
MIT License - See [LICENSE](LICENSE) file

---

**Tested Device Information:**  
**Name:** Vodafone Mobile Broadband  
**Model:** K5161z  
**Software Version:** BD0_K5161zV2.7  
**Hardware Version:** Ver.B(T2)  

**Note:** Always test with non-critical messages first. Not responsible for lost messages or service interruptions.
