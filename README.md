# TTN to Traccar Connector

This project allows GPS trackers connected to The Things Network (TTN) to be easily imported into Traccar, an open-source GPS tracking system.

## Features

- Seamless integration between TTN and Traccar
- Automatic import of GPS tracker data
- Easy configuration and setup

## Prerequisites

- Python 3.6+
- Docker (optional, for containerized deployment)
- TTN account and application
- Traccar server

## Usage

Use docker to quickly deploy this service:
```sh
docker run -d \
  --name ttn-traccar-connector \
  --env-file .env \
  nielstiben/ttn-traccar-connector:latest
    -e TRACCAR_OSMAND_URL=http://your-traccar-server-url \
    -e TTN_WEBHOOK_USERNAME=your-ttn-webhook-username \
    -e TTN_WEBHOOK_PASSWORD=your-ttn-webhook-password
```

## Configuration
Create a `.env` file in the project root directory or simply pass the environment variables directly as shown in the 
example above.

### Required Environment Variables
- `TRACCAR_OSMAND_URL`: The URL of the Traccar server.
- `TTN_WEBHOOK_USERNAME`: The username for the TTN webhook.
- `TTN_WEBHOOK_PASSWORD`: The password for the TTN webhook.

### Optional Environment Variables
- `PAYLOAD_KEY_LONGITUDE`: The key for the longitude in the payload (default: "longitude").
- `PAYLOAD_KEY_LATITUDE`: The key for the latitude in the payload (default: "latitude").
- `PAYLOAD_KEY_BATTERY`: The key for the battery level in the payload (default: "battery").

Example `.env` file:

```env
TRACCAR_OSMAND_URL=http://your-traccar-server-url
TTN_WEBHOOK_USERNAME=your-ttn-webhook-username
TTN_WEBHOOK_PASSWORD=your-ttn-webhook-password
PAYLOAD_KEY_LONGITUDE=longitude
PAYLOAD_KEY_LATITUDE=latitude
PAYLOAD_KEY_BATTERY=battery
```
\


## Development

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/ttn-traccar-connector.git
    cd ttn-traccar-connector
    ```
   

2. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```


3. You can use Docker compose to run the application together with a .env file:

    ```sh
    docker-compose build
    docker compose up -d
    ```

## Device ID Forwarding

The device IDs from TTN are forwarded to Traccar. It is important to re-use the same device IDs in Traccar to ensure proper tracking and data consistency.

## TTN Webhook Configuration

This project depends on the TTN webhook configuration. You need to set up a webhook in your TTN application to forward data to this connector. Here is a small explainer on how to configure the TTN webhook:

**Important:** Ensure that the payload keys (by default 'latitude', 'longitude', and 'battery') are in the top-level decoded message dictionary. This can be checked in TTN's console at payload formatters. When testing a payload formatter, the keys should be in the top level. A payload decoder for the SenseCAP T1000 is included in the `payload-formatter` folder.

1. Go to your TTN application console.
2. Navigate to the "Integrations" section.
3. Add a new webhook and configure it with the following details:
    - **Webhook URL**: `http://your-server-url/webhook`
    - **Authentication**: Select HTTP Basic Authentication.
    - **Username**: The username you set in the `.env` file (`TTN_WEBHOOK_USERNAME`).
    - **Password**: The password you set in the `.env` file (`TTN_WEBHOOK_PASSWORD`).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [The Things Network](https://www.thethingsnetwork.org/)
- [Traccar](https://www.traccar.org/)