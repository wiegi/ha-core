import serial_asyncio


class USBDevice:
    """Dummy-Klasse für das Testen der USB-Verbindung."""

    def __init__(self, device_path: str, baudrate: int = 57600) -> None:
        """Initialisieren."""
        self.device_path = device_path
        self.baudrate = baudrate

    async def check_connection(self) -> bool:
        """Check if the USB device is reachable."""
        try:
            # Attempt to open the serial connection
            reader, writer = await serial_asyncio.open_serial_connection(
                url=self.device_path, baudrate=self.baudrate
            )

            # Close the writer after successful connection
            writer.close()
            await writer.wait_closed()

            return True  # Connection successful
        except Exception as e:
            print(f"Error opening serial connection: {e}")
            return False  # Connection failed
        finally:
            # Ensure the writer is closed in case of an exception
            if "writer" in locals() and not writer.is_closing():
                writer.close()
                await writer.wait_closed()
