use strict;
use warnings;
use MaterialsScript qw(:all);

my $doc = Documents->Item($ARGV[0]);
my $results = Modules->CASTEP->Energy->Run($doc, Settings(
  Quality => "Coarse"
));
my $result_doc = $results->Structure;
print "submitted\n";
