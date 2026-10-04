import json
import logging
from pathlib import Path

import paho.mqtt.client as mqtt


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)

CONFIG_FILE = Path(__file__).with_name("config.json")


def load_config():
    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        config = json.load(file)

    required = ("broker", "port", "username", "password", "topic")
    missing = [key for key in required if not config.get(key)]

    if missing:
        raise ValueError(
            f"Missing or empty configuration values: {', '.join(missing)}"
        )

    return config


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        logging.error("MQTT connection failed: %s", reason_code)
        return

    logging.info("Connected to MQTT broker")
    result, message_id = client.subscribe(CONFIG["topic"], qos=1)

    if result == mqtt.MQTT_ERR_SUCCESS:
        logging.info("Subscribed to topic: %s", CONFIG["topic"])
    else:
        logging.error("Subscription request failed: %s", result)


def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8", errors="replace")

    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        logging.warning("Received non-JSON message on %s", message.topic)
        return

    logging.info("Topic: %s", message.topic)
    logging.info(
        "Payload: %s",
        json.dumps(data, ensure_ascii=False),
    )


def main():
    global CONFIG
    CONFIG = load_config()

    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id="plant1_python_subscriber",
        protocol=mqtt.MQTTv311,
    )

    client.username_pw_set(
        CONFIG["username"],
        CONFIG["password"],
    )

    client.on_connect = on_connect
    client.on_message = on_message
    client.reconnect_delay_set(min_delay=1, max_delay=30)

    logging.info(
        "Connecting to MQTT broker at %s:%s",
        CONFIG["broker"],
        CONFIG["port"],
    )

    client.connect(
        CONFIG["broker"],
        int(CONFIG["port"]),
        keepalive=60,
    )

    client.loop_forever()


if __name__ == "__main__":
    main()
