import argparse
import sys

from iot_rst_button import default_config
from iot_rst_button import rst_button_handler

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=default_config.serviceDescription)
    parser.add_argument('--config', default='/config/rst_button.cfg')
    args = parser.parse_args() 

    rst_button_handler.startHandler(config=args.config)
