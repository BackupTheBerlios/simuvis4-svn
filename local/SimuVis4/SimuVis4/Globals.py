# encoding: utf-8
# version:  $Id$
# author:   Joerg Raedler <jr@j-raedler.de>
# license:  GPL v2
# this file is part of the SimuVis4 framework

"""Globals - globally shared objects and settings"""

import Config, logging, sys, os

mainModule = sys.modules['__main__']
version_string = mainModule.version_string
version_info   = mainModule.version_info

appName = 'SimuVis4'
platform = sys.platform
if os.path.isfile(__file__):
    mainPackagePath = os.path.split(__file__)[0]


from logging.handlers import MemoryHandler
logger = logging.getLogger('main')
logger.setLevel(logging.INFO)
# startLogBufffer will cache logging events until the LogWindow is initialized
startLogBuffer = MemoryHandler(100)
logger.addHandler(startLogBuffer)


if platform == 'linux2':
    userName = os.environ['USER']
    hostName = os.environ.get('HOSTNAME')
    if not hostName:
        hostName = os.popen('hostname', 'r').read().strip()
    homePath = os.environ['HOME']
    systemConfigFile   = os.path.join('/etc/', '%s.ini' % appName)
    personalConfigFile = os.path.join(homePath, '.%s.ini' % appName)
    startLogHandler = logging.StreamHandler(sys.stderr)
elif platform == 'win32':
    userName = os.environ['USERNAME']
    hostName = os.environ['COMPUTERNAME']
    homePath = os.environ['USERPROFILE']
    systemConfigFile   = os.path.join(os.environ['ALLUSERSPROFILE'], '%s.ini' % appName)
    personalConfigFile = os.path.join(homePath, '%s.ini' % appName)
    startLogHandler = logging.StreamHandler(sys.stderr)
elif platform == 'macos_x': # FIXME
    pass
else:
    raise "This platform (%s) is not supported by %s!" % (platform, appName)

# startLogHandler will print logging events until the LogWindow is initialized
logger.addHandler(startLogHandler)


config = Config.Config()
configRead = False
if mainModule.forceConfig:
    requestedConfigFile = mainModule.forceConfig
    if os.path.isfile(requestedConfigFile):
        logger.info('Config: reading requested configuration from %s', requestedConfigFile)
        config.read(requestedConfigFile)
        configRead = True
    else:
        mainModule.errorExit('Configuration Error', 'requested config file not found: %s' % requestedConfigFile)
else:
    if os.path.isfile(systemConfigFile):
        logger.info('Config: reading system-wide configuration from %s', systemConfigFile)
        config.read(systemConfigFile)
        configRead = True
    else:
        logger.warning('Config: system-wide config file not found: %s', systemConfigFile)

    if os.path.isfile(personalConfigFile):
        logger.info('Config: reading personal settings from %s', personalConfigFile)
        config.read(personalConfigFile)
        configRead = True
    else:
        logger.warning('Config: personal config file not found: %s', personalConfigFile)


if not configRead or not config.has_section('main'):
    # default configuration values
    config.add_section('main')
    config.set_def('main', 'disable_splash', 'no')
    config.set_def('main', 'splash_image', 'splash2.png')
    config.set_def('main', 'disable_main_menu', 'no')
    config.set_def('main', 'application_icon', 'Icon16.png')
    config.set_def('main', 'application_name', 'SimuVis4')
    if mainModule.qtcore.PYQT_VERSION_STR >= '4.2':
        config.set_def('main', 'background_image', 'background.png')

    config.set_def('main', 'hide_exceptions', 'no')

    config.set_def('main', 'i18n_language', 'de')
    config.set_def('main', 'save_config', 'no')
    config.set_def('main', 'ignore_plugins', 'DummyPlugIn DataStorageBrowser')

    config.set_def('main', 'disable_log_window', 'no')
    config.set_def('main', 'hide_log_window', 'yes')
    config.set_def('main', 'log_threshold', str(logging.INFO))

    config.set_def('main', 'disable_task_browser', 'yes')
    config.set_def('main', 'hide_task_browser', 'yes')

    config.set_def('main', 'disable_plugin_browser', 'no')
    config.set_def('main', 'hide_plugin_browser', 'yes')

    config.set_def('main', 'disable_help_browser', 'no')

    if platform == 'win32':
        # FIXME: there's an error on windows when exiting, somewhere in the logging system...
        config.set_def('main', 'save_last_exception', 'SV4_lastException.txt')

    # try to guess data path:
    dataPath = os.path.join(mainModule.baseDir, 'data')
    if not os.path.isdir(dataPath):
        # already installed, but not configured correctly?
        dataPath = os.path.join(mainModule.baseDir, 'lib', 'SimuVis4')
    if not os.path.isdir(dataPath):
        logger.error('Config: could not guess data path, SimuVis may not work correctly!')
    config.set_def('main', 'system_data_path', dataPath)
    config.set_def('main', 'system_plugin_path', os.path.join(dataPath, 'PlugIns'))
    config.set_def('main', 'system_picture_path', os.path.join(dataPath, 'Pictures'))
    config.set_def('main', 'system_language_path', os.path.join(dataPath, 'Language'))
    config.set_def('main', 'system_help_path', os.path.join(dataPath, 'Help'))

    config.set_def('main', 'user_plugin_path', os.path.join(mainModule.baseDir, '..', 'AdditionalPlugIns'))

    config.set_def('main', 'user_work_path', os.getcwd())

defaultFolder = config['main:user_work_path']

logger.setLevel(config.getint('main', 'log_threshold'))

