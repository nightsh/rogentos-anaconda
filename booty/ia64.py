from booty import BootyNoKernelWarning
from bootloaderInfo import *

class ia64BootloaderInfo(efiBootloaderInfo):
    def getBootloaderConfig(self, instRoot, bl, kernelList,
                            chainList, defaultDev):
        config = bootloaderInfo.getBootloaderConfig(self, instRoot,
                                                    bl, kernelList, chainList,
                                                    defaultDev)
        # altix boxes need relocatable (#120851)
        config.addEntry("relocatable")

        return config
            
    def writeLilo(self, instRoot, bl, kernelList, 
                  chainList, defaultDev, justConfig):
        config = self.getBootloaderConfig(instRoot, bl,
                                          kernelList, chainList, defaultDev)
        config.write(instRoot + self.configfile, perms = 0755)

        return ""
        
    def write(self, instRoot, bl, kernelList, chainList,
            defaultDev, justConfig):
        if len(kernelList) >= 1:
            out = self.writeLilo(instRoot, bl, kernelList, 
                                 chainList, defaultDev, justConfig)
        else:
            raise BootyNoKernelWarning

        self.removeOldEfiEntries(instRoot)
        self.addNewEfiEntry(instRoot)

    def makeInitrd(self, kernelTag):
        return "/boot/efi/EFI/redhat/initrd%s.img" % kernelTag

    def __init__(self, storage):
        efiBootloaderInfo.__init__(self, storage)
        self._configname = "elilo.conf"
        self._bootloader = "elilo.efi"