import tornado,os
from tornado.options import define, options, parse_config_file


define("serverurl", default="basicurl")

def main():
    parse_config_file(os.path.abspath('')+'/options.conf')

    print(options.serverurl)

if __name__ == '__main__':
    main()
