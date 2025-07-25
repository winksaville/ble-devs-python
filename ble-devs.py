#!/usr/bin/env python3
import asyncio
from bleak import BleakScanner

# Add globals if needed

async def cleanup():
    # Import Globals
    # globals xxx
    print("\nCleaning up...")
    # Do any necessary cleanup here
    print("Cleanup complete")

async def run():
    # Import Globals
    # globals xxx

    try:
        print("Discovering BLE devices...")
        devices_and_advs = await BleakScanner.discover(return_adv=True)
        print(f"Found {len(devices_and_advs)} devices:")

        #print(f"devices_and_advs: {devices_and_advs}")
        #print(f"type(devices_and_advs): {type(devices_and_advs)}")
        #print(f"dir(devices_and_advs): {dir(devices_and_advs)}")
        #print(f"type(devices_and_advs.items()): {type(devices_and_advs.items())}")
        #print(f"dir(devices_and_advs.items()): {dir(devices_and_advs.items())}")
        #result = devices_and_advs.items()
        #print(f"result: {result}")

        # The above wasn't particullary useful but with the bots help I got it working
        for (addr, (device, adv)) in devices_and_advs.items():
            #print(f"addr: {addr}, device: {device}, adv: {adv}\n")
            if device.name == "STRIV_RIGHT" or device.name == "STRIV_LEFT":
                print(f"addr: {addr}, device: {device}, adv: {adv}\n")
                uuids = adv.service_uuids
                if uuids:
                    print(f"Service UUIDs: {uuids}")
                else:
                    print("No service UUIDs found.")

            # A delay so I can interrupt with Ctrl+C to test the CancelledError handling
            #await asyncio.sleep(0.1)
        
    # Handle CancelledError specifically so we can inform user
    except asyncio.CancelledError:
        print("\nCanceled (Ctrl+C)")

    # Tell the user there were timeouts as this is odd behavior
    except asyncio.TimeoutError:
        print("\nConnection timed out.")

    # All other exceptions print the error
    except Exception as e:
        print(f"An error occurred: {e}")

    # And finally do any necessary cleanup
    finally:
        await cleanup()
        print("Done")

if __name__ == "__main__":
    asyncio.run(run())
