# my-rpm-build-broke

...and now what?! Those logs are so long, I don't know what went wrong.


## Motivation

With the success of [large language
models](https://en.wikipedia.org/wiki/Large_language_model) it's time to say
goodbye to analysis of megabytes of logs and leave this job to these AI models.

Why should I as a human spend minutes, hours of reading these giant logs when
we finally have software that can do that very well instead of me.


## Usage

This is a simple proof of concept command line tool that obtains logs from a
failed [Copr](https://copr.fedorainfracloud.org) build, extracts relevant
subset from it and sends it to OpenAI API for analysis. OpenAI then provides
analysis and resolution.

```
$ ./my-rpm-build-broke.py 123456
```


## Requirements

```
$ pip3 install -r ./requirements.txt
```

[OpenAI API token](https://platform.openai.com/account/api-keys)
```
export OPEN_API_TOKEN=fooo-bar-baz
```

OpenAI doesn't provide a free tier for API access, so you are going to pay for every query. New accounts seem to get time-limited starter budget.

This tool consumes around 1700 tokens per "chat". The pricing right now for gpt-3.5-turbo is
```
4K context
Input: $0.0015 / 1K tokens
Output: $0.002 / 1K tokens
```
so every run would cost you around $0.002

I strongly suggest [to set usage limits](https://platform.openai.com/account/billing/limits).

## Example

```
$ python3 ./my-rpm-build-broke.py 6168772
JSSSession
[ERROR] /builddir/build/BUILD/pki-11.5.0/base/server/src/main/java/org/dogtagpki/server/PKIServerSocketListener.java:[233,39] cannot find symbol
[ERROR]   symbol:   method getLocalAddr()
[ERROR]   location: variable session of type org.mozilla.jss.ssl.javax.JSSSession
[ERROR] /builddir/build/BUILD/pki-11.5.0/base/server/src/main/java/org/dogtagpki/server/PKIServerSocketListener.java:[234,51] cannot find symbol
[ERROR]   symbol:   method getLocalAddr()
[ERROR]   location: variable session of type org.mozilla.jss.ssl.javax.JSSSession
[ERROR] /builddir/build/BUILD/pki-11.5.0/base/server/src/main/java/org/dogtagpki/server/PKIServerSocketListener.java:[310,31] cannot find symbol
[ERROR]   symbol:   method getRemoteAddr()
[ERROR]   location: variable session of type org.mozilla.jss.ssl.javax.JSSSession
[ERROR] /builddir/build/BUILD/pki-11.5.0/base/server/src/main/java/org/dogtagpki/server/PKIServerSocketListener.java:[311,43] cannot find symbol
[ERROR]   symbol:   method getRemoteAddr()
[ERROR]   location: variable session of type org.mozilla.jss.ssl.javax.JSSSession
[ERROR] /builddir/build/BUILD/pki-11.5.0/base/server/src/main/java/org/dogtagpki/server/PKIServerSocketListener.java:[313,31] cannot find symbol
[ERROR]   symbol:   method getLocalAddr()
[ERROR]   location: variable session of type org.mozilla.jss.ssl.javax.JSSSession
[ERROR] /builddir/build/BUILD/pki-11.5.0/base/server/src/main/java/org/dogtagpki/server/PKIServerSocketListener.java:[314,43] cannot find symbol
[ERROR]   symbol:   method getLocalAddr()
[ERROR]   location: variable session of type org.mozilla.jss.ssl.javax.JSSSession
[ERROR] -> [Help 1]
[ERROR]
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR]
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/MojoFailureException
[ERROR]
[ERROR] After correcting the problems, you can resume the build with the command
[ERROR]   mvn <args> -rf :pki-server
error: Bad exit status from /var/tmp/rpm-tmp.OzToqy (%build)


RPM build errors:
    Bad exit status from /var/tmp/rpm-tmp.OzToqy (%build)
Finish: rpmbuild pki-11.5.0-0.20230713092329451267.pr4487.309.g1028dadce.el9.src.rpm
Finish: build phase for pki-11.5.0-0.20230713092329451267.pr4487.309.g1028dadce.el9.src.rpm
INFO: chroot_scan: 3 files copied to /var/lib/copr-rpmbuild/results/chroot_scan
INFO: /var/lib/mock/rhel-9-x86_64-1689240256.573275/root/var/log/dnf.rpm.log
/var/lib/mock/rhel-9-x86_64-1689240256.573275/root/var/log/dnf.librepo.log
/var/lib/mock/rhel-9-x86_64-1689240256.573275/root/var/log/dnf.log
ERROR: Exception(/var/lib/copr-rpmbuild/results/pki-11.5.0-0.20230713092329451267.pr4487.309.g1028dadce.el9.src.rpm) Config(rhel-9-x86_64) 1 minutes 5 seconds
INFO: Results and/or logs in: /var/lib/copr-rpmbuild/results
INFO: Cleaning up build root ('cleanup_on_failure=True')
Start: clean chroot
INFO: unmounting tmpfs.
Finish: clean chroot
ERROR: Command failed:
 # /usr/bin/systemd-nspawn -q -M c951b4aec5d741dc9873ed21b2ae33ec -D /var/lib/mock/rhel-9-x86_64-1689240256.573275/root -a -u mockbuild --capability=cap_ipc_lock --rlimit=RLIMIT_NOFILE=10240 --capability=cap_ipc_lock --bind=/tmp/mock-resolv.vtwabed_:/etc/resolv.conf --bind=/dev/btrfs-control --bind=/dev/mapper/control --bind=/dev/loop-control --bind=/dev/loop0 --bind=/dev/loop1 --bind=/dev/loop2 --bind=/dev/loop3 --bind=/dev/loop4 --bind=/dev/loop5 --bind=/dev/loop6 --bind=/dev/loop7 --bind=/dev/loop8 --bind=/dev/loop9 --bind=/dev/loop10 --bind=/dev/loop11 --console=pipe --setenv=TERM=vt100 --setenv=SHELL=/bin/bash --setenv=HOME=/builddir --setenv=HOSTNAME=mock --setenv=PATH=/usr/bin:/bin:/usr/sbin:/sbin --setenv=PROMPT_COMMAND=printf "\033]0;<mock-chroot>\007" --setenv=PS1=<mock-chroot> \s-\v\$  --setenv=LANG=C.UTF-8 --resolv-conf=off bash --login -c /usr/bin/rpmbuild -bb  --target x86_64 --nodeps /builddir/build/SPECS/pki.spec

Copr build error: Build failed




The root cause of the error is that the symbol `getLocalAddr()` and `getRemoteAddr()` cannot be found in the `org.mozilla.jss.ssl.javax.JSSSession` class. These symbols are being used in the `PKIServerSocketListener.java` file.

To fix this issue, you need to update the code in the `PKIServerSocketListener.java` file to use the correct methods or classes that provide the `getLocalAddr()` and `getRemoteAddr()` functionality.

You can start by checking the documentation of the `org.mozilla.jss.ssl.javax.JSSSession` class to see if there are any alternative methods or classes that provide the required functionality. If such methods or classes are available, you can update the code accordingly.

If there are no alternative methods or classes available, you may need to check if there are any updates or patches available for the `org.mozilla.jss` library that provides the `JSSSession` class. Updating the library to a newer version may resolve the issue.

Once you have made the necessary code changes or updated the library, you can rebuild the RPM package using the updated code.
```


## Future work

I have plenty of ideas where to go from here.

Post-processing the AI recommendation would also be beneficial.

Try different models.

Make the interface more usable.
