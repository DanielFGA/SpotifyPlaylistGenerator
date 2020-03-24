class Properties(object):

    def __init__(self):
        properties = open('settings.properties', 'r').read()
        config = {}
        for line in properties.split('\n'):
            if (len(line)) == 0:
                break
            prop = line.split('=')
            config[prop[0]] = prop[1]

        self.client_id = config.get("ClientID")
        self.client_secret = config.get("ClientSecret")
        self.redirect_url = config.get("AuthCallback")
        self.host = config.get("Host") if config.get("Host") != "null" else None
