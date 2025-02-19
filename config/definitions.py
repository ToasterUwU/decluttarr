#### Turning off black formatting
# fmt: off
from config.parser import get_config_value
from config.env_vars import *
# Define data types and default values for settingsDict variables
# General   
LOG_LEVEL                       = get_config_value('LOG_LEVEL',                     'general',      False,  str,    'INFO')
TEST_RUN                        = get_config_value('TEST_RUN',                      'general',      False,  bool,   False)
SSL_VERIFICATION                = get_config_value('SSL_VERIFICATION',              'general',      False,  bool,   True)

# Features  
REMOVE_TIMER                    = get_config_value('REMOVE_TIMER',                  'features',     False,  float,  10)
REMOVE_FAILED                   = get_config_value('REMOVE_FAILED',                 'features',     False,  bool,   False)
REMOVE_FAILED_IMPORTS           = get_config_value('REMOVE_FAILED_IMPORTS' ,        'features',     False,  bool,   False)
REMOVE_METADATA_MISSING         = get_config_value('REMOVE_METADATA_MISSING',       'features',     False,  bool,   False)
REMOVE_MISSING_FILES            = get_config_value('REMOVE_MISSING_FILES',          'features',     False,  bool,   False)
REMOVE_NO_FORMAT_UPGRADE        = get_config_value('REMOVE_NO_FORMAT_UPGRADE',      'features',     False,  bool,   False) # OUTDATED - WILL RETURN WARNING
REMOVE_ORPHANS                  = get_config_value('REMOVE_ORPHANS',                'features',     False,  bool,   False)
REMOVE_SLOW                     = get_config_value('REMOVE_SLOW',                   'features',     False,  bool,   False)
REMOVE_STALLED                  = get_config_value('REMOVE_STALLED',                'features',     False,  bool,   False)
REMOVE_UNMONITORED              = get_config_value('REMOVE_UNMONITORED',            'features',     False,  bool,   False)
RUN_PERIODIC_RESCANS            = get_config_value('RUN_PERIODIC_RESCANS',          'features',     False,  dict,   {})

# Feature Settings
MIN_DOWNLOAD_SPEED              = get_config_value('MIN_DOWNLOAD_SPEED',            'feature_settings',     False,  int,    0)
PERMITTED_ATTEMPTS              = get_config_value('PERMITTED_ATTEMPTS',            'feature_settings',     False,  int,    3)
NO_STALLED_REMOVAL_QBIT_TAG     = get_config_value('NO_STALLED_REMOVAL_QBIT_TAG',   'feature_settings',     False,  str,   'Don\'t Kill')
IGNORE_PRIVATE_TRACKERS         = get_config_value('IGNORE_PRIVATE_TRACKERS',       'feature_settings',     False,  bool,   True)
FAILED_IMPORT_MESSAGE_PATTERNS  = get_config_value('FAILED_IMPORT_MESSAGE_PATTERNS','feature_settings',     False,  list,   [])
IGNORED_DOWNLOAD_CLIENTS        = get_config_value('IGNORED_DOWNLOAD_CLIENTS',      'feature_settings',     False,  list,   [])

# Radarr
RADARR_URL                      = get_config_value('RADARR_URL',                    'radarr',       False,  str)
RADARR_KEY                      = None if RADARR_URL == None else \
                                  get_config_value('RADARR_KEY',                    'radarr',       True,   str)

# Sonarr        
SONARR_URL                      = get_config_value('SONARR_URL',                    'sonarr',       False,  str)
SONARR_KEY                      = None if SONARR_URL == None else \
                                  get_config_value('SONARR_KEY',                    'sonarr',       True,   str)

# Lidarr        
LIDARR_URL                      = get_config_value('LIDARR_URL',                    'lidarr',       False,  str)
LIDARR_KEY                      = None if LIDARR_URL == None else \
                                  get_config_value('LIDARR_KEY',                    'lidarr',       True,   str)

# Readarr       
READARR_URL                     = get_config_value('READARR_URL',                   'readarr',       False,  str)
READARR_KEY                     = None if READARR_URL == None else \
                                  get_config_value('READARR_KEY',                   'readarr',       True,   str)

