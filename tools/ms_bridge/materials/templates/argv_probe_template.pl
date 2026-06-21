use strict;
use warnings;
use MaterialsScript qw(:all);

my $index = 0;
foreach my $arg (@ARGV) {
    print "ARGV[$index]=$arg\n";
    $index++;
}
