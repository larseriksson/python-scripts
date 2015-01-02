# inflate_debian.py

This script will inflate the data part of a debian package. This might be useful when you want to extract the files
in a debian file and make a raw installation of the files by copying the contents to the root. Observe that installation
will do more than that but for certain application this is will work out. 

The reason for this script is to install debian packages into the filesystem since I belong to the minority that prefers
to run Fedora system by different reasons. Some application is released in debian package only and may eventually be
released to other format such as rpm-package.

Use it with great care since the script will make a privilege copy of the content into the file system. Some nice
flags will be added at later stage when I get the need to customize the installation. 

As can be seen in the code, the script requires that **ar**, **xz** and **tar** commands are installed in the system
and the data in that is packaged in the data.tar.xz file will be decompressed in two steps into a temporary folder and
will be distribute to the filesystem using a distributed copy of the folders. Observe that any files that is expected 
to be in the root will not be copied.

The script can be run under the user but requires sudo-privileges for this user. By interrupting at this step when
the sudo-password is requested, the files will remain at the temporary location. If the script stops normally, the
temporary files are cleaned up.

TODO: Add a couple of test cases
