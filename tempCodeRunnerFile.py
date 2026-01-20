try:
        # Use connect_adb to bypass the heavy initialization logic
        d = u2.connect_adb() 
        
        # This is the most important line to prevent the "Pause"
        d.settings['wait_for_idle_timeout'] = 0 
        
        # Disable healthcheck so it doesn't restart the agent
        d.healthcheck = False 
        
        serial = d.serial
    except:
        serial = "UNKNOWN"