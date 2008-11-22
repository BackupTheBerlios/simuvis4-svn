## $Id$
##
## BEGIN LICENSE BLOCK
##
## Copyright (C) 2002  Damon Courtney
## 
## This program is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License
## version 2 as published by the Free Software Foundation.
## 
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License version 2 for more details.
## 
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the
##     Free Software Foundation, Inc.
##     51 Franklin Street, Fifth Floor
##     Boston, MA  02110-1301, USA.
##
## END LICENSE BLOCK

if {[info exists ::InstallJammer]} { return }

namespace eval ::InstallAPI {}
namespace eval ::InstallJammer {}

set ::debug   0
set ::verbose 0

set ::conf(osx)      [string equal $::tcl_platform(os) "Darwin"]
set ::conf(unix)     [string equal $::tcl_platform(platform) "unix"]
set ::conf(windows)  [string equal $::tcl_platform(platform) "windows"]

set ::conf(threaded) [info exists ::tcl_platform(threaded)]

set ::info(Testing)   0
set ::info(Debugging) 0

## Trace the virtual text array for changes and execute any
## attached commands or auto-update actions.
trace add variable ::info write ::InstallJammer::VirtualTextTrace

proc ::InstallJammer::VirtualTextTrace { name1 name2 op } {
    upvar #0 ::info($name2) var

    if {[info exists ::InstallJammer::UpdateVarCmds($name2)]} {
        foreach cmd $::InstallJammer::UpdateVarCmds($name2) {
            uplevel #0 $cmd
        }
    }

    if {[info exists ::InstallJammer::AutoUpdateVars($name2)]
        && $var ne $::InstallJammer::AutoUpdateVars($name2)} {
        set ::InstallJammer::AutoUpdateVars($name2) $var
        ::InstallJammer::UpdateWidgets -updateidletasks 1
    }
}

proc ::InstallJammer::SourceCachedFile { file {namespace "::"} } {
    if {[info exists ::InstallJammer::files($file)]} {
        namespace eval $namespace $::InstallJammer::files($file)
        return 1
    }
    return 0
}

namespace eval ::InstallAPI {}
namespace eval ::InstallJammer {}
set conf(version)     1.2.10
set info(Platform)    Linux-x86
set info(InstallerID) 96AE5542-4DC5-D6A6-CA75-4EA19E07A4B7
array set ::InstallJammer::languagecodes {de German en English ru Russian}
array set info {
AllowLanguageSelection
Yes

AppName
SimuVis4

ApplicationID
F9F8894E-C0E8-F46F-7665-4E34355EABEA

ApplicationURL
http://www.simuvis.de/

BuildVersion
0

CancelledInstallAction
{Rollback and Stop}

CleanupCancelledInstall
Yes

Company
{Joerg Raedler}

CompressionMethod
zlib

Copyright
{GPL v2}

CreateDesktopShortcut
Yes

CreateQuickLaunchShortcut
Yes

DefaultDirectoryPermission
0755

DefaultFilePermission
0755

DefaultLanguage
English

ExtractSolidArchivesOnStartup
No

FallBackToConsole
Yes

Icon
/home/joerg/installjammer/Images/SimuVis/Small/SimuVis4Small01.gif

Image
/home/joerg/installjammer/Images/SimuVis/SimuVis401.gif

IncludeDebugging
Yes

InstallDir
<%Home%>/<%ShortAppName%>

InstallMode
Standard

InstallType
Typical

InstallVersion
1.0.0.0

LaunchApplication
Yes

MajorVersion
1

MinorVersion
0

PackageDescription
{}

PackageLicense
{}

PackageMaintainer
{}

PackageName
<%ShortAppName%>

PackagePackager
{}

PackageRelease
<%PatchVersion%>

PackageSummary
{}

PackageVersion
<%MajorVersion%>.<%MinorVersion%>

PatchVersion
0

ProgramExecutable
<%InstallDir%>/SimuVis4/bin/SimuVis.pyw

ProgramFolderAllUsers
No

ProgramFolderName
<%AppName%>

ProgramLicense
<%InstallDir%>/SimuVis4/data/GPLv2.txt

ProgramName
{}

ProgramReadme
<%InstallDir%>/SimuVis4/data/README.txt

PromptForRoot
Yes

RequireRoot
No

RootInstallDir
/opt/<%ShortAppName%>

ShortAppName
SimuVis4

UpgradeApplicationID
{}

Version
4.0.333

ViewReadme
Yes

WizardHeight
365

WizardWidth
500

}
array set ::InstallJammer::CommandLineOptions {
debug
{Debugging Switch Yes No {} {run installer in debug mode}}

debugconsole
{ShowConsole Switch Yes No {} {run installer with a debug console open}}

mode
{InstallMode Choice No No {Console Default Silent Standard} {set the mode to run the installer in}}

prefix
{InstallDir String No No {} {set the installation directory}}

test
{Testing Switch Yes No {} {run installer without installing any files}}

}
