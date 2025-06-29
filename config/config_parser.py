from configparser import ConfigParser, SectionProxy
from pathlib import Path


CONFIG_FILE_PATH = Path(__file__).parent.parent.absolute() / 'config.ini'

config: ConfigParser = ConfigParser()
config.read(CONFIG_FILE_PATH)

general_config: SectionProxy = config['GENERAL']
brain_ring_config: SectionProxy = config['BRAIN_RING']
www_config: SectionProxy = config['WHAT_WHERE_WHEN']
erudite_config: SectionProxy = config['ERUDITE']
player_buttons_config: SectionProxy = config['PLAYER_BUTTONS']
moderator_buttons_config: SectionProxy = config['MODERATOR_BUTTONS']
