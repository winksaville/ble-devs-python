#!/usr/bin/env python3
import argparse
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

    # Optional parameter
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--algorithm",
        choices=["simple", "pretty", "s", "p"],
        default="simple",
        help="Algorithm to use: simple(s) or pretty(p). Default: simple"
    )
    args = parser.parse_args()

    # Normalize abbreviations
    algo = "simple" if args.algorithm in ["simple", "s"] else "pretty"
    print(f"Algorithm: {algo}")

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

        ## The above wasn't particullary useful but with the bots help I got it working
        #for (addr, (device, adv)) in devices_and_advs.items():
        #    #print(f"addr: {addr}, device: {device}, adv: {adv}\n")

        #    # We should always an address and device details
        #    a = device.address or "Unknown Address"
        #    d = device.details or "No details"

        #    # The device.address should match the addr from the dict
        #    assert a == addr, "Address mismatch"
        #    print(f"Address: {a}, Details: {d}")

        #    # On the next line we'll print the device name and service UUIDs if the exist on one line
        #    leading = "  "
        #    something = False
        #    if n := device.name:
        #        print(f"{leading} name: '{n}'", end="")
        #        leading = " "
        #        something = True
        #    if uuids := adv.service_uuids:
        #        print(f"{leading}uuids: {uuids}", end="")
        #        something = True
        #    if something:
        #        print()

        #    # A delay so I can interrupt with Ctrl+C to test the CancelledError handling
        #    #await asyncio.sleep(0.1)

        #for addr, (device, adv) in devices_and_advs.items():
        #    a = device.address or "Unknown Address"
        #    d = device.details or "No details"

        #    # First line
        #    print(f"Address: {a}, Details: {d}")

        #    # Optional fields
        #    fields = {
        #        "name": device.name,
        #        "uuids": adv.service_uuids,
        #    }

        #    filtered = {k: v for k, v in fields.items() if v}
        #    if filtered:
        #        # Align colons to match "Address:" which is 8 chars (colon at pos 8)
        #        # So: field names should be right-aligned to width 7, colon at pos 8
        #        width = 7
        #        line = "  " + " ".join(f"{k:>{width}}: {v!r}" for k, v in filtered.items())
        #        print(line)

        #for addr, (device, adv) in devices_and_advs.items():
        #    # First-line fields
        #    first_line_fields = {
        #        "Address": device.address or "Unknown Address",
        #        "Details": device.details or "No details",
        #    }

        #    # Second-line optional fields
        #    second_line_optional_fields = {
        #        "name": device.name,
        #        "uuids": adv.service_uuids,
        #        # Add more optional fields here if needed
        #    }

        #    # Compute dynamic width across ALL keys
        #    all_keys = list(first_line_fields.keys()) + list(second_line_optional_fields.keys())
        #    width = max(len(k) for k in all_keys)

        #    # Print first line
        #    print(" ".join(f"{k:>{width}}: {v!r}" for k, v in first_line_fields.items()))

        #    # Print second line if any optional fields exist
        #    filtered = {k: v for k, v in second_line_optional_fields.items() if v}
        #    if filtered:
        #        print(" ".join(f"{k:>{width}}: {v!r}" for k, v in filtered.items()))
        
        # I like this simpler version but it adds ", " at the end of the second line if only one field
        #for addr, (device, adv) in devices_and_advs.items():
        #    first_line = f"address: {device.address or 'Unknown Address'}, details: {device.details or 'No details'}"
        #    first_line_colon = first_line.find(":")
        #    print(first_line)

        #    # Second-line optional fields and none may exist in which case there is no second line
        #    second_line_optional_fields = {
        #        "name": device.name,
        #        "uuids": adv.service_uuids,
        #        # Add more optional fields here if needed
        #    }

        #    # Print second line if any optional fields exist
        #    filtered = {k: v for k, v in second_line_optional_fields.items() if v}
        #    if filtered:
        #        it = iter(filtered.items())
        #        k, v = next(it)
        #        print(f"{k:>{first_line_colon}}: {v!r}", end="")
        #        print(", " + " ".join(f"{k}: {v!r}" for k, v in it))

        # I asked the bot to help me with this and it suggeseted
        # the following which convertes the second line into a filtered
        # list so that we can test if there is 0, 1 or more optional fields
        # and print them accordingly.
        match algo:
            case "pretty" | "p":
                for addr, (device, adv) in devices_and_advs.items():
                    first_line = f"address: {device.address or 'Unknown Address'}, details: {device.details or 'No details'}"
                    first_line_colon = first_line.find(":")
                    print(first_line)

                    # Second-line optional fields and none may exist in which case there is no second line
                    second_line_optional_fields = {
                        "name": device.name,
                        "uuids": adv.service_uuids,
                        # Add more optional fields here if needed
                    }

                    # Create a filtered list of Key Value tuples for the second line
                    # it may be empty if no optional fields exist
                    filtered = [(k, v) for k, v in second_line_optional_fields.items() if v]

                    if filtered:
                        # Print first item with alignment
                        k, v = filtered[0]
                        print(f"{k:>{first_line_colon}}: {v!r}", end="")

                        # Print remaining items separated by comma
                        if len(filtered) > 1:
                            print(", " + "".join(f"{k}: {v!r}" for k, v in filtered[1:]))
                        else:
                            print()
            case "simple" | "s":
                # Simpler more efficient version but always prints a trailing comma
                for addr, (device, adv) in devices_and_advs.items():
                    first_key = "address"
                    print(f"{first_key}: {device.address or 'Unknown Address'}, details: {device.details or 'No details'}")
                    first_line_colon = len(first_key)

                    # Second-line optional fields and none may exist in which case there is no second line
                    second_line_optional_fields = {
                        "name": device.name,
                        "uuids": adv.service_uuids,
                        # Add more optional fields here if needed
                    }

                    # Loop throught all the second line optional fields printing any that have a value
                    # on a single line. The first item is right justified to align the colons with
                    # the first line, the rest are not aligned. This simplified code will always
                    # print a trailing comma if there are any optional fields, ugly but efficient.
                    for k, v in second_line_optional_fields.items():
                        if v:
                            # We printed the first item right justififed to align colons
                            print(f"{k:>{first_line_colon}}: {v!r}, ", end="")
                            first_line_colon = 0 # for the rest we don't need to align
                    # If we printed at least one optional field add a newline
                    if first_line_colon == 0:
                        print()
            case _:
                print("Unknown algorithm specified. Use 'simple' or 'pretty'.")


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
