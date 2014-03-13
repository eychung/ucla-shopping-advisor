import sys
import ConfigParser
from rlscore import Core
try:
    import psyco
    psyco.full()
except ImportError:
    pass

class MyConfigParser(ConfigParser.ConfigParser):
    """Modification makes this case sensitive"""
    
    def optionxform(self, option):
        return str(option)

def main(cffilename):
    """Runs RLScore based on a configuration file
    @param cffilename: path to the configuration file
    @type cffilename: string
    """
    try:
        configfile = open(cffilename)
    except IOError, e:
        print e
        sys.exit()
    config = MyConfigParser()
    config.readfp(configfile)
    #First Module options which define the loaded core modules
    #which control the learning process
    sections = ["Parameters", "Input", "Output", "Readers", "Writers"]
    dictionaries = []
    for section in sections:
        if config.has_section(section):
            dictionaries.append(dict(config.items(section)))
        else:
            dictionaries.append({})
    core = Core.loadCore(*dictionaries)

if __name__=="__main__":
    if not len(sys.argv)==2 or sys.argv[1]=="-h":
        print "Usage: python rank_svm.py CONFIGFILE"
        sys.exit(0)
    filename = sys.argv[1]
    main(filename)