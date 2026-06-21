use strict;
use warnings;

use lib 'C:/Program Files (x86)/BIOVIA/Materials Studio 24.1/etc/Gateway/root_default/dsd/commands';
use dsd_commands;
use DSD_utils;

my $mode = shift @ARGV or die "mode is required\n";

if ($mode eq 'query-status') {
    my $jobid = shift @ARGV or die "jobid is required\n";
    my $status = dsd_commands::getJobStatus($jobid);
    print $status;
    exit 0;
}

if ($mode eq 'stop-job') {
    my $jobid = shift @ARGV or die "jobid is required\n";
    dsd_commands::stopJob($jobid);
    print "stopped";
    exit 0;
}

die "unsupported mode: $mode\n";
