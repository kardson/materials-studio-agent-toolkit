use strict;
use warnings;
use MaterialsScript qw(:all);

my $output = 'gui_loop_enqueue_probe_output.txt';
open(my $fh, '>', $output) or die "Cannot write $output: $!";
print $fh "GUI_LOOP_ENQUEUE_PROBE_OK\n";
close($fh);
print "gui_loop_enqueue_probe_ok\n";