# Whisparr    
WHISPARR_URL                    = get_config_value('WHISPARR_URL',                  'whisparr',       False,  str)
WHISPARR_KEY                    = None if WHISPARR_URL == None else \
                                  get_config_value('WHISPARR_KEY',                  'whisparr',       True,   str)

# qBittorrent   
QBITTORRENT_URL                 = get_config_value('QBITTORRENT_URL',               'qbittorrent',  False,  str,    '')
QBITTORRENT_USERNAME            = get_config_value('QBITTORRENT_USERNAME',          'qbittorrent',  False,  str,    '')
QBITTORRENT_PASSWORD            = get_config_value('QBITTORRENT_PASSWORD',          'qbittorrent',  False,  str,    '')

########################################################################################################################
########### Validate settings
if not (IS_IN_PYTEST or RADARR_URL or SONARR_URL or LIDARR_URL or READARR_URL or WHISPARR_URL):
    print(f'[ ERROR ]: No Radarr/Sonarr/Lidarr/Readarr/Whisparr URLs specified (nothing to monitor)')
    exit()


#### Validate rescan settings
PERIODIC_RESCANS = get_config_value("PERIODIC_RESCANS", "features", False, dict, {})

rescan_supported_apps = ["SONARR", "RADARR"]
rescan_default_values = {
    "MISSING": (True, bool),
    "CUTOFF_UNMET": (True, bool),
    "MAX_CONCURRENT_SCANS": (3, int),
    "MIN_DAYS_BEFORE_RESCAN": (7, int),
}


# Remove rescan apps that are not supported
for key in list(RUN_PERIODIC_RESCANS.keys()):
    if key not in rescan_supported_apps:
        print(f"[ WARNING ]: Removed '{key}' from RUN_PERIODIC_RESCANS since only {rescan_supported_apps} are supported.")
        RUN_PERIODIC_RESCANS.pop(key)

# Ensure SONARR and RADARR have the required parameters with default values if they are present
for app in rescan_supported_apps:
    if app in RUN_PERIODIC_RESCANS:
        for param, (default, expected_type) in rescan_default_values.items():
            if param not in RUN_PERIODIC_RESCANS[app]:
                print(f"[ INFO ]: Adding missing parameter '{param}' to '{app}' with default value '{default}'.")
                RUN_PERIODIC_RESCANS[app][param] = default
            else:
                # Check the type and correct if necessary
                current_value = RUN_PERIODIC_RESCANS[app][param]
                if not isinstance(current_value, expected_type):
                    print(
                        f"[ INFO ]: Parameter '{param}' for '{app}' must be of type {expected_type.__name__} and found value '{current_value}' (type '{type(current_value).__name__}'). Defaulting to '{default}'."
                    )
                    RUN_PERIODIC_RESCANS[app][param] = default

########### Enrich setting variables
if RADARR_URL:      RADARR_URL =        RADARR_URL.rstrip('/')      + '/api/v3'
if SONARR_URL:      SONARR_URL =        SONARR_URL.rstrip('/')      + '/api/v3'
if LIDARR_URL:      LIDARR_URL =        LIDARR_URL.rstrip('/')      + '/api/v1'
if READARR_URL:     READARR_URL =       READARR_URL.rstrip('/')     + '/api/v1'
if WHISPARR_URL:    WHISPARR_URL =      WHISPARR_URL.rstrip('/')    + '/api/v3'
if QBITTORRENT_URL: QBITTORRENT_URL =   QBITTORRENT_URL.rstrip('/') + '/api/v2'


RADARR_MIN_VERSION = "5.3.6.8608"
if "RADARR" in PERIODIC_RESCANS:
    RADARR_MIN_VERSION = "5.10.3.9171"

SONARR_MIN_VERSION = "4.0.1.1131"
if "SONARR" in PERIODIC_RESCANS:
    SONARR_MIN_VERSION = "4.0.9.2332"
LIDARR_MIN_VERSION          = None
READARR_MIN_VERSION         = None
WHISPARR_MIN_VERSION        = '2.0.0.548'
QBITTORRENT_MIN_VERSION     = '4.3.0'

SUPPORTED_ARR_APPS  = ['RADARR', 'SONARR', 'LIDARR', 'READARR', 'WHISPARR']

########### Add Variables to Dictionary
settingsDict = {}
for var_name in dir():
    if var_name.isupper():
        settingsDict[var_name] = locals()[var_name]
