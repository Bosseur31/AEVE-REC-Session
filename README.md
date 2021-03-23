# AEVE-REC-Session REST Server
                                                   
## API
- An `HTTP 200 OK` will be returned if the call was successful.
- An `HTTP 400 BAD REQUEST` will be returned if a request was malformed or if a given resource was not found.
- An `HTTP 409 CONFLICT ` will be returned if a request attempted to create/update a resource that conflicts with an existing resource.
- All responses are in JSON format.

Endpoint | HTTP Method | Description
-------- | ----------- | -----------
`/discoverblasters` | `GET` | Discovers all new Broadlink RM blasters and adds them to the database (Note: blasters must be in the database before they can be used by the application, and they must be on and connected to the local network to be discoverable. You can add the Broadlink devices to your network using the instructions [here](https://github.com/mjg59/python-broadlink#example-use)). Blasters will be added to the database unnamed, so it's recommended to use `PUT /blasters/<attr>/<value>?new_name=<new_name>` to set a friendly name for each blaster.<br><br>NOTE: Discovery will also update blaster IP addresses when applicable.
`/blasters` | `GET` | Gets all blasters (only returns blasters that have already been discovered once). | 
`/blasters?target_name=<target_name>&command_name=<command_name>` | `POST` | Sends command `<command_name>` for target `<target_name>` to all blasters.
`/blasters/<attr>/<value>` | `GET` | Gets specified blaster. `<attr>` should be either `ip`, `mac`, or `name`, and `<value>` should be the corresponding value.
`/blasters/<attr>/<value>` | `DELETE` | Deletes specified blaster. `<attr>` should be either `ip`, `mac`, or `name`, and `<value>` should be the corresponding value.
`/blasters/<attr>/<value>?new_name=<new_name>` | `PUT` | Sets blasters name to `<new_name>`, replacing an existing name if it already exists. `<attr>` should be either `ip`, `mac`, or `name`, and `<value>` should be the corresponding value.<br><br>NOTE: If blaster lookup via IP isn't working, try to rediscover blasters using /discoverblasters which will update IP addresses to their latest.
`/blasters/<attr>/<value>?target_name=<target_name>&command_name=<command_name>` | `POST` | Sends command `<command_name>` for target `<target_name>` via specified blaster. `<attr>` should be either `ip`, `mac`, or `name`, and `<value>` should be the corresponding value.<br><br>NOTE: If blaster lookup via IP isn't working, try to rediscover blasters using /discoverblasters which will update IP addresses to their latest.
`/blasters/<attr>/<value>/status` | `GET` | Verifies availability of specified blaster. `<attr>` should be either `ip`, `mac`, or `name`, and `<value>` should be the corresponding value. Returns an `HTTP 200 OK` if the blaster responds to status check within the `BROADLINK_STATUS_TIMEOUT` timeout window, else returns an `HTTP 408 GATEWAY TIMEOUT`.
`/commands` | `GET` | Gets all commands.
`/targets` | `GET` | Gets all targets.
`/targets/<target_name>` | `PUT` | Creates target `<target_name>`.
`/targets/<target_name>` | `DELETE` | Deletes target `<target_name>` and all of its associated commands.
`/targets/<target_name>?new_name=<new_name>` | `PATCH` | Updates the name of `<target_name>` to `<new_name>`.
`/targets/<target_name>/commands` | `GET` | Gets all commands for target `<target_name>`.
`/targets/<target_name>/commands/<command_name>` | `GET` | Gets command `<command_name>` for target `<target_name>`.
`/targets/<target_name>/commands/<command_name>` | `DELETE` | Deletes command `<command_name>` for target `<target_name>`.
`/targets/<target_name>/commands/<command_name>?new_name=<new_name>` | `PATCH` | Updates command name of  `<command_name>` for target `<target_name>` to `<new_name>`.
`/targets/<target_name>/commands/<command_name>?blaster_attr=<blaster_attr>&blaster_value=<blaster_value>` | `PUT` | Learns command `<command_name>` for target `<target_name>` using specified blaster. `<blaster_attr>` should be either `ip`, `mac`, or `name` and `<blaster_value>` should be the corresponding value. If `<command_name>` already exists, it will be replaced with the new value. Waits for ~10 seconds to detect an input signal from the blaster specified before timing out and consequently returning an `HTTP 408 GATEWAY TIMEOUT`.<br><br>NOTE: If blaster lookup via IP isn't working, try to rediscover blasters using /discoverblasters which will update IP addresses to their latest.
`/targets/<target_name>/commands/<command_name>?value=<value>` | `PUT` | Sets the value command `<command_name>` for target `<target_name>` to `<value>`. If `<command_name>` already exists, it will be replaced with the new value. If you plan to use this method, you should look at the code to see how values are encoded, or use existing command values in the database.

## Shout outs
1. @raman325 for [broadlink-rm-rest](https://github.com/raman325/broadlink-rm-rest) Base of this work
2. @falconry for [falcon](https://github.com/falconry/falcon). This is my first REST app and [falcon](https://github.com/falconry/falcon) made it a breeze.
3. @coleifer for [peewee](https://github.com/coleifer/peewee) which made persisting the data simple.


