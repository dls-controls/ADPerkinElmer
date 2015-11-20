from iocbuilder import Device, AutoSubstitution, SetSimulation
from iocbuilder.arginfo import *

from iocbuilder.modules.ADCore import ADCore, ADBaseTemplate, includesTemplates, makeTemplateInstance
from iocbuilder.modules.asyn import AsynPort

@includesTemplates(ADBaseTemplate)
class _perkinElmerTemplate(AutoSubstitution):
    TemplateFile = "PerkinElmer.template"

class perkinElmer(AsynPort):
    """Creates a Perkin Elmer areaDetector driver"""
    Dependencies = (ADCore,)
    _SpecificTemplate = _perkinElmerTemplate
    UniqueName = "PORT"
    
    def __init__(self, PORT, IDType, IDValue = "", BUFFERS = 50, MEMORY = 0, **args):
        # Init the superclass
        self.__super.__init__(PORT)
        self.__dict__.update(locals())
        makeTemplateInstance(self._SpecificTemplate, locals(), args)

    # __init__ arguments
    ArgInfo = _SpecificTemplate.ArgInfo + makeArgInfo(__init__,
        PORT = Simple('Port name for the detector', str),
        IDType = Choice('Type of system ID in IDValue',
                        [0,1,2,3],
                        ["0.Frame grabber card, leave IDValue empty",
                         "1.GigE detector, IDValue = IP address",
                         "2.GigE detector, IDValue = MAC address lower-case",
                         "3.GigE detector, IDValue = detector name"]),
        IDValue = Simple('System ID', str),
        BUFFERS = Simple('Maximum number of NDArray buffers to be created for '
            'plugin callbacks', int),
        MEMORY = Simple('Max memory to allocate, should be maxw*maxh*nbuffer '
            'for driver and all attached plugins', int))

    # Device attributes
    LibFileList = ['PerkinElmer','XISL']
    DbdFileList = ['PerkinElmerSupport']

    # Copy the libraries
    MakefileStringList = \
            [ 
                'USR_CFLAGS=   /DWINVER=0x0502 /D_WIN32_WINNT=0x0502 /D_WIN32_WINDOWS=0x0502',
                'USR_CXXFLAGS=   /DWINVER=0x0502 /D_WIN32_WINNT=0x0502 /D_WIN32_WINDOWS=0x0502',
                'USR_CPPFLAGS=   /DWINVER=0x0502 /D_WIN32_WINNT=0x0502 /D_WIN32_WINDOWS=0x0502',
                'BIN_INSTALLS_WIN32 += $(ADPERKINELMER)/ADApp/perkinElmerSupport/os/windows-x64/msvcr100.dll']

    def Initialise(self):
        print '#PerkinElmerConfig(const char *portName, int IDType, const char* IDValue, \
            int maxBuffers, size_t maxMemory, int priority, int stackSize )'
        print 'PerkinElmerConfig("%(PORT)s", %(IDType)s, \"%(IDValue)s\", %(BUFFERS)d, ' \
            '%(MEMORY)d, 0, 0)' % self.__dict__

