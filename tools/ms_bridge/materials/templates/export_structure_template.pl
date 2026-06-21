use strict;
use warnings;
use MaterialsScript qw(:all);

my $doc = Documents->Item($ARGV[0]);
$doc->Export($ARGV[1], Settings(Version => "2023", OmitNewerContent => "No"));
print "exported\n";
