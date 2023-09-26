# -*- encoding:utf-8 -*-
# @brief:  ......
# @date:   2023.05.10 14:40:50

import os
import sys

g_this_file = os.path.realpath(sys.argv[0])
g_this_path = os.path.dirname(g_this_file)
sys.path.append(os.path.dirname(g_this_path))

from utils.utils_file import FileUtils
from utils.utils_logger import LoggerUtils
from utils.utils_import import ImportUtils
from framework.wing_env import WingEnv
from framework.wing_git import WingGit
from framework.wing_sync import WingSync

ImportUtils.initEnv()


# -----------------------------------------------------------------------------------------------------------------------------
def exportXml(f, name):
    contents = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        '<manifest>\n',
        '<include name="%s" />\n' % name,
        '</manifest>\n'
    ]
    with open(f, 'w') as f: f.writelines(contents)

def createLocalXml(f, branch):
    path = os.path.dirname(f)
    if not os.path.isdir(path): os.makedirs(path)
    contents = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        '<manifest>\n',
        '\n    <remote name="origin" fetch=".."/>\n',
        '\n    <!-- branch -->\n',
        '    <default revision="%s" remote="origin" sync-j="4"/>\n' % branch,
        '\n    <!-- TODO add git here ... -->\n',
        '<!--    <project path="xxx" name="xxx.git" />    -->\n',
        '\n</manifest>\n'
    ]
    with open(f, 'w') as f: f.writelines(contents)


def fetchManifest(spacePath, remote, branch, xml):
    localProject = '.wing' + os.sep + 'manifests'
    if WingEnv.isLocalMode():
        localXml = spacePath + os.sep + localProject + os.sep + xml
        if not os.path.isfile(localXml):
            createLocalXml(localXml, branch)
    else:
        # fetch
        exist = WingGit.fetchGit(localProject, remote)
        # switch branch
        LoggerUtils.light(remote)
        WingGit.fetchBranch('.wing/manifests', branch, True, not exist)
        assert WingGit.checkBranch('.wing/manifests', branch), 'check manifests branch fail'

        # bind remote branch
        # WingGit.bindBranchToRemote('.wing/manifests', branch)

    # export xml
    indexXml = spacePath + '/.wing/manifest.xml'
    exportXml(indexXml, xml)
    assert os.path.isfile(indexXml), 'export manifest.xml fail'


def switchBranch(spacePath, branch):
    fetchManifest(spacePath, WingEnv.getSpaceRemoteManifestGit(), branch, WingEnv.getSpaceManifestFile())
    WingSync.doSync(True, True)
    WingEnv.setSpaceBranch(branch)


def run():
    """
    python wing_init.py {space_path} {env_path} [arguments]
    """
    spacePath, envPath, groupName, branch, manifest = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    WingEnv.init(spacePath, envPath)
    WingEnv.setSpaceName(groupName)
    WingEnv.setSpaceManifestFile(manifest)
    WingEnv.setSpaceBranch(branch)
    FileUtils.remove(WingEnv.getSpacePath() + os.sep + 'out')  # clear out
    fetchManifest(spacePath, WingEnv.getSpaceRemoteManifestGit(), WingEnv.getSpaceBranch(), WingEnv.getSpaceManifestFile())
    WingSync.doSync(True, False)


if __name__ == "__main__":
    run()
